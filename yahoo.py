#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests


YAHOO_BASE_URL = "https://finance.yahoo.com/quote/"

def fetch_cash_flow(SYMBOL):
    URL = YAHOO_BASE_URL + SYMBOL + "/cash-flow"
    # Fetch page source
    page = requests.get(URL)
    return parse_raw_statement_data(BeautifulSoup(page.content, "html.parser"))


def fetch_balance_sheet(SYMBOL):
    URL = YAHOO_BASE_URL + SYMBOL + "/balance-sheet"
    # Fetch page source
    page = requests.get(URL)
    return parse_raw_statement_data(BeautifulSoup(page.content, "html.parser"))


def fetch_income_statement(SYMBOL):
    URL = YAHOO_BASE_URL + SYMBOL + "/financials"
    # Fetch page source
    page = requests.get(URL)
    return parse_raw_statement_data(BeautifulSoup(page.content, "html.parser"))

 
def parse_raw_statement_data (table_page_source):
    # e.g. MULTIPLIER = 1000 if statement is quoted in thousands
    MULTIPLIER = 1

    # Get the first <section> tag of the table - the meaty stuff
    table = next(table_page_source.find(id="quote-leaf-comp").children)

    # TODO: Extract numeric unit multiplier

    # Exclude the meta info in headers
    statement = next(next(list(table)[2].children).children)

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
    print(fetch_cash_flow("AAPL"))
    print(fetch_balance_sheet("AAPL"))
    print(fetch_income_statement("AAPL"))
