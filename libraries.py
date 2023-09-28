import json

music_data = dict()
map_data = dict()
avatar_data = dict()


def load_data():
    global music_data, map_data, avatar_data
    with open('Data/musicLib.js', 'r', encoding='utf-8') as music_file:
        music_data = json.load(music_file)


def show_music_categories():
    return tuple(music_data.keys())


def get_category_data(category: str):
    try:
        return tuple(music_data[category])
    except KeyError:
        return 'Такой категории нет или она пуста'
