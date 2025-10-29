import duckdb

con = duckdb.connect()
df = con.execute(open("3-Analysis.sql").read()).df()
print(df.head())