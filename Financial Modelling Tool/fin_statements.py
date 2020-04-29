#!/usr/local/bin/python3
""" We call the Financial Modelling Prep API to get some of our data. We use the requests library to
    call the API and return the requested data
"""

import json
import requests
import pandas as pd


def get_jsonparsed_data(ticker, data):
    """
    Receive the content of ``url``, parse it as JSON and return the object.

    Parameters
    ----------
    ticker: Ticker of the stock to get data for
    data: Data to retrieve from the API (historical-price-full, income-statement, etc)
        Different data can be found here: https://financialmodelingprep.com/developer/docs/

    Returns
    -------
    dict
    """
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"
    }

    url = f"https://financialmodelingprep.com/api/v3/{data}/{ticker}"

    fin_statements = ['income-statement',
                      'balance-sheet-statement', 'cash-flow-statement']

    if data in fin_statements:
        url = f"https://financialmodelingprep.com/api/v3/financials/{data}/{ticker}"

    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'

    response_data = json.loads(response.content)

    if data in fin_statements:
        df = pd.DataFrame.from_dict(response_data['financials']).T
        df.columns = df.loc['date']

        # Remove the date row since we made it the column headings
        return df.drop('date')

    return response_data


if __name__ == '__main__':

    data = get_jsonparsed_data('AAPL', 'income-statement')
    data1 = get_jsonparsed_data('AAPL', 'company/rating')
