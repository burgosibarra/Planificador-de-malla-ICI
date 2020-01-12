from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, QSize
from central_window import CentralWindow
from help_window import HelpWindow
from about_window import AboutWindow
from convalidate_window import ConvalidateWindow
from parameters import (path_logo, path_book, path_exit,
                        main_window_x_pos, main_window_y_pos,
                        window_height, window_width,
                        path_plus, path_minus, path_question,
                        path_check_mark)


class MainWindow(QMainWindow):

    process_add_remove_semester = pyqtSignal(str)
    process_semester_update = pyqtSignal(str)
    process_subject_state_update = pyqtSignal(str)
    process_subject_convalidation = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.central_window = CentralWindow()
        self.central_window.send_semester_update.connect(
            self.receive_semester_update)
        self.central_window.send_subject_state_update.connect(
            self.receive_subject_state_update)

        self.init_GUI()

    def init_GUI(self):

        self.setMinimumWidth(450)
        self.setMinimumHeight(270)

        self.central_window.setSizePolicy(QSizePolicy.Expanding,
                                          QSizePolicy.Expanding)

        self.setWindowTitle("Planificador de malla curricular")
        self.setWindowIcon(QIcon(path_logo))

        self.setCentralWidget(self.central_window)

        about_section = QAction(QIcon(path_book),
                                '&Sobre el programa',
                                self)
        about_section.setShortcut('Ctrl+S')
        about_section.setStatusTip('Más información')
        about_section.triggered.connect(self.raise_about_window)

        exit_action = QAction(QIcon(path_exit), '&Exit', self)
        exit_action.setShortcut('Ctrl+E')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(QApplication.quit)

        convalidate_action = QAction(QIcon(path_check_mark),
                                     '&Convalidar', self)
        convalidate_action.setStatusTip('Convalidar ramos')
        convalidate_action.triggered.connect(self.raise_convalidate_window)

        add_semester = QAction(QIcon(path_plus),
                               '&Agregar Semestre',
                               self)
        add_semester.setStatusTip('Se agregará un semestre al final')
        add_semester.triggered.connect(self.add_semester)

        remove_semester = QAction(QIcon(path_minus),
                                  '&Eliminar Semestre',
                                  self)
        message = 'Se eliminará el último semestre si está vacío'
        remove_semester.setStatusTip(message)
        remove_semester.triggered.connect(self.remove_semester)

        help_window = QAction(QIcon(path_question),
                              '&Ayuda',
                              self)
        message = 'Se mostrará una ventana de ayuda'
        help_window.setStatusTip(message)
        help_window.triggered.connect(self.raise_help_window)

        menubar = self.menuBar()
        archivo_menu = menubar.addMenu('&Opciones')
        archivo_menu.addAction(convalidate_action)
        archivo_menu.addAction(about_section)
        archivo_menu.addAction(exit_action)

        toolbar = self.addToolBar('Toolbar')
        toolbar.addAction(add_semester)
        toolbar.addAction(remove_semester)
        toolbar.addAction(help_window)
        toolbar.setIconSize(QSize(100, 16))

        self.setGeometry(main_window_x_pos, main_window_y_pos,
                         window_width, window_height)

    def resizeEvent(self, *args, **kwargs):
        self.process_semester_update.emit("")
        super().resizeEvent(*args, **kwargs)

    def update_status_bar(self, mensaje):
        self.statusBar().showMessage(mensaje)

    def raise_about_window(self):
        self.about_window = AboutWindow()
        self.about_window.show()

    def raise_convalidate_window(self):
        self.convalidate_window = ConvalidateWindow()
        self.convalidate_window.send_convalidation_to_main_window.connect(
            self.receive_subject_convalidation)

    def raise_help_window(self):
        self.help_window = HelpWindow()
        self.help_window.show()

    def receive_semester_update(self, string):
        self.process_semester_update.emit(string)

    def receive_subject_state_update(self, string):
        self.process_subject_state_update.emit(string)

    def receive_subject_convalidation(self, subject):
        self.process_subject_convalidation.emit(subject)

    def update_planner(self, string):
        self.central_window.update(string)

    def update_convalidate_window(self, message):
        self.convalidate_window.setMessage(message)

    def add_semester(self):
        self.process_add_remove_semester.emit('true')

    def remove_semester(self):
        self.process_add_remove_semester.emit('false')
