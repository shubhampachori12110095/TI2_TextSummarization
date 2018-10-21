import os
import pandas as pd

REF_SUMMARIES_DIR = "reference/"

data = pd.read_csv('../data/final_dataset.csv')
total_ted_talks = len(data.index)

for i, row in data.iterrows():
    if(i % 250 == 0):
        print(f"Processing {i}/{total_ted_talks}")
        
    ref_summary = row['summary']

    file_path = os.path.join(REF_SUMMARIES_DIR, f"tedtalk{i}_Dataset.txt")
    file = open(file_path, "w")
    file.write(ref_summary)