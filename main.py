import os

from datetime import date
from src.card_info import get_card_info, get_price_stat
# from src.constants import Constants

if __name__ == '__main__':
    function = input('what would you like to do today? (pc - price check/pt - price track): ')
    game = input('what game? (ws - weiss schwarz/poc - pokemon): ')
    set = input('which set does it belong to? ')
    today = date.today()
    if not os.path.exists(f'data/{game}/{str(today)}'):
        os.makedirs(f'data/{game}/{str(today)}')
    filepath = f'data/{game}/{str(today)}/{set}.csv'
    if function == 'pt':
        if os.path.isfile(filepath):
            print(f'price track already done for {set} today')
        else:
            get_card_info(game, set).to_csv(filepath)
    elif function == 'pc':
        card_num = str(input('what is the number at the bottom of the card? '))
        if not os.path.isfile(filepath):
            get_card_info(game, set).to_csv(filepath)
        price_stat = get_price_stat(set, card_num, filepath)
        print(f'{price_stat[1]} ({price_stat[2]}) costs {price_stat[3]}, {price_stat[4]}')