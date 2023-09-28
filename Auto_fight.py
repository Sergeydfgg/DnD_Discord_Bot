import json
from random import randint

with open('Data/allMonsters.js', encoding='utf-8') as lib:
    monster_data = json.load(lib)

with open('Data/allPlayers.js', encoding='utf-8') as lib:
    players_data = json.load(lib)


class Player:
    def __init__(self, player_name):
        self.name = player_name
        self.attack = list(players_data[player_name].values())[0]
        self.hits = int(players_data[player_name]['hits'])
        self.armor_class = int(players_data[player_name]['ac'])

    @staticmethod
    def _calculate_random_damage(damage):
        damage_list = damage.split('+')
        if len(damage_list) > 1:
            damage_dice = damage_list[0].split('d')
            return sum([randint(1, int(damage_dice[1])) for _ in range(0, int(damage_dice[0]))]) + int(damage_list[1])
        else:
            damage_dice = damage.split('d')
            return sum([randint(1, int(damage_dice[1])) for _ in range(0, int(damage_dice[0]))])

    def make_attack(self):
        penetration = randint(1, 20) + int(self.attack[0])
        damage = sum([self._calculate_random_damage(val) for val in self.attack[1::]])
        return (penetration, damage) if penetration < 20 else (penetration, damage * 2)

    def get_damage(self, attack_pair):
        if self.armor_class < attack_pair[0]:
            self.hits -= attack_pair[1]


class Enemy:
    def __init__(self, monster_name):
        self.name = monster_name
        self.armor_class = int(monster_data[monster_name]['ac'])
        self.hits = int(monster_data[monster_name]['hits'])
        self.attack_key = self._calculate_attack()

    def _calculate_attack(self):
        cur_monster = monster_data[self.name]
        possible_attacks = [key for key in cur_monster.keys() if key not in ['hits', 'ac']]
        attack_pairs = [(attack, sum([self._calculate_damage(val)
                                      for val in cur_monster[attack][1::]])) for attack in possible_attacks]
        return max(attack_pairs, key=lambda pair: pair[1])[0]

    @staticmethod
    def _calculate_damage(damage):
        damage_list = damage.split('+')
        if len(damage_list) > 1:
            damage_dice = damage_list[0].split('d')
            return int(damage_dice[0])*int(damage_dice[1]) + int(damage_list[1])
        else:
            damage_dice = damage.split('d')
            return int(damage_dice[0]) * int(damage_dice[1])

    @staticmethod
    def _calculate_random_damage(damage):
        damage_list = damage.split('+')
        if len(damage_list) > 1:
            damage_dice = damage_list[0].split('d')
            return sum([randint(1, int(damage_dice[1])) for _ in range(0, int(damage_dice[0]))]) + int(damage_list[1])
        else:
            damage_dice = damage.split('d')
            return sum([randint(1, int(damage_dice[1])) for _ in range(0, int(damage_dice[0]))])

    def make_attack(self):
        cur_attack = monster_data[self.name][self.attack_key]
        penetration = randint(1, 20) + int(cur_attack[0])
        damage = sum([self._calculate_random_damage(val) for val in cur_attack[1::]])
        return (penetration, damage) if penetration < 20 else (penetration, damage*2)

    def get_damage(self, attack_pair):
        if self.armor_class < attack_pair[0]:
            self.hits -= attack_pair[1]
