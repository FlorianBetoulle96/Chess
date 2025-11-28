import chess
from stockfish import Stockfish
import os

def b_main_file():
    # --- Création du dossier Files si nécessaire ---
    os.makedirs("Files", exist_ok=True)

    # --- Chemin vers Stockfish ---
    # STOCKFISH_PATH = "Files/stockfish.exe" #path pour local (Windows)
    stockfish = Stockfish()
    # stockfish = Stockfish(STOCKFISH_PATH)

    def evaluate_position(fen):
        stockfish.update_engine_parameters({"UCI_Elo": 2800})
        stockfish.set_fen_position(fen)
        best_move_long = stockfish.get_best_move()
        score = stockfish.get_evaluation()
        return best_move_long, score

    # --- Fichiers d'entrée et de sortie ---
    input_file = "Files/games_fen.txt"
    output_file = "Files/final.txt"

    # Si le fichier d'entrée n'existe pas, on arrête
    if not os.path.exists(input_file):
        print(f"❌ Fichier d'entrée {input_file} introuvable.")
        return

    # --- Lecture et analyse ---
    with open(input_file, "r", encoding="utf-8") as f_in, \
         open(output_file, "w", encoding="utf-8") as f_out:

        for line in f_in:
            line = line.strip()
            if not line or line.startswith("Game"):
                f_out.write(line + "\n")
                continue

            try:
                parts = [x.strip() for x in line.split(" / ")]
                fen = parts[0]
                my_move_san = parts[1]

                # meilleur coup de Stockfish
                best_move_sf, eval_after_sf = evaluate_position(fen)

                # conversion du coup de l'utilisateur vers notation UCI
                board = chess.Board(fen)
                move_obj = board.parse_san(my_move_san)
                my_move_long = move_obj.uci()

                # évaluation après le coup de l'utilisateur
                board.push(move_obj)
                fen_after_my_move = board.fen()
                _, eval_after_my_move = evaluate_position(fen_after_my_move)

                f_out.write(f"{fen} / {best_move_sf} / {eval_after_sf} / {my_move_long} / {eval_after_my_move}\n")

            except Exception as e:
                f_out.write(f"# Erreur sur la ligne : {line} ({e})\n")
            print("line", line)

    print(f"✅ Analyse complète enregistrée dans {output_file}")
