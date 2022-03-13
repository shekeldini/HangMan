import sys
from PyQt5.QtWidgets import QApplication
from classes.widgets.main_widget import Window

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
