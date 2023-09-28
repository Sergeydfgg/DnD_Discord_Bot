import discord
import asyncio
from discord.ext import commands
from discord import ui
from discord import Interaction
from discord import app_commands
from discord.utils import get
import random
import re
import json
import Auto_fight
import sqlite3
import players_db_for_server
import libraries
import creature


current_news_list = list()
with open('builds/builds_list.json', encoding='utf-8') as builds_list_file:
    builds_list = json.load(builds_list_file)

with open('Data/allSpells.js', 'r', encoding='utf-8') as file:
    new_text = file.read()

new_text = new_text.replace('{', '|')
new_text = new_text.replace('}', '|')

spells_list = dict()

for part in new_text.split('|'):
    if part.strip()[:2] == '"n':
        part = part.replace('\n', ':')
        min_parts = part.split(':')
        spells_list[min_parts[2].strip().replace(',', '').replace('"', '').replace('      ', '')] = {
            min_parts[i].strip().replace(',', '').replace('"', '').replace('      ', ''):
                min_parts[i+1].strip().replace(',', '').replace('"', '').replace('      ', '')
            for i in range(3, len(min_parts) - 1, 2)
        }


class LfgMenu(ui.View):
    def __init__(self, game_title, player_col, game_time, game_disc, game_master, channel):
        super().__init__()
        self.value = None
        self.game_title = game_title
        self.player_col = player_col
        self.game_time = game_time
        self.game_disc = game_disc
        self.game_master = game_master
        self.channel = channel
        self.players = list()

    async def send(self):
        self.message = await self.channel.send(embed=self.create_embed(), view=self)

    def create_embed(self):
        embed = discord.Embed(
            title='Партия ДнД',
            description='Присоединяйся к очередной партии ДнД!',
            color=discord.Color.yellow()
        )
        embed.add_field(name='Название компании', value=self.game_title, inline=False)
        embed.add_field(name='Мастер', value=self.game_master, inline=False)
        embed.add_field(name='Свободных мест', value=self.player_col, inline=False)
        embed.add_field(name='Дата и время', value=self.game_time, inline=False)
        embed.add_field(name='Описание', value=self.game_disc, inline=False)
        embed.add_field(name='Участиники', value=self.players, inline=False)
        return embed

    async def update_message(self):
        await self.message.edit(embed=self.create_embed(), view=self)

    @ui.button(label='Записаться', style=discord.ButtonStyle.green)
    async def btn_1(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.defer()
        if int(self.player_col) > 0 and str(interaction.user).split('#')[0] not in self.players:
            self.player_col = int(self.player_col) - 1
            self.players.append(str(interaction.user).split('#')[0])
        else:
            return
        await self.update_message()

    @ui.button(label='Выписаться', style=discord.ButtonStyle.red)
    async def btn_2(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.defer()
        if str(interaction.user).split('#')[0] in self.players:
            self.player_col = int(self.player_col) + 1
            self.players.remove(str(interaction.user).split('#')[0])
        else:
            return
        await self.update_message()


class MusicMenu(ui.View):
    def __init__(self, interaction):
        super().__init__()
        self.interaction = interaction
        self.categories = list(self._get_categories())
        self.songs_list = list()
        self.cur_page = 0
        self.cur_category = ''

    @staticmethod
    def _get_categories():
        return libraries.show_music_categories()

    @staticmethod
    def _get_songs_list(category: str):
        return libraries.get_category_data(category)

    async def send(self):
        self.message = self.interaction.response
        await self.message.send_message(embed=self.create_embed(),
                                        view=self, ephemeral=True)
        self.message = await self.interaction.original_response()

    @staticmethod
    def create_embed():
        embed = discord.Embed(
            title='Список категорий',
            description='',
            color=discord.Color.red()
        )
        return embed

    def create_song_embed(self):
        embed = discord.Embed(
            title='Список музыки',
            description=f'{self.cur_category}',
            color=discord.Color.red()
        )
        for ind, song in enumerate(self.songs_list):
            embed.add_field(name='', value=f'{ind+1}) {str(song)}', inline=False)
        return embed

    async def update_message(self):
        await self.message.edit(embed=self.create_embed(), view=self)

    async def update_song_message(self):
        await self.message.edit(embed=self.create_song_embed(), view=self)

    async def delete_message(self):
        await self.message.delete()

    @ui.button(label='Город', style=discord.ButtonStyle.blurple)
    async def btn_1(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.defer()
        if self.cur_category != 'Город':
            self.cur_page = 5
            self.cur_category = 'Город'
            self.songs_list = self._get_songs_list('Город')[self.cur_page - 5:self.cur_page]
            await self.update_song_message()

    @ui.button(label='Бой', style=discord.ButtonStyle.blurple)
    async def btn_2(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.defer()
        if self.cur_category != 'Бой':
            self.cur_page = 5
            self.cur_category = 'Бой'
            self.songs_list = self._get_songs_list('Бой')[self.cur_page - 5:self.cur_page]
            await self.update_song_message()

    @ui.button(label='Поход', style=discord.ButtonStyle.blurple)
    async def btn_3(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.defer()
        if self.cur_category != 'Поход':
            self.cur_page = 5
            self.cur_category = 'Поход'
            self.songs_list = self._get_songs_list('Поход')[self.cur_page - 5:self.cur_page]
            await self.update_song_message()

    @ui.button(label='Эпичная', style=discord.ButtonStyle.blurple)
    async def btn_4(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.defer()
        if self.cur_category != 'Эпичная':
            self.cur_page = 5
            self.cur_category = 'Эпичная'
            self.songs_list = self._get_songs_list('Эпичная')[self.cur_page - 5:self.cur_page]
            await self.update_song_message()

    @ui.button(label='Фоновая', style=discord.ButtonStyle.blurple)
    async def btn_5(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.defer()
        if self.cur_category != 'Фоновая':
            self.cur_page = 5
            self.cur_category = 'Фоновая'
            self.songs_list = self._get_songs_list('Фоновая')[self.cur_page - 5:self.cur_page]
            await self.update_song_message()

    @ui.button(label='Назад', style=discord.ButtonStyle.green)
    async def btn_7(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.defer()
        try:
            self.cur_page -= 5
            self.songs_list = self._get_songs_list(self.cur_category)[self.cur_page - 5:self.cur_page]
            if len(self.songs_list) == 5:
                await self.update_song_message()
            else:
                self.cur_page += 5
                self.songs_list = self._get_songs_list(self.cur_category)[self.cur_page - 5:self.cur_page]
        except IndexError:
            pass

    @ui.button(label='Далее', style=discord.ButtonStyle.green)
    async def btn_6(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.defer()
        try:
            self.cur_page += 5
            self.songs_list = self._get_songs_list(self.cur_category)[self.cur_page - 5:self.cur_page]
            if 1 < len(self.songs_list) <= 5:
                await self.update_song_message()
            else:
                self.cur_page -= 5
                self.songs_list = self._get_songs_list(self.cur_category)[self.cur_page - 5:self.cur_page]
        except IndexError:
            pass

    @ui.button(label='Закрыть', style=discord.ButtonStyle.red)
    async def btn_8(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.defer()
        await self.delete_message()


class PartyLfg(ui.Modal, title='Сбор на игру'):
    game_title = ui.TextInput(
        style=discord.TextStyle.short,
        label='Название игры',
        required=True
    )

    player_col = ui.TextInput(
        style=discord.TextStyle.short,
        label='Количество игроков',
        required=True,
        placeholder='1-9'
    )

    game_time = ui.TextInput(
        style=discord.TextStyle.short,
        label='Начало игры',
        required=True,
        placeholder='ДД.ММ-ЧЧ:ММ:СС'
    )

    game_disc = ui.TextInput(
        style=discord.TextStyle.long,
        max_length=500,
        label='Описание',
        required=False
    )

    async def on_submit(self, interaction: discord.Interaction):
        channel = interaction.guild.get_channel(1139931220986310706)

        if all([re.fullmatch(r'\d', self.player_col.value),
                re.fullmatch(r'[0-3]\d\.[0-1]\d-[0-2]\d:[0-5]\d:[0-5]\d', self.game_time.value)]):
            view = LfgMenu(self.game_title.value, self.player_col.value,
                           self.game_time.value, self.game_disc.value,
                           str(interaction.user).split('#')[0], channel)

            await view.send()
            await interaction.response.send_message('OK', ephemeral=True)
        else:
            await interaction.response.send_message('Ошибка заполнения', ephemeral=True)

    @staticmethod
    async def on_error(self, interaction: discord.Interaction, error):
        print(error)


class Feedback(ui.Modal, title='Обратная связь'):
    general_feedback = ui.TextInput(
        style=discord.TextStyle.long,
        max_length=1024,
        label='Отзыв',
        required=False
    )

    good_players = ui.TextInput(
        style=discord.TextStyle.short,
        label='Похвала игрокам',
        placeholder='Ники игроков',
        required=False
    )

    bad_players = ui.TextInput(
        style=discord.TextStyle.short,
        label='Претензии игрокам',
        placeholder='Ники игроков',
        required=False
    )

    problem_feedback = ui.TextInput(
        style=discord.TextStyle.long,
        max_length=1024,
        label='Суть проблемы',
        placeholder='Если есть претензии',
        required=False
    )

    async def on_submit(self, interaction: discord.Interaction):
        channel = interaction.guild.get_channel(1146764097728282706)

        embed = discord.Embed(
            title='Карточка отзыва',
            description=f'Отзыв  от {str(interaction.user)}',
            color=discord.Color.blue()
        )
        embed.add_field(name='Отзыв', value=self.general_feedback.value, inline=False)
        embed.add_field(name='Похвала', value=self.good_players.value, inline=False)
        embed.add_field(name='Претензии', value=self.bad_players.value, inline=False)
        embed.add_field(name='Суть проблемы', value=self.problem_feedback.value, inline=False)

        await channel.send(embed=embed)
        await interaction.response.send_message('Ваш отзыв отправлен', ephemeral=True)

    @staticmethod
    async def on_error(self, interaction: discord.Interaction, error):
        print(error)


intents = discord.Intents.all()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1137739483014500382))
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')


@tree.command(name='reg', description='Зарегистрироваться и получить роли', guild=discord.Object(id=1137739483014500382))
async def reg(interaction: discord.Interaction):
    server = client.guilds[0]
    rep_role = get(server.roles, id=1146757466399449098)
    active_role = get(server.roles, id=1146757649053007912)
    try:
        players_db_for_server.reg_player(str(interaction.user).split('#')[0])
        await interaction.user.add_roles(rep_role)
        await interaction.user.add_roles(active_role)
        await interaction.response.send_message('OK', ephemeral=True)
    except sqlite3.Error:
        await interaction.response.send_message('Вы зарегестрированы', ephemeral=True)


@tree.command(name='reg_user', description='Зарегистрироваться и получить роли', guild=discord.Object(id=1137739483014500382))
async def reg_user(interaction: discord.Interaction, user_name: str):
    server = client.guilds[0]
    rep_role = get(server.roles, id=1146757466399449098)
    active_role = get(server.roles, id=1146757649053007912)
    if str(interaction.user).split('#')[0] == 'serega3301':
        try:
            players_db_for_server.reg_player(user_name)
            await interaction.user.add_roles(rep_role)
            await interaction.user.add_roles(active_role)
            await interaction.response.send_message('OK', ephemeral=True)
        except sqlite3.Error:
            await interaction.response.send_message('Уже зареган', ephemeral=True)


@tree.command(name='my_rep', description='Ваша репутация в чисоенном эквиваленте',
              guild=discord.Object(id=1137739483014500382))
async def my_rep(interaction: discord.Interaction):
    try:
        result = players_db_for_server.check_player_rep(str(interaction.user).split('#')[0])
        await interaction.response.send_message(result[0], ephemeral=True)
    except sqlite3.Error:
        await interaction.response.send_message('Что-то пошло не так', ephemeral=True)


@tree.command(name='my_active', description='Ваша активность в чисоенном эквиваленте',
              guild=discord.Object(id=1137739483014500382))
async def my_active(interaction: discord.Interaction):
    try:
        result = players_db_for_server.check_player_active(str(interaction.user).split('#')[0])
        await interaction.response.send_message(result[0], ephemeral=True)
    except sqlite3.Error:
        await interaction.response.send_message('Что-то пошло не так', ephemeral=True)


@tree.command(name='add_rep', description='Поднять репутацию', guild=discord.Object(id=1137739483014500382))
async def add_rep(interaction: discord.Interaction, rep_val: int, player: str):
    server = client.guilds[0]
    admin_role = get(server.roles, id=1146004606514642944)
    if admin_role in interaction.user.roles:
        try:
            cur_rep = players_db_for_server.add_rep_player(rep_val, player)
            cur_user = None
            for mem in client.get_all_members():
                if str(mem).split('#')[0] == player:
                    cur_user = mem
                    break
            if cur_user:
                if 3 < cur_rep < 8:
                    role_to_remove = get(server.roles, id=1146757404957093918)
                    role = get(server.roles, id=1146757466399449098)
                    await cur_user.add_roles(role)
                    await cur_user.remove_roles(role_to_remove)
                elif cur_rep > 7:
                    role_to_remove = get(server.roles, id=1146757466399449098)
                    role = get(server.roles, id=1146757549333430273)
                    await cur_user.add_roles(role)
                    await cur_user.remove_roles(role_to_remove)
                await interaction.response.send_message('OK', ephemeral=True)
            else:
                await interaction.response.send_message('Такого пользователя нет', ephemeral=True)
        except sqlite3.Error:
            await interaction.response.send_message('Что-то пошло не так', ephemeral=True)
    else:
        await interaction.response.send_message('Недостаточно прав', ephemeral=True)


@tree.command(name='remove_rep', description='Понизить репутацию', guild=discord.Object(id=1137739483014500382))
async def remove_rep(interaction: discord.Interaction, rep_val: int, player: str):
    server = client.guilds[0]
    admin_role = get(server.roles, id=1146004606514642944)
    if admin_role in interaction.user.roles:
        try:
            cur_rep = players_db_for_server.add_rep_player(-1*rep_val, player)
            cur_user = None
            for mem in client.get_all_members():
                if str(mem).split('#')[0] == player:
                    cur_user = mem
                    break
            if cur_user:
                if cur_rep < 3:
                    role_to_remove = get(server.roles, id=1146757466399449098)
                    role = get(server.roles, id=1146757404957093918)
                    await cur_user.add_roles(role)
                    await cur_user.remove_roles(role_to_remove)
                elif 3 < cur_rep < 8:
                    role_to_remove = get(server.roles, id=1146757549333430273)
                    role = get(server.roles, id=1146757466399449098)
                    await cur_user.add_roles(role)
                    await cur_user.remove_roles(role_to_remove)
                await interaction.response.send_message('OK', ephemeral=True)
            else:
                await interaction.response.send_message('Такого пользователя нет', ephemeral=True)
        except sqlite3.Error:
            await interaction.response.send_message('Что-то пошло не так', ephemeral=True)
    else:
        await interaction.response.send_message('Недостаточно прав', ephemeral=True)


@tree.command(name='add_active', description='Поднять активность', guild=discord.Object(id=1137739483014500382))
async def add_active(interaction: discord.Interaction, act_val: int, player: str):
    server = client.guilds[0]
    admin_role = get(server.roles, id=1146004606514642944)
    if admin_role in interaction.user.roles:
        try:
            cur_active = players_db_for_server.add_active_player(act_val, player)
            cur_user = None
            for mem in client.get_all_members():
                if str(mem).split('#')[0] == player:
                    cur_user = mem
                    break
            if cur_user:
                if 9 < cur_active < 22:
                    role = get(server.roles, id=1146757649053007912)
                    role_to_remove = get(server.roles, id=1146757602450096209)
                    await cur_user.remove_roles(role_to_remove)
                    await cur_user.add_roles(role)
                elif cur_active > 21:
                    role = get(server.roles, id=1146757842586587266)
                    role_to_remove = get(server.roles, id=1146757649053007912)
                    await cur_user.remove_roles(role_to_remove)
                    await cur_user.add_roles(role)
                await interaction.response.send_message('OK', ephemeral=True)
            else:
                await interaction.response.send_message('Такого пользователя нет', ephemeral=True)
        except sqlite3.Error:
            await interaction.response.send_message('Что-то пошло не так', ephemeral=True)
    else:
        await interaction.response.send_message('Недостаточно прав', ephemeral=True)


@tree.command(name='remove_active', description='Понизить активность', guild=discord.Object(id=1137739483014500382))
async def remove_active(interaction: discord.Interaction, act_val: int, player: str):
    server = client.guilds[0]
    admin_role = get(server.roles, id=1146004606514642944)
    if admin_role in interaction.user.roles:
        try:
            cur_active = players_db_for_server.add_active_player(-1*act_val, player)
            cur_user = None
            for mem in client.get_all_members():
                if str(mem).split('#')[0] == player:
                    cur_user = mem
                    break
            if cur_user:
                if cur_active < 9:
                    role = get(server.roles, id=1146757602450096209)
                    role_to_remove = get(server.roles, id=1146757649053007912)
                    await cur_user.remove_roles(role_to_remove)
                    await cur_user.add_roles(role)
                elif 9 < cur_active < 22:
                    role = get(server.roles, id=1146757649053007912)
                    role_to_remove = get(server.roles, id=1146757842586587266)
                    await cur_user.remove_roles(role_to_remove)
                    await cur_user.add_roles(role)
                await interaction.response.send_message('OK', ephemeral=True)
            else:
                await interaction.response.send_message('Такого пользователя нет', ephemeral=True)
        except sqlite3.Error:
            await interaction.response.send_message('Что-то пошло не так', ephemeral=True)
    else:
        await interaction.response.send_message('Недостаточно прав', ephemeral=True)


@tree.command(name='ft_to_mtr', description='Перевести Футы в Метры', guild=discord.Object(id=1137739483014500382))
async def ft_to_mtr(interaction: discord.Interaction, length: int):
    try:
        await interaction.response.send_message(f'{length/3.281:.3f} m')
    except ValueError:
        await interaction.response.send_message('Неверное значение', ephemeral=True)


@tree.command(name='mtr_to_ft', description='Перевести Метры в Футы', guild=discord.Object(id=1137739483014500382))
async def mtr_to_ft(interaction: discord.Interaction, length: int):
    try:
        await interaction.response.send_message(f'{length*3.281:.3f} ft')
    except ValueError:
        await interaction.response.send_message('Неверное значение', ephemeral=True)


@tree.command(name='send_build', description='Получить готовый билд', guild=discord.Object(id=1137739483014500382))
async def send_build(interaction: discord.Interaction, build_name: str):
    try:
        await interaction.response.send_message(file=discord.File(builds_list[build_name]))
    except KeyError:
        await interaction.response.send_message('Такого билда пока нет...')


@tree.command(name='spell', description='Информация о заклинание', guild=discord.Object(id=1137739483014500382))
async def spell(interaction: discord.Interaction, spell_name: str):
    try:
        cur_spell = spells_list[spell_name]
        embed = discord.Embed(
            title=spell_name,
            description='Карточка заклинания',
            color=discord.Color.green()
        )
        try:
            embed.add_field(name='Школа', value=cur_spell['school'], inline=False)
        except KeyError:
            pass
        try:
            embed.add_field(name='Уровень', value=cur_spell['level'], inline=False)
        except KeyError:
            pass
        try:
            embed.add_field(name='Время каста', value=cur_spell['castingTime'], inline=False)
        except KeyError:
            pass
        try:
            embed.add_field(name='Дальность', value=cur_spell['range'], inline=False)
        except KeyError:
            pass
        try:
            embed.add_field(name='Компоненты', value=cur_spell['components'], inline=False)
        except KeyError:
            pass
        try:
            embed.add_field(name='Материалы', value=cur_spell['materials'], inline=False)
        except KeyError:
            pass
        try:
            embed.add_field(name='Длительность', value=cur_spell['duration'], inline=False)
        except KeyError:
            pass
        try:
            if len(cur_spell['text']) <= 1024:
                embed.add_field(name='Описание', value=cur_spell['text'], inline=False)
            else:
                embed.add_field(name='Описание', value=cur_spell['text'][:1021] + '...', inline=False)
        except KeyError:
            pass
        try:
            embed.add_field(name='Источник', value=cur_spell['source'], inline=False)
        except KeyError:
            pass
        await interaction.response.send_message(embed=embed)
    except KeyError:
        await interaction.response.send_message('Что-то пошло не так, возможно такого заклинания нет в базе.',
                                                ephemeral=True)


@tree.command(name='create_game', description='Создать сбор на игру', guild=discord.Object(id=1137739483014500382))
async def create_game(interaction: discord.Interaction):
    game_modal = PartyLfg()
    await interaction.response.send_modal(game_modal)


@tree.command(name='feedback', description='Обратная связь', guild=discord.Object(id=1137739483014500382))
async def feedback(interaction: discord.Interaction):
    feedback_modal = Feedback()
    await interaction.response.send_modal(feedback_modal)


@tree.command(name='auto_fight', description='Авто бой', guild=discord.Object(id=1137739483014500382))
async def auto_fight(interaction: discord.Interaction, players_name: str, enemy_name: str, enemy_col: int):
    try:
        cur_players = [Auto_fight.Player(player_name) for player_name in players_name.split()]
        cur_enemy = Auto_fight.Enemy(enemy_name)
        players_hits = sum([cur_player.hits for cur_player in cur_players])
        enemy_hits = cur_enemy.hits * enemy_col
        player_to_hit = 0
        while enemy_hits * enemy_col > 0 and players_hits > 0:
            players_hits = sum([cur_player.hits for cur_player in cur_players])
            if cur_players[player_to_hit].hits > 0:
                cur_player = cur_players[player_to_hit]
            else:
                player_to_hit += 1
                cur_player = cur_players[player_to_hit]
            for _ in range(0, enemy_col):
                cur_player.get_damage(cur_enemy.make_attack())
            for attack_player in cur_players:
                attack_pair = attack_player.make_attack()
                if attack_pair[0] > cur_enemy.armor_class:
                    enemy_hits -= attack_pair[1]
        players_names = ", ".join([cur_player.name for cur_player in cur_players])
        if enemy_hits > players_hits:
            await interaction.response.send_message(f'Победил - {cur_enemy.name}\n'
                                                    f'У {players_names} '
                                                    f'{players_hits} хитов\n'
                                                    f'У {cur_enemy.name} {enemy_hits} хитов\n')
        else:
            await interaction.response.send_message(f'Победил - {players_names}\n'
                                                    f'У {players_names} {players_hits} хитов\n'
                                                    f'У {cur_enemy.name} {enemy_hits} хитов\n')
    except IndexError as error:
        await interaction.response.send_message(error, ephemeral=True)


@tree.command(name='roll', description='Рольнуть кубик', guild=discord.Object(id=1137739483014500382))
async def roll(interaction: discord.Interaction, dice: str):
    if re.fullmatch(r'\dd\d', dice) or re.fullmatch(r'\dd\d\d', dice) \
            or re.fullmatch(r'\d\dd\d\d', dice) or re.fullmatch(r'\d\dd\d', dice):
        rolls, limit = map(int, dice.split('d'))
        result = sum(random.randint(1, limit) for _ in range(rolls))
        await interaction.response.send_message(result)
    else:
        await interaction.response.send_message('Че ты сука пишешь?', ephemeral=True)


@tree.command(name='make_creature', description='Создание NPC', guild=discord.Object(id=1137739483014500382))
async def make_creature(interaction: discord.Interaction, name: str, difficult: str, size: str,
                        specialization: str, feet: str = "-"):
    if feet != '-':
        feet_parts = feet.replace(' ', '').split(',')
        feet_to_send = list()
        for cur_part in feet_parts:
            parts_to_send = cur_part.split(':')
            if len(parts_to_send) > 1:
                feet_to_send.append([parts_to_send[0], int(parts_to_send[1])])
            else:
                feet_to_send.append([parts_to_send[0], 1])
    else:
        feet_to_send = [[]]

    made_creature = creature.Creature(name, difficult, size, specialization, feet_to_send)
    stats_text = f'Сил: {"+" if made_creature.stats[0] > 0 else ""}{made_creature.stats[0]}\n' \
                 f'Лов: {"+" if made_creature.stats[1] > 0 else ""}{made_creature.stats[1]}\n' \
                 f'Тел: {"+" if made_creature.stats[2] > 0 else ""}{made_creature.stats[2]}\n' \
                 f'Инт: {"+" if made_creature.stats[3] > 0 else ""}{made_creature.stats[3]}\n' \
                 f'Мдр: {"+" if made_creature.stats[4] > 0 else ""}{made_creature.stats[4]}\n' \
                 f'Хар: {"+" if made_creature.stats[5] > 0 else ""}{made_creature.stats[5]}'
    embed = discord.Embed(
            title=made_creature.name,
            description='Карточка существа',
            color=discord.Color.yellow()
        )
    embed.add_field(name='Размер', value=made_creature.size, inline=False)
    embed.add_field(name='Класс доспеха', value=made_creature.ac, inline=False)
    embed.add_field(name='Хиты', value=made_creature.hits, inline=False)
    embed.add_field(name='Скорость', value=made_creature.speed, inline=False)
    embed.add_field(name='Характеристики', value=stats_text, inline=False)
    embed.add_field(name='Сопротивления', value=made_creature.resistance, inline=False)
    embed.add_field(name='Имунитеты', value=made_creature.immunity, inline=False)
    if made_creature.spells:
        embed.add_field(name='Заклинания', value="\n".join(made_creature.spells), inline=False)
        embed.add_field(name='Сл спасброска от заклинаний',
                        value=f'Базовая характеристика - '
                              f'{max(made_creature.stats[3:])}\n'
                              f'Сл спасброска - {made_creature.spell_throw}', inline=False)
    embed.add_field(name='Оружие', value="\n".join([val[0] for val in made_creature.weapon]), inline=False)
    embed.add_field(name='Атаки', value="\n".join(made_creature.attacks), inline=False)
    await interaction.response.send_message(embed=embed)


@tree.command(name='music_lib', description='Список музыки', guild=discord.Object(id=1137739483014500382))
async def music_lib(interaction: discord.Interaction):
    view = MusicMenu(interaction)
    await view.send()


client.run('MTA0MzU2OTI0NjYwNjcyOTM3Ng.G7yAm4.PDlNM7Y7wzPzDsl_Da_90aJoDNZNUO7OoAA494')
