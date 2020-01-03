from PyQt5.QtWidgets import QLabel, QVBoxLayout
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from parameters import (semester_width, semester_height,
                        path_legend_background,
                        path_approved_subject,
                        path_available_subject,
                        path_unavailable_subject)


class Legend(QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_GUI()

    def init_GUI(self):
        image = QPixmap(path_legend_background).scaled(semester_width,
                                                       semester_height)
        self.setPixmap(image)

        approved_subject = QLabel(parent=self)
        image = QPixmap(path_approved_subject).scaled(semester_width * 0.15,
                                                      semester_height * 0.15)
        approved_subject.setPixmap(image)
        approved_subject.move(semester_width * 0.1, semester_height * 0.1)
        approved_subject_text = QLabel("Ramo\naprobado", parent=self)
        approved_subject_text.move(semester_width * 0.3,
                                   semester_height * 0.175)

        available_subject = QLabel(parent=self)
        image = QPixmap(path_available_subject).scaled(semester_width * 0.15,
                                                       semester_height * 0.15)
        available_subject.setPixmap(image)
        available_subject.move(semester_width * 0.1, semester_height * 0.3)
        available_subject_text = QLabel("Ramo\ndisponible", parent=self)
        available_subject_text.move(semester_width * 0.3,
                                    semester_height * 0.375)

        not_available_subject = QLabel(parent=self)
        image = QPixmap(path_unavailable_subject).scaled(semester_width * 0.15,
                                                         semester_height * 0.15)
        not_available_subject.setPixmap(image)
        not_available_subject.move(semester_width * 0.1, semester_height * 0.5)
        not_available_subject_text = QLabel("Ramo\nno\ndisponible",
                                            parent=self)
        not_available_subject_text.move(semester_width * 0.3,
                                        semester_height * 0.575)

        about = QLabel(("Creado por Nicolás Burgos\n" +
                        "Más información Ctrl+S"),
                       parent=self)
        about.move(semester_width * 0.1, semester_height * 0.7)
