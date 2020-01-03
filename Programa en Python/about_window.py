from PyQt5.QtWidgets import (QWidget, QLabel)
from PyQt5.QtGui import QPixmap, QIcon, QPainter
from PyQt5.QtCore import QRectF, Qt
from parameters import (help_width, help_height, path_question,
                        about_text, path_semester)
import json


class AboutWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.move(150, 100)
        self.setFixedWidth(help_width)
        self.setFixedHeight(help_height)

        self.label = QLabel(about_text, parent=self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(0, 0, help_width, help_height)
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.setWindowTitle("Sobre")
        self.setWindowIcon(QIcon(path_question))

    def closeEvent(self, *args, **kwargs):
        for widgets in self.findChildren(QWidget):
            widgets.deleteLater()

        self.label.deleteLater()

        self.deleteLater()

        super().closeEvent(*args, **kwargs)
