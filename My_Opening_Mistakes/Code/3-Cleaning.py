def final_cleaning(input_file, output_file):
    """
    Nettoie le fichier pour ne garder que les coups, en format CSV compact :
    <position>,<couleur>,<numéro du coup>,<ton coup>,<eval ton coup>,<SF move>,<eval SF move>
    Les lignes d'en-tête sont supprimées.
    """
    with open(input_file, "r", encoding="utf-8") as f_in, \
         open(output_file, "w", encoding="utf-8") as f_out:

        for line in f_in:
            line_strip = line.strip()
            # Ignorer les lignes vides et les en-têtes "Game"
            if not line_strip or line_strip.startswith("Game"):
                continue

            try:
                # Split sur " / "
                parts = [x.strip() for x in line_strip.split(" / ")]

                # FEN complète
                fen_full = parts[0]

                # Découper la FEN pour garder seulement :
                # <position>, <couleur>, <numéro du coup>
                fen_fields = fen_full.split(" ")
                fen_position = fen_fields[0]  # position des pièces
                fen_color = fen_fields[1]     # b ou w
                fen_fullmove = fen_fields[5]  # numéro du coup complet

                # Ajouter les autres éléments (ton coup, eval, SF move, eval)
                other_parts = parts[1:]

                # Écriture CSV compacte (tout accolé)
                new_line = f"{fen_position},{fen_color},{fen_fullmove}," + ",".join(other_parts) + "\n"
                f_out.write(new_line)

            except Exception as e:
                f_out.write(f"# Erreur sur la ligne : {line_strip} ({e})\n")

final_cleaning(
    input_file="../Files/multiples_fens_stockfish.txt",
    output_file="../Files/final_cleaned.csv"
)