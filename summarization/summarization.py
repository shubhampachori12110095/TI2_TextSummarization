import pandas as pd
from summa import summarizer
from nltk import tokenize
import subprocess
import re
import glob
import tempfile
import os
import shutil

#-------------------------------------------------------------

def run_text_rank(text_files_full_path):
    total_itens = len(text_files_full_path)

    for i, filepath in enumerate(text_files_full_path, start=1):
        if(i % 250 == 0):
            print(f"Processing {i}/{total_itens}")

        # Pega o número do nome do arquivo
        filename = os.path.basename(filepath)
        tedtalk_num = re.search('\d+', filename).group()

        # Lê o arquivo de texto
        with open(filepath, "r") as input_file:
            input_text = input_file.read()

        generated_summary = summarizer.summarize(input_text, words=100)
        
        out_file_path = os.path.join(TEXTRANK_OUTPUT_DIR, f"tedtalk{tedtalk_num}_TextRank.txt")
        with open(out_file_path, "w") as output_file:
            output_file.write(generated_summary)

#-------------------------------------------------------------

def run_pointer_generator(text_files_full_path):
    total_itens = len(text_files_full_path)

    for i, filepath in enumerate(text_files_full_path, start=1):
        if(i % 250 == 0):
            print(f"Processing {i}/{total_itens}")

        # Pega o número do nome do arquivo
        filename = os.path.basename(filepath)
        tedtalk_num = re.search('\d+', filename).group()

        # Lê o arquivo de texto
        with open(filepath, "r") as input_file:
            input_text = input_file.read()

        # Converte para a entrada esperada pelo pointer generator (binário)
        # See: https://github.com/dondon2475848/make_datafiles_for_pgn

        # Cria 2 diretórios temporários
        with tempfile.TemporaryDirectory() as temp_text_dir, \
            tempfile.TemporaryDirectory() as temp_bin_dir:
            
            # Cria um arquivo temporário no dir de input
            # Funciona em Unix, mas não no Windows.
            # Se for rodar no Windows é preciso:
            #   - alterar isso para tempfile.NamedTemporaryFile(..., delete=False)
            #   - deletar o arquivo manualmente depois de chamar o subprocesso
            #   make_datafiles.py
            with tempfile.NamedTemporaryFile(mode='r+', dir=temp_text_dir) as temp_file:
                # Escreve o conteúdo do txt lá
                temp_file.write(input_text)

                # Converte pra binário
                subprocess.call(
                    ['python', 'make_datafiles.py', temp_text_dir, temp_bin_dir],
                    cwd='./pgn/make_datafiles_for_pgn/'
                )

            # Passa pra rede
            subprocess.call(
                ['python', 'run_summarization.py', '--mode=decode',
                    f"--data_path={temp_bin_dir}/finished_files/test.bin",
                    '--vocab_path=../vocab', # Vocabulário
                    '--log_root=..', # Pasta que contém os modelos
                    '--exp_name=pretrained_model', # Nome do modelo/pasta
                    '--single_pass=1', # Executa uma vez só para cada texto
                    '--max_enc_steps=400',
                    '--max_dec_steps=100'
                ],
                cwd='./pgn/pointer-generator/'
            )

        # Como não temos controle sobre onde os arquivos gerados pelo pgn
        # são salvos (ele simplesmente salva como "<numero do exemplo>_decode"
        # em uma pasta interna) e o ROUGE 2.0 requer que o nome e localização
        # dos arquivos sigam um padrão, precisamos renomeá-los e movê-los.
        FOLDER_GENERATED_BY_PGN = './pgn/pretrained_model/decode_test_400maxenc_4beam_35mindec_100maxdec_ckpt-238410'
        
        for filepath in glob.glob(f"{FOLDER_GENERATED_BY_PGN}/decoded/*_decoded.txt"):
            correct_path = os.path.join(PGN_OUTPUT_DIR, f"tedtalk{tedtalk_num}_PGN.txt")
            os.replace(filepath, correct_path)

        # Apaga a pasta que o pgn gerou para a próxima iteração
        # (ela não pode existir)
        shutil.rmtree(FOLDER_GENERATED_BY_PGN)

#-------------------------------------------------------------

TEXT_INPUT_DIR = "../data/text_input"
TEXTRANK_OUTPUT_DIR = "../rouge_evaluation/textRankEval/system"
PGN_OUTPUT_DIR = "../rouge_evaluation/pointerGenEval/system"

text_input_filenames = glob.glob(f"{TEXT_INPUT_DIR}/*.txt")

#print("Running TextRank...")
#run_text_rank(text_input_filenames)

print("Running Pointer-Generator Network...")
run_pointer_generator(text_input_filenames)