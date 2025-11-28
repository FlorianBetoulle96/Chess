import chess
import chess.pgn
import io
import os

def a_extraction(pgn_file, player_name="Floflolasticow", min_move=3, max_move=15, output_path="../Files/games_fen.txt"):
    """
    Extrait les positions FEN et les coups d'un fichier PGN pour un joueur donné.

    Args:
        pgn_file: chemin vers un fichier PGN ou flux texte (UploadedFile Streamlit)
        player_name: nom du joueur pour identifier la couleur
        min_move: numéro du premier coup à conserver
        max_move: numéro du dernier coup à conserver
        output_path: chemin du fichier de sortie
    """

    # --- Création du dossier si besoin ---
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # --- Gestion du flux ---
    if isinstance(pgn_file, str):
        pgn_io = open(pgn_file, encoding="utf-8")
        close_file = True
    else:
        content = pgn_file.read()
        if isinstance(content, bytes):
            content = content.decode("utf-8")
        pgn_io = io.StringIO(content)
        close_file = False

    # --- Lecture des parties et extraction FENs ---
    results = []
    while True:
        game = chess.pgn.read_game(pgn_io)
        if game is None:
            break

        # Identifier la couleur
        white = game.headers.get("White", "")
        black = game.headers.get("Black", "")
        color = "Unknown"
        if white == player_name:
            color = "White"
        elif black == player_name:
            color = "Black"

        board = game.board()
        move_fen_pairs = []

        moves = list(game.mainline_moves())
        for i, move in enumerate(moves):
            board.push(move)
            if i + 1 < len(moves):
                next_move = moves[i + 1]
                next_move_san = board.san(next_move)
                if min_move <= i + 1 <= max_move:
                    move_fen_pairs.append((board.fen(), next_move_san))

        results.append({"color": color, "moves_fens": move_fen_pairs})

    if close_file:
        pgn_io.close()

    # --- Export ---
    with open(output_path, "w", encoding="utf-8") as f:
        for idx, game_data in enumerate(results, 1):
            f.write(f"Game {idx} - {game_data['color']}\n")
            for fen, next_move in game_data["moves_fens"]:
                f.write(f"{fen} / {next_move}\n")
            f.write("\n")

    print(f"✅ Export terminé dans {output_path}")
    return results
