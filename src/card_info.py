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

    card_nps = {'card_name': [], 'card_num': [], 'price': [], 'status': []}
    for card_info in all_card_info:
        card_num = card_info.find('span').text.strip()
        card_name = card_info.find('h4').text.strip()
        card_price = card_info.find('strong').text.strip()
        card_status = card_info.find('label').text
        card_status = card_status.replace('\n', '')
        card_status = card_status.replace(' ', '')
        card_status = card_status.replace('在庫', 'remaining')
        card_status = card_status.replace('点', 'pcs')
        card_nps['card_num'].append(card_num)
        card_nps['card_name'].append(card_name)
        card_nps['price'].append(card_price)
        card_nps['status'].append(card_status)
    
    result = pd.DataFrame.from_dict(card_nps)

    return result


def get_price_stat(set, card_num, filepath):
    data = pd.read_csv(filepath)
    print(card_num)
    card = data[data['card_num'] == card_num]
    if set == 'sv02a' and len(card.index) > 1:
        option = input('which version? (n - normal/pb - pokeball/mb - masterball) ')
        card = dream_function(card, option)
    return card.values.flatten().tolist()


def dream_function(card, option):
    if option == 'n':
        return card.iloc[[0]]
    elif option == 'pb':
        return card.iloc[[1]]
    else:
        return card.iloc[[2]]
    

def get_set_links(game):

    result = {}

    if game == 'poc':

        page = requests.get(f'https://yuyu-tei.jp/top/poc')

        soup = BeautifulSoup(page.content, 'html.parser')

        set_sections = soup.find('div', attrs={'id': 'side-sell-target-12'})

        all_links = set_sections.findAll('button', attrs={'id': re.compile(f'side-sell-*')})

        for links in all_links:
            link = links['onclick'].split("'")[1]
            set_name = links.text.replace('\n', '').lstrip()
            set_code = link.replace('https://yuyu-tei.jp/sell/poc/s/', '')
            result[set_code] = {'set_name': set_name, 'link': link}

    elif game == 'ws':

        page = requests.get(f'https://yuyu-tei.jp/top/ws')

        soup = BeautifulSoup(page.content, 'html.parser')

        set_sections = soup.find('div', attrs={'id': 'side-sell-target-12'})

        all_links = set_sections.findAll('a', attrs={'id': re.compile(f'side-sell-*')})

        for links in all_links:
            link = links['href']
            set_name = links.text.replace('\n', '').lstrip()
            set_code = link.replace('https://yuyu-tei.jp/sell/ws/s/', '')
            result[set_code] = {'set_name': set_name, 'link': link}
    
    return result