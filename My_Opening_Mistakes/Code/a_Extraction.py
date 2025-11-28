import chess
import chess.pgn
import io

def a_extraction(pgn_file, player_name="Floflolasticow", min_move=3, max_move=15):
    """
    pgn_file : soit un chemin vers un fichier PGN, soit un flux texte (UploadedFile Streamlit)
    """

    # --- Gestion du flux ---
    if isinstance(pgn_file, str):
        # Si c'est un chemin
        pgn_io = open(pgn_file, encoding="utf-8")
        close_file = True
    else:
        # Sinon, c'est un flux binaire/textuel (ex: UploadedFile)
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
    with open("../Files/games_fen.txt", "w", encoding="utf-8") as f:
        for idx, game_data in enumerate(results, 1):
            f.write(f"Game {idx} - {game_data['color']}\n")
            for fen, next_move in game_data["moves_fens"]:
                f.write(f"{fen} / {next_move}\n")
            f.write("\n")

    print("✅ Export terminé dans games_fens.txt")
    return results