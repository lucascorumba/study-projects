# Currency Rates Fetcher
Simple ETL process to fetch, store and display currency rates. 
Makes use of the [exchangerates API](https://exchangeratesapi.io/) and uses python's built-in module `sqlite3` to create and connect to a simple [SQLite3](https://www.sqlite.org/docs.html) database.

*Check the API documentation [here](https://exchangeratesapi.io/documentation/).*
*Check the `sqlite3` module documentation [here](https://docs.python.org/3/library/sqlite3.html)*

## About the Scripts
* `get_rates.py`
    * Connection to database and storage of fetched data.
* `utils.py`
    * Holds the logic for API authentication and request. Also performs some simple data transformation procedures.
* `query_db.py`
    * Script to query database using python's built-in module.
* `export.py`
    * Script used by PowerBI to ingest or refresh dataset.
    In practice it functions pretty much the same as `query_db.py`, only it does not filter any data (`SELECT * ...`) and produces a `pandas.DataFrame` that is consumed by PowerBI.
    * As PowerBI demands `pandas` and `matplotlib` modules to be imported in order to run a python script, both of them need to be installed. 
    Another solution is to install the [SQLite ODBC driver](http://www.ch-werner.de/sqliteodbc/) and connect PowerBI directly to the database.
    * If using a `venv`, pay attention while setting python path. PowerBI should be provided the `.../venv/Scripts` folder instead of the global install, the former holds the `venv` interpreter.
* `schedule.py`
    * Very simple "scheduler", only relies on `time`and `datetime` modules. 
    Prompts for number of fetches to be executes as well as hours and minutes intervals. Keeps process sleeping for 45 minutes and then checks if queued scheduled time is already reached. If so, it triggers `get_rates.py` to get and store API data.

## Requirements
It's recommended to not install required packages globally, but locally under a project subfolder using `venv`: 
```
python3 -m venv venv-name

# Windows
venv-name\Scripts\activate.bat    # cmd
venv-name\Scripts\activate.ps1    # PowerShell

# Unix
source venv-name/bin/activate
```
Libraries:
```
pip install requests

# Pandas and matplotlib are needed to export data to PowerBI through python script ingestion
pip install pandas
pip install matplotlib
```

## Usage
```
# To fetch latest rates
python3 get_rates.py

# To query the database through .py script
python3 query_db.py

# To schedule fetches
python3 schedule.py
```