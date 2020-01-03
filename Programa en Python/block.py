from PyQt5.QtWidgets import QLabel, QApplication
from PyQt5.QtGui import QPixmap, QDrag, QPainter
from PyQt5.QtCore import (pyqtSignal, QSize, QRect,
                          QMimeData, Qt, QObject, QRectF)
from parameters import (path_subject, subject_width,
                        path_available_subject, path_unavailable_subject,
                        path_approved_subject,
                        path_square)
import json


class Square(QLabel):

    def __init__(self, value, width, height, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = value
        self.height = height
        self.width = width
        self.init_GUI()

    def init_GUI(self):
        image = QPixmap(path_square).scaled(self.width, self.height)

        painter = QPainter(image)
        painter.drawText(QRectF(0.0, 0.0,
                                self.width, self.height),
                         Qt.AlignCenter | Qt.TextWordWrap,
                         self.value)
        painter.end()

        self.setPixmap(image)


class Block(QLabel):

    clicked_block = pyqtSignal(str)

    with open(path_subject, "r") as document:
        subjects = json.load(document)

    def __init__(self, code, height, semester=None,
                 state="no disponible", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombre = self.subjects[code]["nombre"]
        self.code = code
        self.height = height
        self.state = state
        self.semester = semester
        self.requirements = self.subjects[self.code]["requisitos"]
        self.credits = self.subjects[self.code]["creditos"]
        self.init_GUI()

    def init_GUI(self):
        if self.state == "disponible":
            image = QPixmap(path_available_subject).scaled(subject_width,
                                                           self.height)
        elif self.state == "no disponible":
            image = QPixmap(path_unavailable_subject).scaled(subject_width,
                                                             self.height)
        elif self.state == "cursado":
            image = QPixmap(path_approved_subject).scaled(subject_width,
                                                          self.height)

        painter = QPainter(image)

        painter.drawText(QRectF(0.0, self.height * 0.1,
                                subject_width, self.height * 0.8),
                         Qt.AlignCenter | Qt.TextWordWrap,
                         self.nombre)

        painter.end()

        self.setPixmap(image)

        label = Square(value=self.code, height=self.height * 0.15,
                       width=subject_width/2, parent=self)
        label.move(1, 1)

        label = Square(value=self.credits, height=self.height * 0.15,
                       width=subject_width/5, parent=self)
        label.move(subject_width * 0.8 + 1, 1)

        if "" not in self.requirements:
            requirement_height = self.height * 0.15
            requirement_width = subject_width - 2
            requirement_width -= (len(self.requirements) - 1) * 2
            requirement_width /= len(self.requirements)
            requirement = 1
            for requirements in self.requirements:
                label = Square(value=requirements, height=requirement_height,
                               width=requirement_width, parent=self)
                x_pos = (requirement - 1) * (requirement_width + 2) + 1
                label.move(x_pos, self.height * 0.84)
                requirement += 1

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
        if event.button() == Qt.RightButton:
            dictionary = json.dumps({"codigo": self.code,
                                     "semestre actual": self.semester,
                                     "estado": self.state})
            self.clicked_block.emit(dictionary)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return None

        manhattanLength = event.pos()
        manhattanLength -= self.drag_start_position
        manhattanLength = manhattanLength.manhattanLength()
        if manhattanLength < QApplication.startDragDistance():
            return None

        drag = QDrag(self)
        mimedata = QMimeData()
        message = json.dumps({"codigo": self.code,
                              "estado": self.state,
                              "semestre actual": self.semester})
        mimedata.setText(message)

        drag.setMimeData(mimedata)

        pixmap = QPixmap(QSize(subject_width,
                               self.height)
                         )
        painter = QPainter(pixmap)
        painter.drawPixmap(0, 0,
                           subject_width,
                           self.height,
                           self.grab()
                           )
        painter.end()
        pixmap = pixmap.scaled(QSize(subject_width,
                                     self.height)
                               )
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        drag.exec_(Qt.CopyAction | Qt.MoveAction)
