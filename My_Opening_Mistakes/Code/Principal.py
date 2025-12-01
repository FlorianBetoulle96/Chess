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
image_path = os.path.join(os.path.dirname(__file__), "Image.png")

# --- Texte explicatif ---
st.markdown("## ♟️ Your opening mistakes")
st.markdown("""
This program identifies recurring positions where the difference between Stockfish's evaluation and your move's evaluation is the largest. (from moves 3 to 15)

You will see all analysed positions and visualize them on a board.
            
            

-> Upload a PGN file (downloadable from Chess.com or Lichess.com)

⚠️ Note: The processing time is quite long : ~1m20 per game ⇒ ~2h15 for 100 games 

""")
st.image(image_path, caption="Voici une image", use_column_width=True)

# --- Upload du fichier PGN ---
uploaded_file = st.file_uploader("", type=["pgn"])

if uploaded_file is not None:
    # --- Extraction FENs (une seule fois) ---
    if not os.path.exists(fen_file_path):
        a_extraction(uploaded_file, min_move=3, max_move=15, output_path=fen_file_path)
    
    # --- Appel des autres traitements ---
    b_main_file()
    c_cleaning()
    d_read_sql()
    e_streamlit_full()