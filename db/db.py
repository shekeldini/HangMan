import sqlite3
import random


class DataBase:
    def __init__(self):
        self._con = sqlite3.connect("db/db.sqlite")

    def create_tables(self):
        cur = self._con.cursor()
        cur.execute(open("Create Tables.sql", "r").read())
        cur.close()

    def fill_words(self):
        cur = self._con.cursor()
        words = ['муравей', 'бабуин', 'барсук', 'медведь',
                 'бобр', 'верблюд', 'кошка', 'моллюск',
                 'кобра', 'пума', 'койот', 'ворона',
                 'олень', 'собака', 'осел', 'утка',
                 'орел', 'хорек', 'лиса', 'лягушка',
                 'коза', 'гусь', 'ястреб', 'ящерица',
                 'лама', 'моль', 'обезьяна', 'лось',
                 'мышь', 'мул', 'тритон', 'выдра',
                 'сова', 'панда', 'попугай', 'голубь',
                 'питон', 'кролик', 'баран', 'крыса',
                 'носорог', 'лосось', 'акула', 'змея',
                 'паук', 'аист', 'лебедь', 'тигр',
                 'жаба', 'форель', 'индейка', 'черепаха',
                 'ласка', 'кит', 'волк', 'вомбат',
                 'зебра']
        for word in words:
            try:
                cur.execute(f"""
                INSERT INTO words (word) VALUES ('{word}');
                """)
                self._con.commit()
            except sqlite3.Error as e:
                print("Ошибка при добавлении в базу данных:" + str(e))

        cur.close()

    def get_words(self):
        cur = self._con.cursor()
        cur.execute("""
        SELECT word FROM words;
        """)
        res = cur.fetchall()
        cur.close()
        if res:
            return [x[0] for x in res]
        return []

    def get_random_word(self):
        return random.choice(self.get_words())

    def close_connection(self):
        self._con.close()

