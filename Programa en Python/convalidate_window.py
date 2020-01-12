from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QLineEdit)
from PyQt5.QtGui import QPixmap, QIcon, QPainter
from PyQt5.QtCore import QRectF, Qt, pyqtSignal
from parameters import (convalidate_width, convalidate_height,
                        path_check_mark)


class ConvalidateWindow(QWidget):

    send_convalidation_to_main_window = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.move(150, 100)
        self.setFixedWidth(convalidate_width)
        self.setFixedHeight(convalidate_height)

        self.label_1 = QLabel(("Ramo a convalidar (Si está convalidado" +
                              "aparecerá como no cursado)"), parent=self)
        self.label_1.setAlignment(Qt.AlignCenter)
        self.label_1.setGeometry(convalidate_width * 0.1,
                                 convalidate_height * 0.1,
                                 convalidate_width * 0.9,
                                 convalidate_height * 0.3)

        self.line_edit = QLineEdit("Ingrese el codigo del ramo", 
                                   parent=self)
        self.line_edit.setGeometry(convalidate_width * 0.1,
                                   convalidate_height * 0.5,
                                   convalidate_width * 0.5,
                                   convalidate_height * 0.3)

        self.button = QPushButton("Enviar", parent=self)
        self.button.setGeometry(convalidate_width * 0.7,
                                convalidate_height * 0.5,
                                convalidate_width * 0.2,
                                convalidate_height * 0.3)
        self.button.clicked.connect(self.send_convalidation)

        self.label_2 = QLabel(("Ramo a convalidar (Si está convalidado" +
                              "aparecerá como no cursado)"), parent=self)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setGeometry(convalidate_width * 0.1,
                                 convalidate_height * 0.9,
                                 convalidate_width * 0.9,
                                 convalidate_height * 0.1)

        self.setWindowTitle("Convalidar")
        self.setWindowIcon(QIcon(path_check_mark))
        self.show()

    def send_convalidation(self):
        subject = self.line_edit.text()
        self.line_edit.setText("")
        self.send_convalidation_to_main_window.emit(subject)

    def setMessage(self, message):
        self.label_2.setText(message)

    def closeEvent(self, *args, **kwargs):
        for widgets in self.findChildren(QWidget):
            widgets.deleteLater()

        self.deleteLater()

        super().closeEvent(*args, **kwargs)
