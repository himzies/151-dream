import json

from src.card_info import get_set_links

class Constants:
    en_pkmn_names = json.load(open('data/pkmn_names/en.json'))
    jp_pkmn_names = json.load(open('data/pkmn_names/ja.json'))
    en_jp_pkmn_name_dict = zip(jp_pkmn_names, en_pkmn_names)
    pkmn_set_links = get_set_links('poc')
    ws_set_links = get_set_links('ws')