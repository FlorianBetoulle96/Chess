import chess
import chess.pgn

def pgns_to_fens_with_next_move(pgn_file, player_name="Floflolasticow", min_move=5, max_move=30):
    results = []

    with open(pgn_file, encoding="utf-8") as pgn:
        while True:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break

            # --- Identifier ta couleur ---
            white = game.headers.get("White", "")
            black = game.headers.get("Black", "")
            if white == player_name:
                color = "White"
            elif black == player_name:
                color = "Black"
            else:
                color = "Unknown"

            board = game.board()
            move_fen_pairs = []

            moves = list(game.mainline_moves())
            for i, move in enumerate(moves):
                board.push(move)

                # On ne garde que si le coup suivant existe
                if i + 1 < len(moves):
                    next_move = moves[i + 1]
                    next_move_san = board.san(next_move)

                    # Index de coup complet = i + 1 (1-based)
                    if min_move <= i + 1 <= max_move:
                        move_fen_pairs.append((board.fen(), next_move_san))

            results.append({
                "color": color,
                "moves_fens": move_fen_pairs
            })

    return results

data = pgns_to_fens_with_next_move("../Files/games_pgn.pgn")

# === Export ===
with open("../Files/games_fen.txt", "w", encoding="utf-8") as f:
    for idx, game_data in enumerate(data, 1):
        f.write(f"Game {idx} - {game_data['color']}\n")
        for fen, next_move in game_data["moves_fens"]:
            f.write(f"{fen} / {next_move}\n")
        f.write("\n")

print("✅ Export terminé dans multiples_fens.txt")