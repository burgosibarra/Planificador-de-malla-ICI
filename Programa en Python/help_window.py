from PyQt5.QtWidgets import (QWidget, QLabel)
from PyQt5.QtGui import QPixmap, QIcon
from parameters import help_width, help_height, path_help, path_question


class HelpWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.move(150, 100)
        self.setFixedWidth(help_width)
        self.setFixedHeight(help_height)

        self.label = QLabel(parent=self)
        image = QPixmap(path_help).scaled(help_width, help_height)
        self.label.setPixmap(image)
        self.label.move(0, 0)

        self.setWindowTitle("Ayuda")
        self.setWindowIcon(QIcon(path_question))

    def closeEvent(self, *args, **kwargs):
        for widgets in self.findChildren(QWidget):
            widgets.deleteLater()

        self.label.deleteLater()

        self.deleteLater()

        super().closeEvent(*args, **kwargs)
