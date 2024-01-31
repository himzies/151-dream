import pandas as pd
import requests
import re

from bs4 import BeautifulSoup

page = requests.get('https://yuyu-tei.jp/sell/poc/s/sv02a')

soup = BeautifulSoup(page.content, 'html.parser')

all_card_info = soup.findAll('div', attrs={'class': re.compile('card-product position-relative mt-4*')})

card_nps = {}
for card_info in all_card_info:
    card_name = card_info.find('h4').text.strip()
    card_price = card_info.find('strong').text.strip()
    card_status = card_info.find('label').text
    card_status = card_status.replace('\n', '')
    card_status = card_status.replace(' ', '')
    card_nps[card_name] = {'price': card_price, 'status': card_status}

print(card_nps)