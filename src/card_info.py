import os
import pandas as pd
import requests
import re

from bs4 import BeautifulSoup
from datetime import date
# from src.constants import Constants

def get_set_info(game, set, date):

    page = requests.get(f'https://yuyu-tei.jp/sell/{game}/s/{set}')

    soup = BeautifulSoup(page.content, 'html.parser')

    all_card_info = soup.findAll('div', attrs={'class': re.compile('card-product position-relative mt-4*')})

    result = pd.DataFrame({'card_name': [], 'card_num': [], 'price': [], 'status': []})

    for card_info in all_card_info:
        card_num = card_info.find('span').text.strip().upper()
        card_name = card_info.find('h4').text.strip()
        card_price = card_info.find('strong').text.strip()
        card_status = card_info.find('label').text
        card_status = card_status.replace('\n', '')
        card_status = card_status.replace(' ', '')
        card_status = card_status.replace('在庫', 'remaining')
        card_status = card_status.replace('点', 'pcs')
        new_row = pd.DataFrame({'card_name': [card_name], 'card_num': [card_num], 'price': [card_price], 'status': [card_status]})
        result = pd.concat([result, new_row])
    
    result.to_csv(f'data/{game}/{str(date)}/{set}.csv')

    return result


def get_price_stat(game, set, card_num, date):

    data = pd.read_csv(f'data/{game}/{str(date)}/{set}.csv')

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
    

def get_pkmn_links(date):

    if not os.path.exists(f'data/poc/{str(date)}'):
        os.makedirs(f'data/poc/{str(date)}')

    result = pd.DataFrame({'set_code': [], 'set_name': [], 'set_link': []})

    page = requests.get(f'https://yuyu-tei.jp/top/poc')

    soup = BeautifulSoup(page.content, 'html.parser')

    set_sections = soup.find('div', attrs={'id': 'side-sell-target-12'})

    all_links = set_sections.findAll('button', attrs={'id': re.compile(f'side-sell-*')})

    for links in all_links:
        link = links['onclick'].split("'")[1].strip()
        set_name = links.text.strip()
        set_code = link.replace('https://yuyu-tei.jp/sell/poc/s/', '')
        new_row = pd.DataFrame({'set_code': [set_code], 'set_name': [set_name], 'set_link': [link]})
        result = pd.concat([result, new_row])
    
    result = result.reset_index()

    result.to_csv(f'data/poc/{str(date)}/poc_links.csv')
    
    return result


def get_ws_links(date):

    if not os.path.exists(f'data/ws/{str(date)}'):
        os.makedirs(f'data/ws/{str(date)}')

    result = pd.DataFrame({'set_code': [], 'set_name': [], 'set_link': []})

    page = requests.get(f'https://yuyu-tei.jp/top/ws')

    soup = BeautifulSoup(page.content, 'html.parser')

    set_sections = soup.find('div', attrs={'id': 'side-sell-target-12'})

    all_links = set_sections.findAll('a', attrs={'id': re.compile(f'side-sell-*')})

    for links in all_links:
        link = links['href'].strip()
        set_name = links.text.strip()
        set_code = link.replace('https://yuyu-tei.jp/sell/ws/s/', '').replace('#kana', '')
        new_row = pd.DataFrame({'set_code': [set_code], 'set_name': [set_name], 'set_link': [link]})
        result = pd.concat([result, new_row])

    result = result.reset_index()
    
    result.to_csv(f'data/ws/{str(date)}/ws_links.csv')
    
    return result


def link_retrieval(game, set, date):
    filepath = f'data/{game}/{str(date)}/{game}_links.csv'
    df = pd.read_csv(filepath)
    target = df[df['set_code'] == set]
    return target['set_link']


def get_set_names(game, date):
    filepath = f'data/{game}/{str(date)}/{game}_links.csv'
    df = pd.read_csv(filepath)
    print(df[['set_code', 'set_name']].to_markdown())