import pandas as pd
import requests
import json

monster_table = pd.read_csv('../monsters.csv')
duplicates = list()

for monster in monster_table['Name']:
    cur_monster = list(map(lambda cur_str:
                           cur_str.strip().replace(' ', '-').replace(',', '').lower(), monster.split('(')))
    url = f'https://www.dnd5eapi.co/api/monsters/{cur_monster[0]}'

    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
    r = requests.get(url=url, headers=headers)
    if r.status_code == 200:
        with open('../allMonsters.js', 'a') as monster_file:
            data = r.json()
            if data['name'] not in duplicates:
                text_to_append = f'"{data["name"]}": ' + '{\n'
                for action in data['actions']:
                    try:
                        if action['damage']:
                            text_to_append += f'"{action["name"]}":["{action["attack_bonus"]}"'
                            for damage_params in action['damage']:
                                text_to_append += f', "{damage_params["damage_dice"]}"'
                            text_to_append += '],\n'
                    except KeyError:
                        pass
                text_to_append += f'"hits":"{data["hit_points"]}",\n'
                text_to_append += f'"ac":"{data["armor_class"][0]["value"]}"'
                text_to_append += '\n},\n'
                duplicates.append(data["name"])
                monster_file.write(text_to_append)
