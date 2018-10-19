import pandas as pd
from summa import summarizer
from nltk import tokenize
import os

gen_summaries_dir = "../rouge_evaluation/system/"

data = pd.read_csv('tedtalks.csv')
total_ted_talks = len(data.index)

# Summa: TextRank
for i, row in data.iterrows():
    if(i % 250 == 0):
        print(f"Processing {i}/{total_ted_talks}")

    full_text = row['transcript']
    
    # Summa requer que cada sentença esteja em uma linha
    sentences = tokenize.sent_tokenize(full_text)
    full_text = ""
    for sentence in sentences:
        full_text += sentence + "\n"

    generated_summary = summarizer.summarize(full_text, words=100)
    
    file_path = os.path.join(gen_summaries_dir, f"tedtalk{i}_TextRank.txt")
    file = open(file_path, "w")
    file.write(generated_summary)

# Pointer-generator network
# TODO