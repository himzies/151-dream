import os
import pandas as pd
import requests
import re

from bs4 import BeautifulSoup
# from src.constants import Constants

def get_card_info(game, set):
    page = requests.get(f'https://yuyu-tei.jp/sell/{game}/s/{set}')

    soup = BeautifulSoup(page.content, 'html.parser')

    all_card_info = soup.findAll('div', attrs={'class': re.compile('card-product position-relative mt-4*')})

    card_nps = {}
    for card_info in all_card_info:
        card_name = card_info.find('h4').text.strip()
        card_num = card_info.find('span').text.strip()
        card_price = card_info.find('strong').text.strip()
        card_status = card_info.find('label').text
        card_status = card_status.replace('\n', '')
        card_status = card_status.replace(' ', '')
        card_status = card_status.replace('在庫', 'remaining')
        card_status = card_status.replace('点', 'pcs')
        card_nps['card_name'] = card_name
        card_nps['card_num'] = card_num
        card_nps['price'] = card_price
        card_nps['status'] = card_status

    return pd.DataFrame(card_nps)


def get_price_stat(game, set, card_num, filepath):
    if not os.path.isfile(filepath):
