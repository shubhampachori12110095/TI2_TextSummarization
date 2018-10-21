import pandas as pd
from summa import summarizer
from nltk import tokenize
import os
import subprocess
import glob

#-------------------------------------------------------------

def run_text_rank(text_filenames):
    total_itens = len(text_filenames)

    for i, filename in enumerate(text_filenames, start=1):
        with open(filename, "r") as input_file:
            input_text = input_file.read()

        if(i % 250 == 0):
            print(f"Processing {i}/{total_itens}")

        generated_summary = summarizer.summarize(input_text, words=100)
        
        out_file_path = os.path.join(TEXTRANK_OUTPUT_DIR, f"tedtalk{i}_TextRank.txt")
        with open(out_file_path, "w") as output_file:
            output_file.write(generated_summary)

#-------------------------------------------------------------

def run_pointer_generator():
    PATH_TO_BIN_INPUT = '../data/bin_input/finished_files/test.bin'

    subprocess.call(
        ['python', 'run_summarization.py', '--mode=decode',
            f"--data_path=../../{PATH_TO_BIN_INPUT}",
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
    FILES_GENERATED = 'pgn/pretrained_model/decode_test_400maxenc_4beam_35mindec_100maxdec_ckpt-238410/decoded/*_decoded.txt'
    for i, filepath in enumerate(glob.glob(FILES_GENERATED)):
        correct_path = os.path.join(PGN_OUTPUT_DIR, f"tedtalk{i}_PGN.txt")
        os.replace(filepath, correct_path)

#-------------------------------------------------------------

TEXT_INPUT_DIR = "../data/text_input"
TEXTRANK_OUTPUT_DIR = "../rouge_evaluation/textRankEval/system"
PGN_OUTPUT_DIR = "../rouge_evaluation/pointerGenEval/system"

text_input_filenames = glob.glob(f"{TEXT_INPUT_DIR}/*.txt")

print("Running TextRank...")
run_text_rank(text_input_filenames)

#print("Running Pointer-Generator Network...")
#run_pointer_generator()