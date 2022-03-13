from classes.game.game import Game
from classes.widgets.new_game import NewGame
from settings import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QFont, QIcon
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.buttons = {}
        self.game = Game()
        self.word = "_" * self.game.get_len_secret_word()
        self.difference_hp = 0
        self.word_label = QLabel(self)
        self.health_label = QLabel(self)
        self.new_game_widget = NewGame()
        self.new_game_widget.closed.connect(self.close)
        self.new_game_widget.clicked.connect(self.new_game)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.init()

    def new_game(self):
        self.game.new_game()
        self.create_alpha_btn()
        self.word = "_" * self.game.get_len_secret_word()
        self.health_label.setText("Количество попыток: " + str(self.game.get_health()))
        self.word_label.setText(" ".join(self.word))
        self.update()
        self.show()

    def init(self):
        self.setWindowTitle("Виселица")
        self.setWindowIcon(QIcon("images/icon.png"))

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f'background-color: {BG_COLOR};')
        self.create_alpha_btn()

        self.word_label.setText(" ".join(self.word))
        self.word_label.setFont(QFont('Times', 20))
        self.word_label.move(WINDOW_WIDTH // 2, 50)
        self.word_label.resize(WINDOW_WIDTH // 2, 40)

        self.health_label.setText("Количество попыток: " + str(self.game.get_health()))
        self.health_label.setFont(QFont('Times', 15))
        self.health_label.move(MARGIN_WINDOW, WINDOW_HEIGHT - 50)
        self.health_label.resize(WINDOW_WIDTH // 2, 40)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 4))
        painter.drawLine(MARGIN_WINDOW, WINDOW_HEIGHT - MARGIN_WINDOW, MARGIN_WINDOW, MARGIN_WINDOW)
        painter.drawLine(MARGIN_WINDOW, MARGIN_WINDOW, WINDOW_WIDTH // 3, MARGIN_WINDOW)
        painter.drawLine(WINDOW_WIDTH // 3, MARGIN_WINDOW, WINDOW_WIDTH // 3, MARGIN_WINDOW * 2)
        draw_man_funcs = [self.draw_head,
                          self.draw_body,
                          self.draw_left_leg,
                          self.draw_right_leg,
                          self.draw_left_hand,
                          self.draw_right_hand]
        self.difference_hp = self.game.get_max_health() - self.game.get_health()
        for _, func in zip(range(self.difference_hp), draw_man_funcs):
            func(painter)

    @staticmethod
    def draw_head(painter: QPainter):
        painter.drawEllipse(WINDOW_WIDTH // 3 - 30,
                            MARGIN_WINDOW + 50,
                            WINDOW_WIDTH // 3 - 140,
                            MARGIN_WINDOW + 10)

    @staticmethod
    def draw_body(painter: QPainter):
        painter.drawLine(WINDOW_WIDTH // 3,
                         MARGIN_WINDOW * 3 + 10,
                         WINDOW_WIDTH // 3,
                         MARGIN_WINDOW * 5)

    @staticmethod
    def draw_left_leg(painter: QPainter):
        painter.drawLine(WINDOW_WIDTH // 3,
                         MARGIN_WINDOW * 5,
                         WINDOW_WIDTH // 3 - 20,
                         MARGIN_WINDOW * 6 + 10)

    @staticmethod
    def draw_right_leg(painter: QPainter):
        painter.drawLine(WINDOW_WIDTH // 3,
                         MARGIN_WINDOW * 5,
                         WINDOW_WIDTH // 3 + 20,
                         MARGIN_WINDOW * 6 + 10)

    @staticmethod
    def draw_right_hand(painter: QPainter):
        painter.drawLine(WINDOW_WIDTH // 3,
                         MARGIN_WINDOW * 4 - 10,
                         WINDOW_WIDTH // 3 + 30,
                         MARGIN_WINDOW * 4 + 30)

    @staticmethod
    def draw_left_hand(painter: QPainter):
        painter.drawLine(WINDOW_WIDTH // 3,
                         MARGIN_WINDOW * 4 - 10,
                         WINDOW_WIDTH // 3 - 30,
                         MARGIN_WINDOW * 4 + 30)

    def create_alpha_btn(self):
        ords = iter(i for i in range(ord("А"), ord("Я") + 1))
        for row in range(1, 6):
            for col in range(1, 8):
                margin = 40
                try:
                    char = chr(next(ords))
                    self.buttons[f'btn_{char}'] = QPushButton(char, self)
                    self.buttons[f'btn_{char}'].move(WINDOW_WIDTH // 2 - 40 + col * margin,
                                                     WINDOW_HEIGHT // 2 - 40 + row * margin)
                    self.buttons[f'btn_{char}'].resize(30, 20)
                    self.buttons[f'btn_{char}'].clicked.connect(lambda ch, key=char: self.clicked_on_char(key))
                except StopIteration:
                    return

    def clicked_on_char(self, key):
        if self.game.char_in_secret_word(key):
            word = list(self.word)
            for i in self.game.find_position(key):
                word[i] = key
            self.word = "".join(word)
            self.word_label.setText(" ".join(self.word))
            self.buttons[f'btn_{key}'].setStyleSheet("background-color: green")
        else:
            painter = QPainter(self)
            painter.setPen(QPen(Qt.black, 4))
            self.game.reduce_health()
            self.health_label.setText("Количество попыток: " + str(self.game.get_health()))
            self.buttons[f'btn_{key}'].setStyleSheet("background-color: red")
            self.update()
        self.buttons[f'btn_{key}'].setEnabled(False)
        if not self.game.get_health():
            self.hide()
            self.show_new_game_widget("Вы проиграли")
        if "_" not in self.word:
            self.hide()
            self.show_new_game_widget("Вы выиграли")

    def show_new_game_widget(self, text):
        self.new_game_widget.create_text(text)
        self.new_game_widget.show()

    def closeEvent(self, event):
        self.game.end()