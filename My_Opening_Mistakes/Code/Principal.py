import streamlit as st
import pandas as pd
from a_Extraction import a_extraction
from b_Main_file import b_main_file
from c_Cleaning import c_cleaning
from d_Read_sql import d_read_sql
from e_Streamlit_full import e_streamlit_full
import os

# --- Création du dossier Files si nécessaire ---
os.makedirs("Files", exist_ok=True)

# --- Chemins vers les fichiers ---
fen_file_path = "Files/games_fen.txt"

# --- Texte explicatif ---
st.markdown("## ♟️ Your mistakes analysis")
st.markdown("""
Upload a PGN file (downloadable from Lichess or Chess.com).  
This program identifies recurring positions where the difference between Stockfish's evaluation and your move's evaluation is the largest.
You can then see a tab with all analysed positions, and select each position to visualize it, with the Stockfish evaluations.

We only analyse the moves 3 to 15 of each game, to focus on the opening phase, and show the positions repeated at least 2 times
with at least 0.3 pawn difference between your move and Stockfish's recommendation.

⚠️ Note: The processing time is quite long : ~1 minutes 20 seconds per game, so ~2 hours 15 minutes for 100 games. 
""")
st.write("")  # espacement

# --- Upload du fichier PGN ---
uploaded_file = st.file_uploader("Upload a PGN file", type=["pgn"])

if uploaded_file is not None:
    # --- Extraction FENs (une seule fois) ---
    if not os.path.exists(fen_file_path):
        a_extraction(uploaded_file, min_move=3, max_move=15, output_path=fen_file_path)
    
    # --- Appel des autres traitements ---
    b_main_file()
    c_cleaning()
    d_read_sql()
    e_streamlit_full()
