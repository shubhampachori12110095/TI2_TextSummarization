import pandas as pd
import os
import glob
from distutils.dir_util import copy_tree
from nltk import tokenize

def text_to_one_sentence_per_line(text):
    sentences = tokenize.sent_tokenize(text)

    output_text = ""
    for sentence in sentences:
        output_text += sentence + "\n"

    return output_text

def create_reference_summaries():
    data = pd.read_csv('../data/final_dataset.csv')
    total_ted_talks = len(data.index)

    for i, row in data.iterrows():
        tedtalk_number = i+1

        if(i % 250 == 0):
            print(f"Processing {i}/{total_ted_talks}")

        # Lê do dataset
        ref_summary = row['summary']

        # Precisa estar em uma sentença por linha
        formatted_ref_summary = text_to_one_sentence_per_line(ref_summary)

        # Escreve em um arquivo em uma das pastas
        file_path = os.path.join(REF_SUMMARIES_DIR, f"tedtalk{tedtalk_number}_Dataset.txt")
        with open(file_path, "w") as output:
            output.write(formatted_ref_summary)

    # Para cada algoritmo é uma avaliação separada, então
    # tem que ficar em pastas diferentes. No entanto os resumos
    # de referência são os mesmos, então é só copiar a pasta inteira
    copy_tree(REF_SUMMARIES_DIR, REF_SUMMARIES_DIR2)

def format_generated_summaries():
    for file_path in glob.glob(TEXTRANK_GEN_SUMMARIES):
        with open(file_path, "r+") as f:
            gen_summary = f.read()

            # Precisa estar em uma sentença por linha
            formatted_gen_summary = text_to_one_sentence_per_line(gen_summary)

            f.write(formatted_gen_summary)

    # for file_path in glob.glob(PGN_GEN_SUMMARIES):
    #     with open(file_path, "r+") as f:
    #         gen_summary = f.read()

    #         # Precisa estar em uma sentença por linha
    #         formatted_gen_summary = text_to_one_sentence_per_line(gen_summary)

    #         f.write(formatted_gen_summary)

REF_SUMMARIES_DIR = "textRankEval/reference/"
REF_SUMMARIES_DIR2 = "pointerGenEval/reference/"
TEXTRANK_GEN_SUMMARIES = "textRankEval/system/*.txt"
PGN_GEN_SUMMARIES = "pointerGenEval/system/*.txt"

print("Creating reference summaries...")
create_reference_summaries()

print("Formatting generated summaries...")
format_generated_summaries()