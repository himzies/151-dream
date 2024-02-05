import os

from datetime import date
from src.card_info import *
# from src.constants import Constants

if __name__ == '__main__':
    today = date.today()
    again = True
    get_pkmn_links(today)
    get_ws_links(today)
    while again:
        game = input('what game? (ws - weiss schwarz/poc - pokemon): ').lower()
        get_set_names(game, today)
        set = input('which set does it belong to? ').lower()
        if game == 'ws':
            set = input('which set does it belong to? ').lower() + '#kana'
        card_num = str(input('what is the number at the bottom of the card? ')).upper()
        link = link_retrieval(game, set, today)
        set_info = get_set_info(game, set, today)
        price_stat = get_price_stat(game, set, card_num, today)
        print(f'{price_stat[1]} ({price_stat[2]}) costs {price_stat[3]}, {price_stat[4]}')
        prompt = input('wwould you like to search for another card? (y - yes/n - no): ').lower()
        if prompt == 'n':
            again = False