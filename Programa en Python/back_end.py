import json
from PyQt5.QtCore import pyqtSignal, QObject
from parameters import path_planner, path_subject
import sys


class Processor(QObject):

    update_central_window = pyqtSignal(str)
    update_status_bar = pyqtSignal(str)
    update_convalidation_window = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_semester(self, string):

        if len(string) == 0:
            self.update()
            return None

        subject = json.loads(string)
        if not self.evaluate_update(subject):
            message = "No puedes mover ese ramo ahí, "
            message += "tendrás problemas con sus prerrequisitos"
            self.update_status_bar.emit(message)
            return None

        with open(path_planner, "r") as document:
            planner = json.load(document)

        del planner[subject["semestre actual"]][subject["codigo"]]
        planner[subject["semestre destino"]][subject["codigo"]] = \
            subject["estado"]

        with open(path_planner, "w") as document:
            json.dump(planner, document, indent=4)

        self.update()

    def evaluate_update(self, subject):
        with open(path_planner, "r") as document:
            planner = json.load(document)
        if int(subject["semestre actual"]) > int(subject["semestre destino"]):
            ignored_subject = set()
            for semester in range(int(subject["semestre destino"]),
                                  len(planner) + 1):
                ignored_subject |= set(planner[str(semester)].keys())
            with open(path_subject, "r") as document:
                all_subject = json.load(document)
            requirements = set(all_subject[subject["codigo"]]["requisitos"])
            if len(requirements & ignored_subject) > 0:
                return False
            else:
                return True
        return True

    def update_subject_state(self, string):
        dictionary = json.loads(string)
        with open(path_planner, "r") as document:
            planner = json.load(document)
        semester = dictionary["semestre actual"]
        code = dictionary["codigo"]
        if dictionary["estado"] == "disponible":
            planner[semester][code] = "cursado"
            dictionary["instruccion"] = "cursar ramo"
        elif dictionary["estado"] == "cursado":
            planner[semester][code] = "disponible"
            dictionary["instruccion"] = "descursar ramo"
        with open(path_planner, "w") as document:
            json.dump(planner, document, indent=4)
        if not (dictionary["estado"] == "no disponible" or
                dictionary["estado"] == "convalidado"):
            self.evaluate_requirement(dictionary)
            self.update()
        return None

    def update(self):
        with open(path_planner, "r") as document:
            planner = json.load(document)
        dictionary = {"malla": planner}
        dictionary["creditos"] = {}

        with open(path_subject, "r") as document:
            subject = json.load(document)
        for semesters in planner:
            credit = 0
            for code in planner[semesters]:
                credit += int(subject[code]["creditos"])
            dictionary["creditos"][semesters] = str(credit)

        if max([int(value) for value in dictionary["creditos"].values()]) > 21:
            message = "Existe un semestre con mas de 21 creditos"
        else:
            message = "Se ha actualizado la malla con exito"
        self.update_status_bar.emit(message)

        self.update_central_window.emit(json.dumps(dictionary))
        return None

    def evaluate_requirement(self, dictionary):
        with open(path_planner, "r") as document:
            planner = json.load(document)
        with open(path_subject, "r") as document:
            subjects = json.load(document)
        approved_subjects = set({""})
        for semesters in planner:
            for codes in planner[semesters]:
                if (planner[semesters][codes] == "cursado" or
                    planner[semesters][codes] == "convalidado"):
                    approved_subjects.add(codes)
        if dictionary["instruccion"] == "cursar ramo":
            for semester in range(int(dictionary["semestre actual"]),
                                  len(planner) + 1):
                for codes in planner[str(semester)]:
                    if planner[str(semester)][codes] == "no disponible":
                        requirements = set(subjects[codes]["requisitos"])
                        if requirements <= approved_subjects:
                            planner[str(semester)][codes] = "disponible"

        elif dictionary["instruccion"] == "descursar ramo":
            for semester in range(int(dictionary["semestre actual"]),
                                  len(planner) + 1):
                semester_subjects = list(planner[str(semester)].keys())
                semester_subjects.sort(
                    key=lambda subject: int(subjects[subject]["codigo"])
                )
                for codes in semester_subjects:
                    bool_1 = not (set(subjects[codes]["requisitos"]) <= \
                                  approved_subjects)
                    bool_2 = planner[str(semester)][codes] != "convalidado"
                    if bool_1 and bool_2:
                        if codes in approved_subjects:
                            approved_subjects.remove(codes)
                        planner[str(semester)][codes] = "no disponible"
        with open(path_planner, "w") as document:
            json.dump(planner, document, indent=4)

        return None

    def add_remove_semester(self, string):
        boolean = json.loads(string)

        with open(path_planner, "r") as document:
            planner = json.load(document)

        last_semester = len(planner)

        if boolean:
            new_semester = str(last_semester + 1)
            planner[new_semester] = {}

        else:
            if len(planner[str(last_semester)]) == 0:
                del planner[str(last_semester)]

        with open(path_planner, "w") as document:
            json.dump(planner, document, indent=4)

        self.update()

    def convalidate_subject(self, subject):
        subject = subject.upper()
        message = ""

        with open(path_planner, "r") as document:
            planner = json.load(document)

        for semesters in planner:
            if subject in planner[semesters]:
                if planner[semesters][subject] != "convalidado":
                    planner[semesters][subject] = "convalidado"
                    message = "Se ha convalidado el ramo"
                    dictionary = {"instruccion": "cursar ramo"}
                elif planner[semesters][subject] == "convalidado":
                    planner[semesters][subject] = "no disponible"
                    message = "Se ha des-convalidado el ramo"
                    dictionary = {"instruccion": "descursar ramo"}
                self.update_convalidation_window.emit(message)
                break

        if message == "":
            message = "No se ha encontrado el ramo"
            self.update_convalidation_window.emit(message)
            return None

        with open(path_planner, "w") as document:
            json.dump(planner, document, indent=4)

        dictionary["semestre actual"] = "1"
        self.evaluate_requirement(dictionary)
        self.update()
