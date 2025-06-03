import sqlite3
import utils


def runner(db_path):
    """
    Uses utils.py methods to make API call and store produced data into the database.
    Receives filepath of database file as input.
    """
    print("Fetching rates")
    # Makes request to the API
    response = utils.get_rates()

    print("Connecting to database")
    # Connects to the database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # Create table on the first run, otherwise, ignore
    cur.execute(
        "CREATE TABLE IF NOT EXISTS \
        brl_prices(timestamp INTEGER, symbol TEXT, price NUMERIC);"
    )

    # Data transfomation - calculates the price in BRL of all fetched symbols
    rates = utils.calculate_brl(response)

    # Inserts produced data into the database
    timestamp = response.get("timestamp")
    for rate in rates:
        cur.execute(
            "INSERT INTO brl_prices VALUES(?, ?, ?);", 
            (timestamp, rate[0], rate[1])
        )
    print("Storing records")
    conn.commit()

    print("Closing database connection")
    conn.close()
    # Returns list of tuples with last rates for selected symbols -> ('symbol', 0.00)
    return rates


def simple_report(rates):
    """
    Prints a simple report with last fetched prices for the selected symbols.
    Symbol: 0.000 BRL
    """
    fast_check = ("USD", "EUR", "BTC")
    print("Latest prices:")
    for item in rates:
        if item[0] in fast_check:
            print(f"{item[0]}: {round(item[1], 3)} BRL")


if __name__ == "__main__":
    rates = runner("currency.db")
    simple_report(rates)