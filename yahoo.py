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

for row in statement.children:
    # extract info
#//*[@id="quote-leaf-comp"]/section/div[3]/table/tbody/tr[1]/td[1]/span
