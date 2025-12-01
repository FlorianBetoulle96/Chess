import duckdb
import os

# Création du dossier Files si nécessaire
os.makedirs("Files", exist_ok=True)

def d_read_sql():
    con = duckdb.connect(database=':memory:')  # base en mémoire

    query = """
    COPY (
        WITH fens_final AS (
            SELECT 
                column0 AS fen,
                column1 AS b_or_w,
                column2 AS move_nb,
                column3 AS stck_move,
                ROUND(CAST(column4 AS FLOAT) / 0.2) * 0.2 AS stck_eval,
                column5 AS my_move,
                ROUND(CAST(column6 AS FLOAT) / 0.2) * 0.2 AS my_eval,
                CASE WHEN column1 = 'w' THEN (stck_eval - my_eval) ELSE (my_eval - stck_eval) END AS diff_eval
            FROM read_csv_auto('Files/final_cleaned.csv', delim=',', header=False, null_padding=True)
        ),
        fens_grouped AS (
            SELECT 
                fen,
                b_or_w,
                ANY_VALUE(stck_move) AS stck_move,
                AVG(stck_eval) AS stck_eval,
                ANY_VALUE(my_move) AS my_move,
                AVG(my_eval) AS my_eval,
                AVG(diff_eval) AS diff_eval,
                COUNT(*) AS counter
            FROM fens_final
            GROUP BY fen, b_or_w
        ),
        worst_moves AS (
            SELECT fen, b_or_w,
                stck_move,
                ROUND(stck_eval,1) AS stck_eval,
                my_move,
                ROUND(my_eval,1) AS my_eval,
                ROUND(diff_eval,1) AS diff_eval,
                counter
            FROM fens_grouped
            WHERE 1=1
                AND counter > 1
                AND stck_move != my_move
                AND diff_eval > 200
            ORDER BY counter DESC
        )
        SELECT * FROM worst_moves
    ) TO 'Files/worst_moves.csv' (HEADER, DELIMITER ',');
    """

    con.execute(query)
    con.close()
    print("✅ worst_moves.csv créé dans Files/")
