import streamlit as st
import chess
import chess.svg
import pandas as pd
import streamlit.components.v1 as components


def e_streamlit_full():

    # --- Configuration de la page ---
    st.set_page_config(page_title="Analyse FEN", layout="wide")
    
    # --- Chargement du CSV ---
    CSV_PATH = "../Files/worst_moves.csv"
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
    if turn.strip().lower() == "b":
        board.turn = chess.BLACK
    else:
        board.turn = chess.WHITE

    # --- Flèches ---
    my_arrow = stock_arrow = None
    if my_move:
        my_move_obj = board.parse_san(my_move)
        my_arrow = chess.svg.Arrow(my_move_obj.from_square, my_move_obj.to_square, color="#cc0000")
    if stockfish_move:
        stock_move_obj = board.parse_san(stockfish_move)
        stock_arrow = chess.svg.Arrow(stock_move_obj.from_square, stock_move_obj.to_square, color="#00cc44")

    # --- Plateau avec flèches ---
    arrows = []
    if my_arrow:
        arrows.append(my_arrow)
    if stock_arrow:
        arrows.append(stock_arrow)

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
