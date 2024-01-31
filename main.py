import os

from datetime import date
from src.card_info import get_card_info, get_price_stat
from src.constants import Constants

if __name__ == '__main__':
    function = input('what would you like to do today? (pc - price check/pt - price track): ')
    game = input('what game? (ws - weiss schwarz/poc - pokemon): ')
    set = input('which set does it belong to? ')
    today = date.today()
    filepath = f'data/{str(today)/{game}/{set}.csv}'
    if function == 'pt':
        if os.path.isfile(filepath):
            print(f'price track already done for {set} today')
        else:
            os.makedirs(filepath)
            get_card_info(game, set).to_csv(filepath)
    elif function == 'pc':
        if os.path.isfile(filepath):
            card_name = input('what is the name of the card? ')
            price_stat = get_price_stat(card_name, filepath)
            print(f'{card_name} costs {price_stat[0]}, {price_stat[1]}')