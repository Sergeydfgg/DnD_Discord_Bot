import sqlite3


def create_db():
    try:
        sqlite_connection = sqlite3.connect('players.db')
        sqlite_create_table_query = '''CREATE TABLE reg_players (
                                    name TEXT UNIQUE,
                                    reputation INTEGER,
                                    activity INTEGER);'''

        cursor = sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        cursor.execute(sqlite_create_table_query)
        sqlite_connection.commit()
        print("Таблица SQLite создана")

        cursor.close()
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)


def add_rep_player(rep_val: int, player_name: str):
    try:
        sqlite_connection = sqlite3.connect('players.db')
        cursor = sqlite_connection.cursor()
        print("База данных подключена к SQLite")

        sql = "SELECT reputation FROM reg_players WHERE name=?;"

        cursor.execute(sql, (player_name,))
        one_result = cursor.fetchone()

        sql = ''' UPDATE reg_players
                  SET reputation = ?
                  WHERE name = ?'''

        cursor.execute(sql, (one_result[0] + rep_val, player_name))
        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")
        return one_result[0] + rep_val
    except sqlite3.Error as error:
        print("Ошибка при выполнении")
        print("Класс исключения: ", error.__class__)


def add_active_player(act_val: int, player_name: str):
    try:
        sqlite_connection = sqlite3.connect('players.db')
        cursor = sqlite_connection.cursor()
        print("База данных подключена к SQLite")

        sql = "SELECT activity FROM reg_players WHERE name=?;"

        cursor.execute(sql, (player_name,))
        one_result = cursor.fetchone()

        sql = ''' UPDATE reg_players
                  SET activity = ?
                  WHERE name = ?'''

        cursor.execute(sql, (one_result[0] + act_val, player_name))
        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")
        print(one_result[0] + act_val)
        return one_result[0] + act_val
    except sqlite3.Error as error:
        print("Ошибка при выполнении")
        print("Класс исключения: ", error.__class__)


def check_player_rep(player: str):
    sqlite_connection = sqlite3.connect('players.db')
    cursor = sqlite_connection.cursor()

    sql = "SELECT reputation FROM reg_players WHERE name=?;"

    cursor.execute(sql, (player, ))
    one_result = cursor.fetchone()
    sqlite_connection.commit()
    cursor.close()
    sqlite_connection.close()
    return one_result


def check_player_active(player: str):
    sqlite_connection = sqlite3.connect('players.db')
    cursor = sqlite_connection.cursor()

    sql = "SELECT activity FROM reg_players WHERE name=?;"

    cursor.execute(sql, (player, ))
    one_result = cursor.fetchone()
    sqlite_connection.commit()
    cursor.close()
    sqlite_connection.close()
    return one_result


def reg_player(player: str):
    sqlite_connection = sqlite3.connect('players.db')
    cursor = sqlite_connection.cursor()
    print("База данных подключена к SQLite")

    sql = """INSERT INTO reg_players
                     (name, reputation, activity)  VALUES  (?, ?, ?)"""

    cursor.execute(sql, (player, 4, 10))
    sqlite_connection.commit()
    cursor.close()
