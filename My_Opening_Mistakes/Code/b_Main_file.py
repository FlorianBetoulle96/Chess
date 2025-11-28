import chess
from stockfish import Stockfish

def b_main_file() :

    STOCKFISH_PATH = r"../Files/stockfish.exe"
    stockfish = Stockfish(STOCKFISH_PATH)

    def evaluate_position(fen):
        stockfish.update_engine_parameters({"UCI_Elo": 2800})
        stockfish.set_fen_position(fen)
        best_move_long = stockfish.get_best_move()
        score = stockfish.get_evaluation()
        return best_move_long, score

    input_file = "../Files/games_fen.txt"
    output_file = "../Files/final.txt"

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

                # meilleur coup de stockfish en long
                best_move_sf, eval_after_sf = evaluate_position(fen)

                # conversion de TON coup vers notation longue
                board = chess.Board(fen)
                move_obj = board.parse_san(my_move_san)
                my_move_long = move_obj.uci()

                # évaluation après ton coup
                board.push(move_obj)
                fen_after_my_move = board.fen()
                _, eval_after_my_move = evaluate_position(fen_after_my_move)

                f_out.write(f"{fen} / {best_move_sf} / {eval_after_sf} / {my_move_long} / {eval_after_my_move}\n")

            except Exception as e:
                f_out.write(f"# Erreur sur la ligne : {line} ({e})\n")
            print("line", line)

    print(f"✅ Analyse complète enregistrée dans {output_file}")
