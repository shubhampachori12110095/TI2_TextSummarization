import pandas as pd
import os
import subprocess
from nltk import tokenize

def text_to_one_sentence_per_line(text):
    sentences = tokenize.sent_tokenize(text)

    output_text = ""
    for sentence in sentences:
        output_text += sentence + "\n"

    return output_text

def convert_to_one_sentence_per_line(data):
    data['transcript'] = data['transcript'].apply(text_to_one_sentence_per_line)

    return data

def input_data_to_individual_text_files(data, output_dir):
    for i, row in data.iterrows():
        input_text = row['transcript']

        file_path = os.path.join(output_dir, f"tedtalk{i}.txt")
        file = open(file_path, "w")
        file.write(input_text)

DATASET_PATH = '../data/final_dataset.csv'
TEXT_INPUT_DIR = '../data/text_input/'
BIN_INPUT_DIR = '../data/bin_input/'

print("Reading from dataset...")
data = pd.read_csv(DATASET_PATH)

# Ambos os algoritmos precisam que cada sentença
# esteja em uma linha
print("Converting to one sentence per line...")
data = convert_to_one_sentence_per_line(data)

# Salva cada texto de entrada em um arquivo separado.
#    O script que chamamos abaixo precisa disso. Para
# o código ficar mais consistente, o outro algoritmo
# também lê direto do arquivo
print("Saving each input in one text file...")
input_data_to_individual_text_files(data, TEXT_INPUT_DIR)

# Converte os .txts para a entrada esperada pelo pointer-generator
# (binário)
# See: https://github.com/dondon2475848/make_datafiles_for_pgn
# Os argumentos são em relação ao cwd
print("Preparing binary data to pointer-generator...")
subprocess.call(
    ['python', 'make_datafiles.py', f"../{TEXT_INPUT_DIR}", f"../{BIN_INPUT_DIR}"],
    cwd='./make_datafiles_for_pgn/'
)