import json
from random import randint, choice
from math import ceil, floor

with open('Data/creature_settings.js', 'r', encoding='utf-8') as creatures_file:
    creatures_settings = json.load(creatures_file)

with open('Data/spells_settings.js', 'r', encoding='utf-8') as spells_file:
    spells_settings = json.load(spells_file)

with open('Data/allAbilities.js', 'r', encoding='utf-8') as abilities_file:
    abilities_dict = json.load(abilities_file)


class Creature:
    difficult_to_damage = {
        "1": (5, 10),
        "2": (8, 16),
        "3": (16, 30),
        "4": (30, 40),
        "5": (35, 60),
        "6": (50, 75),
        "7": (70, 100),
        "8": (80, 110),
        "9": (90, 120),
        "10": (100, 130)
    }

    difficult_to_damage_magic = {
        1: [4, 8],
        2: [12, 18],
        3: [25, 30]
    }

    difficult_to_magic_level = {
        1: "Шаблон ступень 1",
        2: "Шаблон ступень 2",
        3: "Шаблон ступень 3",
    }

    def __init__(self, name: str, difficult: str, size: str, spec: str, feet: list[list]):
        self.name = name
        self.size = size
        self.lvl = difficult
        self.speed = 30
        self.hits = 0
        self.ac = 0
        self.stats = list()
        self.attacks = list()
        self.spells = list()
        self.immunity = list()
        self.resistance = list()
        self.skill = 0
        self.hit_bonus = 0
        self.weapon = list()
        self.spell_throw = 0

        self.spec_dict = {
            "Ближний бой": self._calc_spec_melee,
            "Дальний бой": self._calc_spec_range,
            "Заклинания": self._calc_spec_spell,
            "Бог": self._calc_spec_god
        }

        self.difficult_to_attacks_limit = {
            1: [self._calc_damage, 2],
            2: [self._calc_damage, 3],
            3: [self._calc_high_damage, 4]
        }

        self._calc_difficult_to_stats(difficult)
        if feet[0]:
            self._calc_feet(feet)
        self.spec_dict[creatures_settings['Специализация'][spec]['Архетип']](spec)
        self._calc_immunity(spec)
        self._calc_spell_through()

    def _calc_spell_through(self):
        main_stat = max(self.stats[3:])
        self.spell_throw = 8 + self.skill + main_stat

    def _calc_feet(self, feet: list[list]):
        available_feet = creatures_settings['Черты']
        for cur_feet in feet:
            for _ in range(0, cur_feet[1]):
                for ind, stat in enumerate(available_feet[cur_feet[0]]['Бонусы']):
                    self.stats[ind] = int(self.stats[ind]) + int(stat)

    def _calc_difficult_to_stats(self, difficult: str):
        hits_range = creatures_settings['Сложность'][difficult]['Хиты']
        ac_range = creatures_settings['Сложность'][difficult]['КЗ']
        skill = creatures_settings['Сложность'][difficult]['Мастерство']
        stats = creatures_settings['Сложность'][difficult]['Характеристики']
        self.hits = randint(hits_range[0], hits_range[1])
        self.ac = randint(ac_range[0], ac_range[1])
        self.skill = skill
        self.stats = [randint(stat[0], stat[1]) for stat in stats]

    def _calc_immunity(self, spec: str):
        if spec in ['Воин', 'Стрелок', 'Паладин', 'Убийца', 'Монстр']:
            if 0 < int(self.lvl) < 4:
                self._calc_phys_immunity(0, 0)
            elif 3 < int(self.lvl) < 6:
                self._calc_phys_immunity(1, 0)
            elif 5 < int(self.lvl) < 8:
                self._calc_phys_immunity(2, 1)
            else:
                self._calc_phys_immunity(3, 3)
        else:
            if 0 < int(self.lvl) < 4:
                self._calc_magic_immunity(0, 0)
            elif 3 < int(self.lvl) < 6:
                self._calc_magic_immunity(1, 0)
            elif 5 < int(self.lvl) < 8:
                self._calc_magic_immunity(2, 1)
            else:
                self._calc_magic_immunity(3, 3)

    def _calc_phys_immunity(self, resist: int, immunity: int):
        for _ in range(0, resist):
            resist_to_append = choice(abilities_dict['Сопротивления']['Физический'])
            while resist_to_append in self.resistance:
                resist_to_append = choice(abilities_dict['Сопротивления']['Физический'])
            self.resistance.append(resist_to_append)
        for _ in range(0, int(ceil(resist/2))):
            resist_to_append = choice(abilities_dict['Сопротивления']['Эффекты'])
            while resist_to_append in self.resistance:
                resist_to_append = choice(abilities_dict['Сопротивления']['Эффекты'])
            self.resistance.append(resist_to_append)
        for _ in range(0, immunity):
            immune_to_append = choice(abilities_dict['Имунитеты']['Физический'])
            while immune_to_append in self.immunity:
                immune_to_append = choice(abilities_dict['Имунитеты']['Физический'])
            self.immunity.append(immune_to_append)

    def _calc_magic_immunity(self, resist: int, immunity: int):
        for _ in range(0, resist):
            resist_to_append = choice(abilities_dict['Сопротивления']['Магический'])
            while resist_to_append in self.resistance:
                resist_to_append = choice(abilities_dict['Сопротивления']['Магический'])
            self.resistance.append(resist_to_append)
        for _ in range(0, int(ceil(resist/2))):
            resist_to_append = choice(abilities_dict['Сопротивления']['Эффекты'])
            while resist_to_append in self.resistance:
                resist_to_append = choice(abilities_dict['Сопротивления']['Эффекты'])
            self.resistance.append(resist_to_append)
        for _ in range(0, immunity):
            immune_to_append = choice(abilities_dict['Имунитеты']['Магический'])
            while immune_to_append in self.immunity:
                immune_to_append = choice(abilities_dict['Имунитеты']['Магический'])
            self.immunity.append(immune_to_append)

    def _calc_damage(self, cur_spec: dict, main_stat: int, random_damage: bool = True, weapon: int = 0,
                     attack_text_to_add: str = ''):
        if random_damage:
            damage_range = self.__class__.difficult_to_damage[self.lvl]
            damage_val = randint(damage_range[0], damage_range[1])
        else:
            res = (lambda val: val // 3 + 1 if val % 3 != 0 else val // 3)(int(self.lvl)) if int(self.lvl) != 10 else 3
            damage_range = self.__class__.difficult_to_damage_magic[res]
            damage_val = randint(damage_range[0], damage_range[1])
        if attack_text_to_add:
            pass
        else:
            attack_text_to_add = cur_spec["Текст атаки"]
        cube_col = (damage_val - self.stats[main_stat]) // self.weapon[weapon][1]
        attack_text = f'{self.name} {attack_text_to_add} ' \
                      f'{cube_col}d{self.weapon[weapon][1]}{"+" if self.stats[main_stat] > 0 else ""}' \
                      f'{self.stats[main_stat]} едениц урона. ' \
                      f'Попадание: {"+" if self.stats[main_stat] > 0 else ""}{self.skill + self.stats[main_stat]}'
        self.attacks.append(attack_text)

    def _calc_high_damage(self, cur_spec: dict, main_stat: int, random_damage: bool = True, weapon: int = 0,
                          attack_text_to_add: str = ''):
        if random_damage:
            damage_range = self.__class__.difficult_to_damage[self.lvl]
            damage_val = randint(damage_range[0], damage_range[1])
        else:
            res = (lambda val: val // 3 + 1 if val % 3 != 0 else val // 3)(int(self.lvl)) if int(self.lvl) != 10 else 3
            damage_range = self.__class__.difficult_to_damage_magic[res]
            damage_val = randint(damage_range[0], damage_range[1])
        if attack_text_to_add:
            pass
        else:
            attack_text_to_add = cur_spec["Текст атаки"]
        try:
            bonus_damage = choice(cur_spec["Бонусный урон"])
            cube_col = int((damage_val - self.stats[main_stat]) / 2 // self.weapon[weapon][1])
            add_cube_col = int((damage_val - self.stats[main_stat]) / 2 // bonus_damage[1])
            attack_text = f'{self.name} {attack_text_to_add} ' \
                          f'{cube_col}d{self.weapon[weapon][1]}' \
                          f'{"+" if self.stats[main_stat] > 0 else ""}{self.stats[main_stat]} едениц урона от оружия' \
                          f' и {add_cube_col}d{self.weapon[weapon][1]} едениц урона от {bonus_damage[0]}. ' \
                          f'Попадание: {"+" if self.stats[main_stat] > 0 else ""}{self.skill + self.stats[main_stat]}'
        except KeyError:
            cube_col = (damage_val - self.stats[main_stat]) // self.weapon[weapon][1]
            attack_text = f'{self.name} {attack_text_to_add} ' \
                          f'{cube_col}d{self.weapon[weapon][1]}{"+" if self.stats[main_stat] > 0 else ""}' \
                          f'{self.stats[main_stat]} едениц урона. ' \
                          f'Попадание: {"+" if self.stats[main_stat] > 0 else ""}{self.skill + self.stats[main_stat]}'
        self.attacks.append(attack_text)

    def _calc_multi_attack(self):
        if 4 < int(self.lvl) < 9:
            self.attacks.append(f'Мультиатака: Персонаж совершает две атаки своим оружием')
        if 8 < int(self.lvl) < 11:
            self.attacks.append(f'Мультиатака: Персонаж совершает три атаки своим оружием')

    def _create_attack(self, cur_spec: dict, main_stat: int, random_damage: bool = True):
        self._calc_multi_attack()
        res = (lambda val: val // 3 + 1 if val % 3 != 0 else val // 3)(int(self.lvl)) if int(self.lvl) != 10 else 3
        func_to_call = self.difficult_to_attacks_limit[res]
        for _ in range(0, func_to_call[1]):
            func_to_call[0](cur_spec, main_stat, random_damage=random_damage)

    def _create_killer_attack(self, cur_spec: dict, main_stat: int, random_damage: bool = True):
        self._calc_multi_attack()
        self.weapon.append(choice(creatures_settings['Специализация']['Стрелок']['Простое оружие']))
        res = (lambda val: val // 3 + 1 if val % 3 != 0 else val // 3)(int(self.lvl)) if int(self.lvl) != 10 else 3
        func_to_call = self.difficult_to_attacks_limit[res]
        for _ in range(0, ceil(func_to_call[1] / 2)):
            func_to_call[0](cur_spec, main_stat, random_damage=random_damage)
        for _ in range(0, floor(func_to_call[1] / 2)):
            func_to_call[0](cur_spec, main_stat + 1, random_damage=random_damage, weapon=1,
                            attack_text_to_add=creatures_settings['Специализация']['Стрелок']['Текст атаки'])

    def _generate_spells(self, cur_spec: dict):
        res = (lambda val: val // 3 + 1 if val % 3 != 0 else val // 3)(int(self.lvl)) if int(self.lvl) != 10 else 3
        template_key = self.__class__.difficult_to_magic_level[res]
        template = cur_spec[template_key]
        for category in template:
            for _ in range(0, category[1]):
                col = 0
                spell = choice(spells_settings[category[0]][str(res)])
                while spell in self.spells or col > 100:
                    spell = choice(spells_settings[category[0]][str(res)])
                    col += 1
                self.spells.append(spell)

    def _choose_weapon(self, cur_spec: dict):
        if 0 < int(self.lvl) < 4:
            try:
                self.weapon.append(choice(cur_spec['Простое оружие']))
            except KeyError:
                self.weapon.append(choice(cur_spec['Воинское оружие']))
        else:
            try:
                self.weapon.append(choice(cur_spec['Воинское оружие']))
            except KeyError:
                self.weapon.append(choice(cur_spec['Простое оружие']))

    def _calc_spec_melee(self, spec):
        cur_spec = creatures_settings['Специализация'][spec]
        for ind, stat in enumerate(cur_spec['Бонусы']):
            self.stats[ind] += stat
        self._choose_weapon(cur_spec)
        if spec not in ['Убийца', 'Паладин']:
            self._create_attack(cur_spec, 0)
        elif spec == 'Убийца':
            self._create_killer_attack(cur_spec, 0)
        else:
            self._create_attack(cur_spec, 0)
            self._generate_spells(cur_spec)

    def _calc_spec_range(self, spec):
        cur_spec = creatures_settings['Специализация'][spec]
        for ind, stat in enumerate(cur_spec['Бонусы']):
            self.stats[ind] += stat
        self._choose_weapon(cur_spec)
        self._create_attack(cur_spec, 1)

    def _calc_spec_spell(self, spec):
        cur_spec = creatures_settings['Специализация'][spec]
        for ind, stat in enumerate(cur_spec['Бонусы']):
            self.stats[ind] += stat
        self._choose_weapon(cur_spec)
        self._create_attack(cur_spec, 1, False)
        self._generate_spells(cur_spec)

    def _calc_spec_god(self, spec):
        cur_spec = creatures_settings['Специализация'][spec]
        for ind, stat in enumerate(cur_spec['Бонусы']):
            self.stats[ind] += stat
