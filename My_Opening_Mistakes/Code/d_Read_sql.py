import duckdb

def d_read_sql():
    con = duckdb.connect()
    df = con.execute(open("d_Analysis.sql").read()).df()
    print(df.head())