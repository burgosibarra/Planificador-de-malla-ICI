from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QFormLayout, QGroupBox,
                             QScrollArea, QSizePolicy, QLabel)
from PyQt5.QtCore import pyqtSignal, QObjectCleanupHandler
from semester import Semester
from block import Block
from legend import Legend
from parameters import (semester_width,
                        semester_height_scale)
import json


class CentralWindow(QWidget):

    send_semester_update = pyqtSignal(str)
    send_subject_state_update = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll = QScrollArea()

        self.setWindowTitle("Malla")

        self.setLayout(QHBoxLayout())

    def update(self, string):

        QObjectCleanupHandler().add(self.layout())

        scroll_bar_position = self.scroll.horizontalScrollBar().value()

        for widgets in self.findChildren(QWidget):
            widgets.deleteLater()

        dictionary = json.loads(string)
        credit = dictionary["creditos"]
        dictionary = dictionary["malla"]

        hbox = QHBoxLayout()

        legend = Legend()
        hbox.addWidget(legend)

        for semester_number in [str(index)
                                for index in range(1, len(dictionary) + 1)]:
            height = self.geometry().height() * semester_height_scale
            semester = Semester(number=semester_number,
                                credit=credit[semester_number],
                                height=height)
            semester.add_subjects(dictionary[semester_number])
            hbox.addWidget(semester)
            semester.send_semester_update.connect(
                self.receive_semester_update)
            semester.send_subject_state_update.connect(
                self.receive_subject_state_update)

        groupBox = QGroupBox()
        groupBox.setLayout(hbox)
        self.scroll = QScrollArea()
        self.scroll.setWidget(groupBox)
        self.scroll.setWidgetResizable(True)

        self.scroll.horizontalScrollBar().setValue(scroll_bar_position)

        hbox = QHBoxLayout()
        hbox.addWidget(self.scroll)
        self.setLayout(hbox)

    def receive_semester_update(self, string):
        self.send_semester_update.emit(string)

    def receive_subject_state_update(self, string):
        self.send_subject_state_update.emit(string)
