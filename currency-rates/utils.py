import requests

# API handling

def get_key(file_path):
    """
    Gets API key from .txt file in the same directory.
    """
    with open(file_path, encoding="utf-8") as f:
        return f.readline()

def get_params(base_currency, get_symbols):
    """
    Takes in one base currency and a sequence of symbols (USR, BRL, ...) 
    to be compared against base currency.
    """
    return {
        "access_key": get_key("credentials.txt"),
        "base": base_currency,
        "symbols": ",".join(get_symbols)
    }

def endpoint_latest(params):
    """
    Makes request to 'latest' exchangerates API endpoint. Returns response object.
    """
    response = requests.get("https://api.exchangeratesapi.io/v1/latest", params=params)
    print(f"Status: {response.status_code}") 
    if response.status_code != 200:
        raise Exception(
            f"Request error: {response.status_code}\n{response.text}"
        )
    return response

def get_rates():
    """
    Makes call to 'latest' endpoint and get symbols rate.
    The free plan of this API just allows use of "EUR" as base currency. 
    """
    #params = get_params("EUR", ("BRL", "USD", "ARS", "AUD", "BTC", "GBP", "HKD", "JPY", "XAU", "XAG", "CNH"))
    params = get_params("EUR", ("BRL", "USD", "BTC", "GBP", "XAU", "XAG"))
    response = endpoint_latest(params)
    return response.json()


# Data transformation

def calculate_brl(response):
    """
    Gets API response and calculate all currency prices in BRL. -> 1 USD costs 5.67 BRL; 1 EUR costs 6.29 BRL;
    Outputs a list of tuples in the format: (symbol, price)
    """
    brl_base = list()
    rates = response.get("rates")
    brl_eur_rate = 1 / rates.get("BRL")
    for symbol in rates:
        if symbol == "BRL":
            brl_base.append(("EUR", rates.get("BRL")))
            continue
        calc = brl_eur_rate * rates.get(symbol)
        brl_base.append((symbol, round((1 / calc), 6)))
    return brl_base

