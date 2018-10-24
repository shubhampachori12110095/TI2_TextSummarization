import pandas as pd
from nltk import tokenize
import re
import glob
import os
import shutil

# Pega o número do nome do arquivo
# Ex: "tedtalk30_whatever.txt" ==> 30
# Ex: "tedtalk13_whatever.txt" ==> 13
def get_tedtalk_num(filepath):
    filename = os.path.basename(filepath)    
    return re.search('\d+', filename).group()

def text_to_one_sentence_per_line(text):
    sentences = tokenize.sent_tokenize(text)

    output_text = ""
    for sentence in sentences:
        output_text += sentence + "\n"

    return output_text

def prepare_to_eval(generated_summaries, reference_summaries_dir):
    # Recria a pasta de resumos de referências
    # Ela vai ser preenchida de acordo com os resumos
    # que estão na pasta system
    shutil.rmtree(reference_summaries_dir)
    os.mkdir(reference_summaries_dir)

    data = pd.read_csv(PATH_TO_DATASET)

    for gen_summary_filepath in generated_summaries:
        # Pega o número do TED Talk do nome do arquivo
        tedtalk_num = get_tedtalk_num(gen_summary_filepath)

        # Lê o respectivo resumo de referência do dataset
        # O -1 é por causa da diferença na faixa
            # números nos arquivos: 1 a n
            # números no dataset: 0 a n-1
        ref_summary = data.loc[int(tedtalk_num)-1, 'summary']
        
        # Formata o resumo de referencia como o Rouge pede (uma sentença por linha)
        formatted_ref_summary = text_to_one_sentence_per_line(ref_summary)

        ref_summary_file_path = os.path.join(reference_summaries_dir, f"tedtalk{tedtalk_num}_Dataset.txt")
        with open(ref_summary_file_path, "w") as ref_summary_file:
            ref_summary_file.write(formatted_ref_summary)

        # Formata o resumo gerado como o Rouge pede (uma sentença por linha)
        with open(gen_summary_filepath, "r+") as gen_summary_file:
            gen_summary = gen_summary_file.read()

            formatted_gen_summary = text_to_one_sentence_per_line(gen_summary)

            gen_summary_file.write(formatted_gen_summary)

PATH_TO_DATASET = '../data/final_dataset.csv'

TEXTRANK_EVAL_DIR = "./textRankEval"
POINTERGEN_EVAL_DIR = "./pointerGenEval"

textrank_summaries = glob.glob(f"{TEXTRANK_EVAL_DIR}/system/*.txt")

print("Preparing to evaluate TextRank generated summaries...")
prepare_to_eval(textrank_summaries, f"{TEXTRANK_EVAL_DIR}/reference")

pointergen_summaries = glob.glob(f"{POINTERGEN_EVAL_DIR}/system/*.txt")

print("Preparing to evaluate Pointer-Generator generated summaries...")
prepare_to_eval(pointergen_summaries, f"{POINTERGEN_EVAL_DIR}/reference")