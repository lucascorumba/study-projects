import pandas as pd
import sqlite3

# Must provide absolute path to database file as argument to .connect()
conn = sqlite3.connect("")
cur = conn.cursor()

sql = "SELECT * FROM brl_prices;"

res = cur.execute(sql)

df = pd.DataFrame.from_records(res.fetchall(), columns=["timestamp", "symbol", "price"])
conn.close()
print(df)