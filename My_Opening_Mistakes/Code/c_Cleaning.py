import re
import os

def c_cleaning():
    # --- Création du dossier Files si nécessaire ---
    os.makedirs("Files", exist_ok=True)

    def extract_eval(val):
        """Extrait juste le nombre de l'évaluation"""
        match = re.search(r"-?\d+(\.\d+)?", val)
        if match:
            return match.group(0)
        return val

    def final_cleaning(input_file, output_file):
        with open(input_file, "r", encoding="utf-8") as f_in, \
             open(output_file, "w", encoding="utf-8") as f_out:

            for line in f_in:
                line_strip = line.strip()
                if not line_strip or line_strip.startswith("Game"):
                    continue

                try:
                    parts = [x.strip() for x in line_strip.split(" / ")]
                    fen_full = parts[0]

                    # On ne garde que la position, la couleur et le numéro de coup complet
                    fen_fields = fen_full.split(" ")
                    fen_position = fen_fields[0]     # position des pièces
                    fen_color = fen_fields[1]        # b ou w
                    fen_fullmove = fen_fields[5]     # numéro du coup complet

                    # Coups et évaluations
                    my_move = parts[1]
                    my_eval = extract_eval(parts[2])
                    sf_move = parts[3]
                    sf_eval = extract_eval(parts[4])

                    # Écriture CSV compact
                    new_line = f"{fen_position},{fen_color},{fen_fullmove},{my_move},{my_eval},{sf_move},{sf_eval}\n"
                    f_out.write(new_line)

                except Exception as e:
                    f_out.write(f"# Erreur sur la ligne : {line_strip} ({e})\n")

    final_cleaning(
        input_file="Files/final.txt",
        output_file="Files/final_cleaned.csv"
    )
    print("✅ Cleaning terminé, fichier final_cleaned.csv créé dans Files/")
