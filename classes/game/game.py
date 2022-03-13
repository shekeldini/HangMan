from db.db import DataBase


class Game:
    def __init__(self):
        self.__db = DataBase()
        self._health = 6
        self.__secret_word = self.__db.get_random_word().upper()
        self.__max_health = 6

    def char_in_secret_word(self, char: str):
        return char in self.__secret_word

    def get_health(self):
        return self._health

    def reduce_health(self):
        self._health -= 1

    def get_max_health(self):
        return self.__max_health

    def find_position(self, char: str):
        return (i for i, ltr in enumerate(self.__secret_word) if ltr == char)

    def get_len_secret_word(self):
        return len(self.__secret_word)

    def new_game(self):
        self.__secret_word = self.__db.get_random_word().upper()
        self._health = self.__max_health

    def get_secret_word(self):
        return self.__secret_word

    def end(self):
        self.__db.close_connection()
