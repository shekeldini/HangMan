from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR


class NewGame(QWidget):
    closed = QtCore.pyqtSignal()
    clicked = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.new_game_btn = QPushButton("Новая Игра", self)
        self.text_label = QLabel(self)
        self.init()

    def init(self):
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f'background-color: {BG_COLOR};')

        self.new_game_btn.clicked.connect(self.click_on_new_game)
        self.new_game_btn.move(WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2)
        self.new_game_btn.resize(150, 50)
        self.new_game_btn.setFont(QFont('Times', 14))

        self.text_label.setFont(QFont('Times', 24))
        self.text_label.resize(WINDOW_WIDTH, 40)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.move(0, 100)

    def create_text(self, text):
        self.text_label.setText(text)

    def click_on_new_game(self):
        self.clicked.emit()
        self.hide()

    def closeEvent(self, event):
        self.closed.emit()
