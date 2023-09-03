import sqlite3
import threading


def connect_db(path_db):
    db = Database(path_db)
    # Установка соединения с базой данных
    db.connect()
    # Создание таблицы, если она не существует
    db.create_table()

    return db


class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self._connection = threading.local()

    def connect(self):
        conn = getattr(self._connection, 'conn', None)
        if conn is None:
            conn = sqlite3.connect(self.db_file)
            self._connection.conn = conn
        return conn

    def __del__(self):
        conn = getattr(self._connection, 'conn', None)
        if conn is not None:
            conn.close()

    def execute_query(self, query, params=None):
        conn = self.connect()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        return cursor.lastrowid

    def create_table(self):
        query = '''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id TEXT,
                name TEXT,
                surname TEXT,
                email TEXT,
                age INTEGER,
                type_diabetes TEXT,
                place TEXT,
                number TEXT,
                access INTEGER
            )
        '''
        self.execute_query(query)

    # def insert_user(self, chat_id, name, surname, email, age, type_diabetes, place, number, access):
    #     query = 'INSERT INTO users (chat_id, name, surname, email, age, type_diabetes, place, number, access) ' \
    #             'VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
    #     params = (chat_id, name, surname, email, age, type_diabetes, place, number, access)
    #     self.execute_query(query, params)

    def get_all_records(self):
        query = "SELECT * FROM users"
        cursor = self.connect().cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        return records

    def delete_user(self, user_id):
        query = f'DELETE FROM users WHERE id = {user_id}'
        self.execute_query(query)

    def clear_database(self):
        query = 'DELETE FROM users'
        self.execute_query(query)

    def insert_partial_user(self, chat_id, name, surname, email, age=None, type_diabetes=None, place=None, number=None,
                            access=None):
        query = 'INSERT INTO users (chat_id, name, surname, email'
        params = [chat_id, name, surname, email]
        value = "VALUES (?, ?, ?, ?"

        if age is not None:
            query += ', age'
            value += ', ?'
            params.append(age)

        if type_diabetes is not None:
            query += ', type_diabetes'
            value += ', ?'
            params.append(type_diabetes)

        if place is not None:
            query += ', place'
            value += ', ?'
            params.append(place)

        if number is not None:
            query += ', number'
            value += ', ?'
            params.append(number)

        if access is not None:
            query += ', access'
            value += ', ?'
            params.append(access)

        query += ') ' + value + ')'

        self.execute_query(query, tuple(params))
    def update_partial_user(self, chat_id, name=None, surname=None, email=None, age=None, type_diabetes=None, place=None, number=None, access=None):
        query = 'UPDATE users SET'

        params = []

        if name is not None:
            query += ' name = ?,'
            params.append(name)

        if surname is not None:
            query += ' surname = ?,'
            params.append(surname)

        if email is not None:
            query += ' email = ?,'
            params.append(email)

        if age is not None:
            query += ' age = ?,'
            params.append(age)

        if type_diabetes is not None:
            query += ' type_diabetes = ?,'
            params.append(type_diabetes)

        if place is not None:
            query += ' place = ?,'
            params.append(place)

        if number is not None:
            query += ' number = ?,'
            params.append(number)

        if access is not None:
            query += ' access = ?,'
            params.append(access)

        # Удаление последней запятой из запроса
        query = query.rstrip(',')

        # Добавление условия для конкретного пользователя по user_id
        query += ' WHERE id = ?'
        params.append(chat_id)

        self.execute_query(query, tuple(params))