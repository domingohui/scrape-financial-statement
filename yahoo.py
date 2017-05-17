#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests
from . import csv_output

YAHOO_BASE_URL = "https://finance.yahoo.com/quote/"

def fetch_cash_flow(SYMBOL):
    URL = YAHOO_BASE_URL + SYMBOL + "/cash-flow"
    # Fetch page source
    page = requests.get(URL)
    return SYMBOL, "Cash Flow", parse_raw_statement_data(page.content)


def fetch_balance_sheet(SYMBOL):
    URL = YAHOO_BASE_URL + SYMBOL + "/balance-sheet"
    # Fetch page source
    page = requests.get(URL)
    return parse_raw_statement_data(page.content)


def fetch_income_statement(SYMBOL):
    URL = YAHOO_BASE_URL + SYMBOL + "/financials"
    # Fetch page source
    page = requests.get(URL)
    return parse_raw_statement_data(page.content)


def infer_dollar_multiplier(string):
    '''
    string: string

    returns: int
    '''

    if "thousands" in string:
        return 1000
    if "millions" in string:
        return 1000000
    return 1
 
def parse_raw_statement_data (table_page_source):
    '''
    parse raw HTML
    table_page_source: string

    returns: [ [...], ... ]
    '''
    soup = BeautifulSoup(table_page_source, "html.parser")

    # Get the first <section> of the table - the meaty stuff
    table = list(next(soup.find(id="quote-leaf-comp").children))

    # Extract dollar unit multiplier
    metadata = table[1]
    # e.g. MULTIPLIER = 1000 if statement is quoted in thousands
    MULTIPLIER = max(infer_dollar_multiplier(s) for s in metadata.strings)

    # Exclude the meta info in headers
    statement = next(next(table[2].children).children)

    # Raw data in dollar value
    # Extract and work with it later
    # 2d list
    data = []

    for row in statement.children:
        # Extract info
        data.append([])
        for entry in row.children:
            # For each column entry
            value = entry.string
            # Try to parse numeric value
            try:
                # Strip comma
                value = float(value.replace(",", ""))
                value = value * MULTIPLIER
            except ValueError:
                # Not a numeric value
                pass
            data[-1].append(value) 

    return data


if __name__ == "__main__":
    to_csv(fetch_cash_flow("AAPL"))
    '''
    print(fetch_cash_flow("AAPL"))
    print(fetch_balance_sheet("AAPL"))
    print(fetch_income_statement("AAPL"))
    '''
