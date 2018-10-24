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
        # Números nos arquivos vão de 1 a n
        tedtalk_number = i+1

        input_text = row['transcript']

        file_path = os.path.join(output_dir, f"tedtalk{tedtalk_number}.txt")
        file = open(file_path, "w")
        file.write(input_text)

PATH_TO_DATASET = '../data/final_dataset.csv'
TEXT_INPUT_DIR = '../data/text_input/'

print("Reading from dataset...")
data = pd.read_csv(PATH_TO_DATASET)

# Ambos os algoritmos precisam que cada sentença
# esteja em uma linha
print("Converting to one sentence per line...")
data = convert_to_one_sentence_per_line(data)

# Salva cada texto de entrada em um arquivo separado
print("Saving each input in one text file...")
input_data_to_individual_text_files(data, TEXT_INPUT_DIR)