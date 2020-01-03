from PyQt5.QtWidgets import QLabel, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, QRectF, Qt
from PyQt5.QtGui import QPixmap, QDrag, QPainter
from parameters import (semester_width,
                        path_semester, path_semester_21,
                        path_semester_number,
                        semester_number_height, subject_width)
from block import Block
import json


class Semester(QLabel):

    send_semester_update = pyqtSignal(str)
    send_subject_state_update = pyqtSignal(str)

    def __init__(self, number, credit, height, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.number = number
        self.credit = int(credit)
        self.height = height
        self.setAcceptDrops(True)
        self.init_GUI()

    def init_GUI(self):
        if self.credit > 21:
            image = QPixmap(path_semester_21).scaled(semester_width,
                                                     self.height)
        else:
            image = QPixmap(path_semester).scaled(semester_width,
                                                  self.height)
        self.setPixmap(image)

    def dragEnterEvent(self, subject):
        if subject.mimeData().hasFormat("text/plain"):
            subject.accept()
        else:
            subject.ignore()

    def dropEvent(self, subject):
        dictionary = json.loads(subject.mimeData().text())
        dictionary["semestre destino"] = self.number
        text = json.dumps(dictionary)
        self.send_semester_update.emit(text)

    def add_subjects(self, dictionary):

        semester_number = QLabel(parent=self)
        image = QPixmap(path_semester_number).scaled(subject_width,
                                                     semester_number_height)

        painter = QPainter(image)
        painter.drawText(QRectF(0.0, 0.0,
                                subject_width, semester_number_height),
                         Qt.AlignJustify | Qt.AlignCenter,
                         f"SEMESTRE \n {self.number}")
        painter.end()

        semester_number.setPixmap(image)
        semester_number.move(15, 5)

        subject_length = len(dictionary)
        if subject_length != 0:
            subject_height = (self.height - semester_number_height)
            subject_height -= (subject_length - 1) * 5
            subject_height -= 10
            subject_height /= subject_length
            subject_number = 1
            for subject in dictionary:
                block = Block(code=subject, state=dictionary[subject],
                              height=subject_height,
                              semester=self.number, parent=self)
                block.clicked_block.connect(self.update_subject_state)
                pos_y = (subject_height + 5) * (subject_number - 1)
                block.move(15, pos_y + semester_number_height + 10)
                subject_number += 1

    def update_subject_state(self, string):
        self.send_subject_state_update.emit(string)
