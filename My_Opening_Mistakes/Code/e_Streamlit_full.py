import streamlit as st
import chess
import chess.svg
import pandas as pd
import streamlit.components.v1 as components
import os

def e_streamlit_full():
    # --- Création du dossier Files si nécessaire ---
    os.makedirs("Files", exist_ok=True)

    # --- Configuration de la page ---
    st.set_page_config(page_title="Analyse FEN", layout="wide")
    
    # --- Chargement du CSV ---
    CSV_PATH = "Files/worst_moves.csv"
    if not os.path.exists(CSV_PATH):
        st.warning("Le fichier worst_moves.csv n'a pas encore été généré.")
        return
    
    df = pd.read_csv(CSV_PATH, header=0, encoding="utf-8-sig", sep=",", skipinitialspace=True)

    # --- Ajout d'une colonne visible ---
    df.reset_index(inplace=True)
    df.rename(columns={"index": "Ligne"}, inplace=True)

    # --- Tableau + sélecteur ---
    st.dataframe(df, width='content')

    selected_index = st.selectbox(
        "Position :",
        df["Ligne"],
        format_func=lambda i: f"Position {i}"
    )

    # --- Données de la ligne sélectionnée ---
    row = df.loc[df["Ligne"] == selected_index].iloc[0]
    fen = row["fen"]
    turn = row["b_or_w"]
    my_move = row["my_move"]
    my_eval = row["my_eval"]
    stockfish_move = row["stck_move"]
    stockfish_eval = row["stck_eval"]
    diff_eval = row["diff_eval"]
    counter = row["counter"]

    # --- Création du plateau ---
    board = chess.Board(fen)
    board.turn = chess.WHITE if turn.strip().lower() == "w" else chess.BLACK

    # --- Flèches ---
    arrows = []
    if my_move:
        try:
            my_move_obj = board.parse_san(my_move)
            arrows.append(chess.svg.Arrow(my_move_obj.from_square, my_move_obj.to_square, color="#cc0000"))
        except:
            pass
    if stockfish_move:
        try:
            stock_move_obj = board.parse_san(stockfish_move)
            arrows.append(chess.svg.Arrow(stock_move_obj.from_square, stock_move_obj.to_square, color="#00cc44"))
        except:
            pass

    # --- Plateau avec flèches ---
    svg_code = chess.svg.board(
        board=board,
        size=600,
        flipped=(turn.strip().lower() == "b"),
        arrows=arrows
    )

    # --- Affichage des coups ---
    st.markdown(f"""
    <div style="text-align:center; font-size:18px; margin-top:10px;">
        <span style="color:#cc0000;">Your move: {my_move} (eval: {round(0.01*my_eval,2)})</span> &nbsp;&nbsp;|&nbsp;&nbsp;
        <span style="color:#00cc44;">Best move: {stockfish_move} (eval: {round(0.01*stockfish_eval,2)})</span> &nbsp;&nbsp;|&nbsp;&nbsp;
        <span style="color:#000000;">Frequency: {counter} times</span>
    </div>
    """, unsafe_allow_html=True)

    # --- Affichage du plateau ---
    components.html(f"""
    <div style='display: flex; justify-content: center;'>
        {svg_code}
    </div>
    """, height=650)
