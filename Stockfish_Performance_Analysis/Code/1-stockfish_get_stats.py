import chess
import chess.engine
import statistics

depth_to_elo = {
    12: 1400, 13: 1475, 14: 1550, 15: 1625, 16: 1700,
    17: 1775, 18: 1850, 19: 1925, 20: 2000, 21: 2100,
    22: 2200, 23: 2300, 24: 2400, 25: 2500, 26: 2600,
    27: 2700, 28: 2800, 29: 2825, 30: 2850, 31: 2875,
    32: 2900, 33: 2925, 34: 2950, 35: 2975, 36: 3000,
}

def estimated_elo_from_depth(depth):
    d = int(round(depth))
    if d < 12:
        return "1300-"
    if d > 36:
        return "3050+"
    return depth_to_elo[d]

def get_stockfish_infos(board, engine, time_limit):
    info = engine.analyse(board, chess.engine.Limit(time=time_limit))

    # Récupération du score
    score_obj = info["score"].white()
    if score_obj.is_mate():
        score = 100000 if score_obj.mate() > 0 else -100000
    else:
        score = score_obj.score(mate_score=100000)
        if isinstance(score, tuple):
            score = score[0] if isinstance(score[0], (int, float)) else 0
        score = int(score)

    # 🔹 Autres infos intéressantes
    best_move = info.get("pv", [None])[0]
    depth = info.get("depth", None)
    nodes = info.get("nodes", None)

    return score, best_move, depth, nodes


def stability_test(fen, engine, trials=10, time_limits=[0.2, 1, 3, 20]):
    results = {}
    for t in time_limits:
        scores_list = []
        depths_list = []
        nodes_list = []
        best_moves_list = []
        for _ in range(trials):
            board = chess.Board(fen)
            #score = get_stockfish_score(board, engine, time_limit=t)
            score, best_move, depth, nodes = get_stockfish_infos(board, engine, time_limit=t)
            scores_list.append(score)
            depths_list.append(depth)
            nodes_list.append(nodes) 
            best_moves_list.append(best_move)   

        #stats diff, depth, nodes
        avg_depth = statistics.mean(depths_list)
        avg_nodes = statistics.mean(nodes_list)

        #stats score
        max_score = max(scores_list)
        min_score = min(scores_list)
        avg_score = statistics.mean(scores_list)
        elo_est = estimated_elo_from_depth(avg_depth)
        diff_max = max_score - min_score
        avg_diff = statistics.mean([abs(s - avg_score) for s in scores_list])
        

        #stats best move
        main_move = statistics.mode(best_moves_list)
        same_move_count = best_moves_list.count(main_move)
        pct_same_move = (same_move_count / len(best_moves_list)) * 100

        results[t] = {"fen": fen,
                    "score_avg": avg_score, "elo_est": elo_est, 
                    "diff_max": diff_max, "diff_avg": avg_diff, 
                    "depth_avg": avg_depth, "nodes_avg": avg_nodes,
                    "%_same_move": pct_same_move
                    }
    return results

if __name__ == "__main__":
    fen_file = "../Files/games_data.txt"  # ton fichier contenant une FEN par ligne
    fens = [line.strip() for line in open(fen_file, "r", encoding="utf-8") if line.strip()]

    all_results = {}

    # ⚡ Stockfish ouvert une seule fois pour toutes les FEN
    with chess.engine.SimpleEngine.popen_uci("stockfish.exe") as engine:
        with open("../Files/perf_results.txt", "w", encoding="utf-8") as f_out:  # 🔹 fichier de sortie
            for fen_idx, fen in enumerate(fens, 1):
                print(f"\n== FEN {fen_idx}/{len(fens)} ==")
                f_out.write(f"\n== FEN {fen_idx}/{len(fens)} ==\n")  # écrit aussi dans le fichier

                results = stability_test(fen, engine=engine)
                all_results[fen] = results

                for limit, vals in results.items():
                        line = (
                            f"FEN_{fen_idx} {fen} | "
                            f"{limit:.1f}s | "
                            f"score_avg = {round(vals['score_avg'], 0)} | "
                            f"elo_est = {vals['elo_est']} | "
                            f"diff_max = {vals['diff_max']} | "
                            f"diff_avg = {round(vals['diff_avg'], 0)} | "
                            f"depth_avg = {round(vals['depth_avg'], 0)} | "
                            f"nodes_avg = {int(vals['nodes_avg'])} | "
                            f"%_same_move = {round(vals['%_same_move'], 0)}"
                        )
                        print(line)
                        f_out.write(line + "\n")

    print("\n✅ Analyse complète terminée pour toutes les FEN.")

