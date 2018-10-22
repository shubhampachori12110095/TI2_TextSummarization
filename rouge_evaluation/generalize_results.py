
import csv
import glob
from collections import defaultdict

def fix_csv(in_filename, out_filename):
    with open(in_filename, "r") as orig_csvfile, open(out_filename, "w") as dest_csvfile:
        linereader = csv.reader(orig_csvfile)

        for i, csv_row in enumerate(linereader, start=1):
            if i == 1:
                # Headers estão certos, só mantém
                dest_csvfile.write(','.join(csv_row) + "\n")
                continue

            if len(csv_row) == 0:
                # Linha vazia, ignora
                continue

            if csv_row[3] == 'NaN' or \
                csv_row[5] == 'NaN' or \
                csv_row[7] == 'NaN':
                # De vez em quanto dá uns NaN nos resultados que ele
                # calculou não faço ideia do porque
                continue

            # Junta os decimais que ele separou em 2 colunas
            fixed_row = csv_row[0] + ',' \
                + csv_row[1] + ',' \
                + csv_row[2] + ',' \
                + csv_row[3] + '.' + csv_row[4] + ',' \
                + csv_row[5] + '.' + csv_row[6] + ',' \
                + csv_row[7] + '.' + csv_row[8] + ',' \
                + csv_row[9] + "\n"

            dest_csvfile.write(fixed_row)

def compute_average(in_filename, out_filename, num_summaries):
    rouge_names = []

    # Nome => soma do recall/precision/fscore
    rouge_recall_sum = defaultdict(lambda: 0)
    rouge_precision_sum = defaultdict(lambda: 0)
    rouge_fscore_sum = defaultdict(lambda: 0)

    with open(in_filename, "r") as orig_csvfile:
        linereader = csv.reader(orig_csvfile)

        for i, csv_row in enumerate(linereader, start=1):
            if i == 1:
                # Ignore a linha dos headers
                continue

            # Lê os valores
            rouge_name = csv_row[0]
            recall = float(csv_row[3])
            precision = float(csv_row[4])
            fscore = float(csv_row[5])

            # Salva o nome do ROUGE
            if rouge_name not in rouge_names:
                rouge_names.append(rouge_name)

            # Soma o quanto deu pra cada medida
            rouge_recall_sum[rouge_name] += recall
            rouge_precision_sum[rouge_name] += precision
            rouge_fscore_sum[rouge_name] += fscore

    with open(out_filename, "w") as dest_csvfile:
        dest_csvfile.write("ROUGE \t Recall (avg) \t Precision (avg) \t F-Score (avg)\n")

        for rouge_name in rouge_names:
            avg_recall = rouge_recall_sum[rouge_name] / num_summaries
            avg_precision = rouge_precision_sum[rouge_name] / num_summaries
            avg_fscore = rouge_fscore_sum[rouge_name] / num_summaries

            dest_csvfile.write(f"{rouge_name} \t {avg_recall} \t {avg_precision} \t {avg_fscore} \n")


TEXT_RANK_COMPUTED_RESULTS = 'textRankEval/results.csv'
TEXT_RANK_FIXED_CSV = 'textRankEval/fixed_results.csv'
TEXT_RANK_FINAL_RESULTS = 'textRankEval/final_results.txt'

PGN_COMPUTED_RESULTS = 'pointerGenEval/results.csv'
PGN_FIXED_CSV = 'pointerGenEval/fixed_results.csv'
PGN_FINAL_RESULTS = 'pointerGenEval/final_results.txt'


# Parece que tem um problema de locale, ele salva os valores decimais
# como "x,xxxxx" (usa vírgula ao invés de ponto), o que zoa o CSV
fix_csv(TEXT_RANK_COMPUTED_RESULTS, TEXT_RANK_FIXED_CSV)
# fix_csv(PGN_COMPUTED_RESULTS, PGN_FIXED_CSV)


# Esse Rouge 2.0 só dá o resultado para cada resumo,
# não faz a média. Temos que fazer na mão
num_summaries_on_text_rank = len(glob.glob('textRankEval/system/*.txt'))
# num_summaries_on_pgn = len(glob.glob('pointerGenEval/system/*.txt'))

compute_average(TEXT_RANK_FIXED_CSV, TEXT_RANK_FINAL_RESULTS, num_summaries_on_text_rank)
# compute_average(PGN_FIXED_CSV, PGN_FINAL_RESULTS, num_summaries_on_pgn)