import os
import pandas as pd

ref_summaries_dir = "tedtalk_summarization/reference/"

data = pd.read_csv('tedtalks.csv')
total_ted_talks = len(data.index)

for i, row in data.iterrows():
    if(i % 250 == 0):
        print(f"Processing {i}/{total_ted_talks}")
        
    ref_summary = row['summary']

    file_path = os.path.join(ref_summaries_dir, f"tedtalk{i}_ref.txt")
    file = open(file_path, "w")
    file.write(ref_summary)