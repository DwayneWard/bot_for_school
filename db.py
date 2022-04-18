import sqlite3

from exceptions import UserNotFound


class BotDB:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def user_exist(self, email):
        db_result = self.cursor.execute("SELECT * FROM user WHERE email = ?", [email])
        result = db_result.fetchone()
        if result:
            return None
        else:
            raise UserNotFound

    def get_name_by_email(self, email):
        db_result = self.cursor.execute('SELECT first_name, last_name FROM user WHERE email = ?', [email])
        result = db_result.fetchone()
        if result:
            return result
        else:
            raise UserNotFound
