import re
import csv

input_file = "../Files/perf_results.txt"
output_file = "../Files/perf_results_cleaned.csv"

# Regex plus souple (accepte entiers ou décimaux, espaces facultatifs)
line_re = re.compile(
    r"FEN_(\d+)\s+([rnbqkpRNBQKP1-8/ ]+[wb]\s[-kq]+)\s*\|\s*([\d.]+)s\s*\|\s*"
    r"score_avg\s*=\s*(-?[\d.]+)\s*\|\s*elo_est\s*=\s*(\d+)\s*\|\s*"
    r"diff_max\s*=\s*(\d+)\s*\|\s*diff_avg\s*=\s*([\d.]+)\s*\|\s*"
    r"depth_avg\s*=\s*([\d.]+)\s*\|\s*nodes_avg\s*=\s*(\d+)\s*\|\s*%_same_move\s*=\s*([\d.]+)"
)

with open(input_file, "r", encoding="utf-8") as f_in, open(output_file, "w", newline="", encoding="utf-8") as f_out:
    writer = csv.writer(f_out)
    writer.writerow([
        "fen_idx", "fen", "time", "score_avg", "elo_est",
        "diff_max", "diff_avg", "depth_avg", "nodes_avg", "%_same_move"
    ])

    for line in f_in:
        match = line_re.search(line)
        if match:
            fen_idx, fen, time, score_avg, elo_est, diff_max, diff_avg, depth_avg, nodes_avg, pct_same = match.groups()
            writer.writerow([
                fen_idx, fen.strip(), time, score_avg, elo_est,
                diff_max, diff_avg, depth_avg, nodes_avg, pct_same
            ])

print(f"✅ CSV créé : {output_file}")