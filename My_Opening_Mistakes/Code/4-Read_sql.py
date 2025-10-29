import duckdb

con = duckdb.connect()
df = con.execute(open("4-Analysis.sql").read()).df()
print(df.head())