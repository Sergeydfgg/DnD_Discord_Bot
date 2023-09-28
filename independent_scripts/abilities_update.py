import pandas as pd
import requests
import json
from googletrans import Translator

monster_table = pd.read_csv('../monsters.csv')
duplicates = list()
dict_to_load = {
    "Атаки": list(),
    "Имунитеты": list(),
    "Сопротивления": list(),
    "Легендарные действия": list(),
    "Способности": list()
}


def load_data():
    for monster in monster_table['Name']:
        cur_monster = list(map(lambda cur_str:
                               cur_str.strip().replace(' ', '-').replace(',', '').lower(), monster.split('(')))
        url = f'https://www.dnd5eapi.co/api/monsters/{cur_monster[0]}'

        headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                 "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
        r = requests.get(url=url, headers=headers)
        if r.status_code == 200:
            data = r.json()
            if data['name'] not in duplicates:
                for action_data in data['actions']:
                    try:
                        dict_to_load['Атаки'].append([action_data['name'], action_data['desc']])
                    except KeyError:
                        pass
                if data['damage_immunities']:
                    for val in data['damage_immunities']:
                        if val not in dict_to_load['Имунитеты']:
                            dict_to_load['Имунитеты'].append(val)
                if data['condition_immunities']:
                    for val in data['condition_immunities']:
                        if val not in dict_to_load['Имунитеты']:
                            dict_to_load['Имунитеты'].append(val)
                if data['damage_resistances']:
                    for val in data['damage_resistances']:
                        if val not in dict_to_load['Сопротивления']:
                            dict_to_load['Сопротивления'].append(val)
                try:
                    for action_data in data['legendary_actions']:
                        try:
                            dict_to_load['Способности'].append([action_data['name'], action_data['desc']])
                        except KeyError:
                            pass
                except KeyError:
                    pass
                try:
                    for action_data in data['special_abilities']:
                        try:
                            dict_to_load['Легендарные действия'].append([action_data['name'], action_data['desc'],
                                                                         action_data['usage']['type'],
                                                                         action_data['usage']['time']])
                        except KeyError:
                            pass
                except KeyError:
                    pass
                duplicates.append(data["name"])


def translate_data():
    translator = Translator()
    for key, val in dict_to_load.items():
        if key in ['Способности', 'Атаки']:
            for ind, text in enumerate(val):
                val[ind] = [translator.translate(text[0], dest='ru').text,
                            translator.translate(text[1], dest='ru').text]
        elif key in ['Имунитеты', 'Сопротивления']:
            for ind, text in enumerate(val):
                val[ind] = translator.translate(text, dest='ru').text
        else:
            for ind, text in enumerate(val):
                val[ind] = [translator.translate(text[0], dest='ru').text,
                            translator.translate(text[1], dest='ru').text,
                            translator.translate(text[2], dest='ru').text,
                            translator.translate(text[3], dest='ru').text]


def sort_data():
    for val in dict_to_load['Атаки']:
        if val[0] == 'Мультиатака':
            val.append(-1)
            continue
        try:
            val.append(int(val[1].split('урон')[1].split()[0]))
        except (IndexError, ValueError):
            val.append(0)
    dict_to_load['Атаки'] = list(sorted(dict_to_load['Атаки'], key=lambda value: value[2]))


def sort_change_data(dict_to_change):
    for val in dict_to_change['Атаки']:
        if val[0] == 'Мультиатака':
            try:
                val.remove(0)
                continue
            except ValueError:
                pass
        if val[2] == 0:
            try:
                if '(' in val[1]:
                    val[2] = int(val[1].split('урон')[1].split('(')[0].split()[-1])
            except (ValueError, IndexError):
                pass
    dict_to_change['Атаки'] = list(sorted(dict_to_change['Атаки'], key=lambda value: value[2]))
    return dict_to_change


def get_cubes(dict_to_change):
    for val in dict_to_change['Атаки']:
        try:
            val.append(f"+{val[1].split('+')[1].split()[0]}")
        except IndexError:
            pass
    return dict_to_change


def update_data():
    with open('../allAbilities.js', 'w', encoding='utf-8') as abilities_file:
        load_data()
        translate_data()
        sort_data()
        js_obj = json.dumps(dict_to_load, indent=4, ensure_ascii=False).encode('utf8')
        abilities_file.write(js_obj.decode())


def change_data():
    with open('../allAbilities.js', 'r', encoding='utf-8') as abilities_file:
        dict_to_change = json.load(abilities_file)
        dict_to_change = get_cubes(dict_to_change)

    with open('../allAbilities.js', 'w', encoding='utf-8') as abilities_file:
        js_obj = json.dumps(dict_to_change, indent=4, ensure_ascii=False).encode('utf8')
        abilities_file.write(js_obj.decode())



change_data()

