# Currency Rates Fetcher
Simple ETL process to fetch, store and display currency rates. 
Makes use of the [exchangerates](https://exchangeratesapi.io/) API and uses python's built-in module `sqlite3` to create and connect to a simple [SQLite3](https://www.sqlite.org/docs.html) database. 

*Check the API documentation [here](https://exchangeratesapi.io/documentation/).*
*Check the `sqlite3` module documentation [here](https://docs.python.org/3/library/sqlite3.html)*

## About the Scripts
* `get_rates.py`
    * Connection to database and storage of fetched data.
* `utils.py`
    * Logic for API authentication and request. Also Holds data transformation procedures.
* `query_db.py`
    * Script to query database using python's built-in module.
* `export.py`
    * Script used by PowerBI to ingest or refresh dataset.

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
python3 database.py
```