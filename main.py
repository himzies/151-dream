import os

from datetime import date
from src.card_info import *
# from src.constants import Constants

if __name__ == '__main__':
    today = date.today()
    again = False # change here for non-automation
    if not os.path.isfile(f'data/poc/{str(today)}/poc_links.csv'):
        pkmn_links = get_pkmn_links(today)
    else:
        pkmn_links = pd.read_csv(f'data/poc/{str(today)}/poc_links.csv')
    if not os.path.isfile(f'data/ws/{str(today)}/ws_links.csv'):
        ws_links = get_ws_links(today)
    else:
        ws_links =pd.read_csv(f'data/ws/{str(today)}/ws_links.csv')
    poc_sets = pkmn_links.set_code
    ws_sets = ws_links.set_code
    for set in poc_sets:
        set_info = get_set_info('poc', set, today)
    for set in ws_sets:
        set_info = get_set_info('ws', set, today)
    # while again:
    #     game = input('what game? (ws - weiss schwarz/poc - pokemon): ').lower()
    #     get_set_names(game, today)
    #     if game == 'ws':
    #         set = input('which set does it belong to? ').lower() + '#kana'
    #     else:
    #         set = input('which set does it belong to? ').lower()
    #     card_num = str(input('what is the number at the bottom of the card? ')).upper()
    #     link = link_retrieval(game, set, today)
    #     set_info = get_set_info(game, set, today)
    #     price_stat = get_price_stat(game, set, card_num, today)
    #     print(f'{price_stat[1]} ({price_stat[2]}) costs {price_stat[3]}, {price_stat[4]}')
    #     prompt = input('wwould you like to search for another card? (y - yes/n - no): ').lower()
    #     if prompt == 'n':
    #         again = False