#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests

'''
page = requests.get("https://finance.yahoo.com/quote/AAPL/financials")

soup = BeautifulSoup(page.content)
'''
with open('page_source') as fp:
    soup = BeautifulSoup(fp)

# First <section> tag of the table - the meaty stuff
table = next(soup.find(id="quote-leaf-comp").children)

# TODO: Extract meta info


# Exclude the headers
statement = next(next(list(table)[2].children).children)

# Raw data
# Extract and work with it later
# 2d list
data = []

for row in statement.children:
    # Extract info
    data.append([])
    for entry in row.children:
        # For each column entry
        value = entry.string
        try:
            # Strip comma
            value = float(value.replace(",", ""))
        except ValueError:
            pass
        data[-1].append(value) 

for row in data:
    print(row)
