import pandas as pd
from summa import summarizer
import os

gen_summaries_dir = "../rouge_evaluation/system/"

data = pd.read_csv('tedtalks.csv')
total_ted_talks = len(data.index)

# Summa: TextRank
for i, row in data.iterrows():
    if(i % 250 == 0):
        print(f"Processing {i}/{total_ted_talks}")
        
    full_text = row['transcript']
    
    generated_summary = summarizer.summarize(full_text)
    
    # O "1" no final é por ser o algoritmo 1.
    # o do pointer-networks vai ser 2
    file_path = os.path.join(gen_summaries_dir, f"tedtalk{i}_gen1.txt")
    file = open(file_path, "w")
    file.write(generated_summary)

# Pointer-generator network
# TODO