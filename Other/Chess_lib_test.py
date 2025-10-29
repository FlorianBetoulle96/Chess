import chess

#library chess  
def is_checkmate_in_one(fen): #marche
    board = chess.Board(fen)
    for move in board.legal_moves:
        board.push(move)
        if board.is_checkmate():
            board.pop()
            print(board)
            return True, move
        board.pop()
    return False, None

def has_en_passant(fen): #marche
    board = chess.Board(fen)
    for move in board.legal_moves:
        board.push(move)
        if board.has_legal_en_passant():
            board.pop()
            print(board)
            return True, move
        board.pop()
    return False, None


fen = "6k1/5ppp/8/8/8/8/5PPP/6K1 w - - 0 1"  # Position triviale, pas de mat
print(is_checkmate_in_one(fen))

fen_mate = "6k1/5ppp/8/8/8/8/5PPP/4Q1K1 w - - 0 1"  # Qf8# disponible
print(is_checkmate_in_one(fen_mate))

fen_en_passant = "rnbqkbnr/pp1ppppp/8/2pP4/4P3/5N2/PPP2PPP/RNBQKB1R b KQkq - 1 2"
print(has_en_passant(fen_en_passant))



