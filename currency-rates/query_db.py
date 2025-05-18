import sqlite3

conn = sqlite3.connect("currency.db")
cur = conn.cursor()

# Query statement
sql = "SELECT symbol, price FROM brl_prices WHERE symbol = 'USD' ORDER BY timestamp DESC;"

res = cur.execute(sql)
#conn.commit()

for row in res:
    print(row)

conn.close()