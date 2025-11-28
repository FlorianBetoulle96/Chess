import chess.engine
import statistics
import time

fen1 = "r3k2r/pp1n2p1/3b1q1p/1BpPp3/Q3Pp2/5N2/PP3PPP/R4RK1 b kq"
fen2 = "r3k2r/pq3ppp/1bn1p3/3pPn2/1Pp2B2/2P2N2/P1QN1PPP/R4RK1 w kq"
fen3 ="2rq1rk1/pp2bppp/8/5p2/2Q5/2N5/PP3PPP/R1B2RK1 w -"
fen4 = "r1bqkb1r/ppp1pppp/2n2n2/3p4/3P1B2/5N2/PPP1PPPP/RN1QKB1R w -"

def get_stockfish(fen, time_limit, stockfish_path):
    board = chess.Board(fen)

    with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
        info = engine.analyse(board, chess.engine.Limit(time=time_limit))
        # info = engine.analyse(board, chess.engine.Limit(depth=100))

        # Coup principal
        best_move = info.get("pv")[0] if "pv" in info else None

        # Score
        score_obj = info["score"].white()
        if score_obj.is_mate():
            score = 100000 if score_obj.mate() > 0 else -100000
        else:
            score = score_obj.score(mate_score=100000)
        if isinstance(score, tuple):
            score = score[0] if isinstance(score[0], (int, float)) else 0

        # Autres infos utiles
        depth = info.get("depth", None)
        seldepth = info.get("seldepth", None)
        nodes = info.get("nodes", None)
        nps = info.get("nps", None)
        time_spent = info.get("time", None)

        # print(f"Best move: {board.san(best_move) if best_move else None}")
        # print(f"Score (centipions): {score}")
        # print(f"Depth: {depth}, SelDepth: {seldepth}")
        # print(f"Nodes: {nodes}, NPS: {nps}, Time: {round(time_spent,3) if time_spent else None}s")

        return best_move, score, depth, seldepth, nodes, nps, time_spent

time_limit = 8
best_move, score, depth, seldepth, nodes, nps, time_spent = get_stockfish(fen4, time_limit,"./stockfish.exe")
print("time_limit : ", time_limit)
print("Meilleur coup :", best_move)
print("Score (centipions) :", score)
print("Profondeur :", depth)
print("Profondeur de sélection :", seldepth)
print("Nœuds analysés :", nodes)   

#--> on vise profondeur 26 pour elo 2800
