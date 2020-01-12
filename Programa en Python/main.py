from back_end import Processor
from main_window import MainWindow
import sys
from PyQt5.QtWidgets import QApplication


def hook(type, value, traceback):
    print(type)
    print(traceback)


app = QApplication([])
sys.__excepthook__ = hook

main_window = MainWindow()

processor = Processor()

main_window.process_semester_update.connect(
    processor.update_semester)
main_window.process_subject_state_update.connect(
    processor.update_subject_state)
main_window.process_add_remove_semester.connect(
    processor.add_remove_semester)
main_window.process_subject_convalidation.connect(
    processor.convalidate_subject)

processor.update_central_window.connect(
    main_window.update_planner
)

processor.update_status_bar.connect(
    main_window.update_status_bar
)

processor.update_convalidation_window.connect(
    main_window.update_convalidate_window
)

main_window.show()
processor.update()

sys.exit(app.exec_())
