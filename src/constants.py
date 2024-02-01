import json

class Constants:
    en_pkmn_names = json.load(open('data/pkmn_names/en.json'))
    jp_pkmn_names = json.load(open('data/pkmn_names/ja.json'))
    en_jp_pkmn_name_dict = zip(jp_pkmn_names, en_pkmn_names)