import sqlite3
from typing import Optional


def select_random_records():
    try:
        with sqlite3.connect('games.db') as sqlite_connection:
            cursor = sqlite_connection.cursor()
            print("Підключено до SQLite")

            sqlite_select_query = """ 
            SELECT * FROM game_store WHERE metascore BETWEEN 90 AND 96 ORDER BY RANDOM() LIMIT 6 """

            cursor.execute(sqlite_select_query)
            rows = cursor.fetchall()

            column_names = [description[0] for description in cursor.description]

            records = [dict(zip(column_names, row)) for row in rows]

            return records

    except sqlite3.Error as error:
        print("Помилка при роботі з SQLite", error)
        return []


def select_game_name_for_url(name):
    try:
        with sqlite3.connect('games.db') as sqlite_connection:
            cursor = sqlite_connection.cursor()
            print("Підключено до SQLite")

            sqlite_select_query = "SELECT * FROM game_store WHERE name_for_url = ?"

            cursor.execute(sqlite_select_query, (name,))
            rows = cursor.fetchall()

            column_names = [description[0] for description in cursor.description]

            records = [dict(zip(column_names, row)) for row in rows]

            return records

    except sqlite3.Error as error:
        print("Помилка при роботі з SQLite", error)
        return []


def select_game_name(name):
    try:
        with sqlite3.connect('games.db') as sqlite_connection:
            cursor = sqlite_connection.cursor()
            print("Підключено до SQLite")

            sqlite_select_query = "SELECT * FROM game_store WHERE name = ?"

            cursor.execute(sqlite_select_query, (name,))
            rows = cursor.fetchall()

            column_names = [description[0] for description in cursor.description]

            records = [dict(zip(column_names, row)) for row in rows]

            return records

    except sqlite3.Error as error:
        print("Помилка при роботі з SQLite", error)
        return []


def select_all_games():
    try:
        with sqlite3.connect('games.db') as sqlite_connection:
            cursor = sqlite_connection.cursor()
            print("Підключено до SQLite")

            sqlite_select_query = """SELECT * FROM game_store"""

            cursor.execute(sqlite_select_query)
            rows = cursor.fetchall()

            column_names = [description[0] for description in cursor.description]

            records = [dict(zip(column_names, row)) for row in rows]

            return records

    except sqlite3.Error as error:
        print("Помилка при роботі з SQLite", error)
        return []


def add_column_to_game_store(column_name, column_type):
    try:
        with sqlite3.connect('games.db') as sqlite_connection:
            cursor = sqlite_connection.cursor()
            print("Підключено до SQLite")

            sqlite_add_column_query = f"""ALTER TABLE game_store ADD COLUMN {column_name} {column_type}"""

            cursor.execute(sqlite_add_column_query)
            print(f"Колонка '{column_name}' з типом '{column_type}' була успішно додана.")

    except sqlite3.Error as error:
        print("Помилка при роботі з SQLite:", error)


def update_image_by_id(new_image_url, game_id):
    try:
        with sqlite3.connect('games.db') as conn:
            cursor = conn.cursor()

            update_query = """UPDATE game_store
                              SET about_game = ?
                              WHERE id = ?;"""

            cursor.execute(update_query, (new_image_url, game_id))
            conn.commit()

            print("Зображення успішно оновлене")

    except sqlite3.Error as error:
        print("Помилка при оновленні зображення:", error)


def select_all_games_filter(sort_by: Optional[str] = None, filter_text: Optional[str] = None):
    games = select_all_games()
    if filter_text:
        games = [game for game in games if filter_text.lower() in game["name"].lower()]

    if sort_by:
        if sort_by == 'price-asc':
            games.sort(key=lambda x: x['price'])
        elif sort_by == 'price-desc':
            games.sort(key=lambda x: x['price'], reverse=True)
        elif sort_by == 'name-asc':
            games.sort(key=lambda x: x['name'].lower())
        elif sort_by == 'name-desc':
            games.sort(key=lambda x: x['name'].lower(), reverse=True)

    return games
