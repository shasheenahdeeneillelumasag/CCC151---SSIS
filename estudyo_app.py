import sys
import csv
import os
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QHeaderView, QAbstractItemView
from PyQt6.QtCore import Qt

#CSV file paths
COLLEGES_CSV = "colleges.csv"
PROGRAMS_CSV = "programs.csv"
STUDENTS_CSV = "students.csv"

#CSV Data Manager
class CSVManager:
    def __init__(self):
        self.init_csv_files()

    def init_csv_files(self):
        if not os.path.exists(COLLEGES_CSV):
            self.write_colleges([
                {"code": "CCS", "name": "College of Computer Studies"},
                {"code": "COE", "name": "College of Engineering"},
            ])

        if not os.path.exists(PROGRAMS_CSV):
            self.write_programs([
                {"code": "BSCS", "name": "Bachelor of Science in Computer Science", "college_code": "CCS"},
                {"code": "BSIT", "name": "Bachelor of Science in Information Technology", "college_code": "CCS"},
            ])

        if not os.path.exists(STUDENTS_CSV):
            self.write_students([
                {
                    "id": "2024-0001",
                    "first_name": "Shasheenah Deeneille",
                    "last_name": "Lumasag",
                    "gender": "Female",
                    "program_code": "BSCS",
                    "year_level": "3",
                },
            ])

    def read_colleges(self):
        return self._read_csv(COLLEGES_CSV)

    def read_programs(self):
        return self._read_csv(PROGRAMS_CSV)

    def read_students(self):
        return self._read_csv(STUDENTS_CSV)

    def write_colleges(self, rows):
        self._write_csv(COLLEGES_CSV, ["code", "name"], rows)

    def write_programs(self, rows):
        self._write_csv(PROGRAMS_CSV, ["code", "name", "college_code"], rows)

    def write_students(self, rows):
        self._write_csv(STUDENTS_CSV, ["id", "first_name", "last_name", "gender", "program_code", "year_level"], rows)

    def _read_csv(self, filepath):
        if not os.path.exists(filepath):
            return []
        with open(filepath, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def _write_csv(self, filepath, fieldnames, rows):
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    #College operations
    def add_college(self, code, name):
        colleges = self.read_colleges()
        if any(c["code"] == code for c in colleges):
            raise ValueError("College code already exists!")
        colleges.append({"code": code, "name": name})
        self.write_colleges(colleges)

    def delete_college(self, code):
        self.write_colleges([c for c in self.read_colleges() if c["code"] != code])

    def college_has_programs(self, code):
        return any(p["college_code"] == code for p in self.read_programs())

    #Program operations
    def add_program(self, code, name, college_code):
        programs = self.read_programs()
        if any(p["code"] == code for p in programs):
            raise ValueError("Program code already exists!")
        programs.append({"code": code, "name": name, "college_code": college_code})
        self.write_programs(programs)

    def delete_program(self, code):
        self.write_programs([p for p in self.read_programs() if p["code"] != code])

    def program_has_students(self, code):
        return any(s["program_code"] == code for s in self.read_students())

    #Student operations 
    def add_student(self, sid, first_name, last_name, gender, program_code, year_level):
        students = self.read_students()
        if any(s["id"] == sid for s in students):
            raise ValueError("Student ID already exists!")
        students.append({
            "id": sid, "first_name": first_name, "last_name": last_name,
            "gender": gender, "program_code": program_code, "year_level": year_level,
        })
        self.write_students(students)

    def delete_student(self, sid):
        self.write_students([s for s in self.read_students() if s["id"] != sid])

    def search_students(self, field, value):
        return [s for s in self.read_students() if value.lower() in s.get(field, "").lower()]

    def sort_students(self, field):
        return sorted(self.read_students(), key=lambda s: s.get(field, "").lower())
    
#Main
class EstudyoApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.csv = CSVManager()
        uic.loadUi("estudyo_main.ui", self)

        self.setup_ui()
        self.setup_connections()
        self.load_initial_data()
        self.show()

    def setup_ui(self):
        self.setup_table_properties(self.tableStudents)
        self.setup_table_properties(self.tablePrograms)
        self.setup_table_properties(self.tableColleges)
        self.stackedWidget.setCurrentIndex(0)
        self.headerTitle.setText("Dashboard")
        self.populate_combo_boxes()

    def setup_table_properties(self, table):
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.verticalHeader().setVisible(False)

    def populate_combo_boxes(self):
        programs = self.csv.read_programs()
        self.comboProgramCode.clear()
        for p in programs:
            self.comboProgramCode.addItem(f"{p['code']} - {p['name']}", p["code"])

        colleges = self.csv.read_colleges()
        self.comboCollegeCode.clear()
        for c in colleges:
            self.comboCollegeCode.addItem(f"{c['code']} - {c['name']}", c["code"])

    def setup_connections(self):
        # Sidebar navigation
        self.navButton.clicked.connect(lambda: self.switch_page(0, "Dashboard"))
        self.btnManage.clicked.connect(lambda: self.switch_page(1, "Manage Students"))
        self.btnPrograms.clicked.connect(lambda: self.switch_page(2, "Manage Programs"))
        self.btnColleges.clicked.connect(lambda: self.switch_page(3, "Manage Colleges"))

        # Dashboard buttons
        self.btnSearch.clicked.connect(self.search_students)
        self.btnSort.clicked.connect(self.sort_students)
        self.btnEdit.clicked.connect(self.edit_student_from_dashboard)
        self.pageDashboard.findChild(QtWidgets.QPushButton, "btnDelete").clicked.connect(
            self.delete_student_from_dashboard
        )

        # Manage Students page
        for btn in self.pageManage.findChildren(QtWidgets.QPushButton):
            if btn.text() == "Add Student":
                btn.clicked.connect(self.add_student)
            elif btn.text() == "Clear Form":
                btn.clicked.connect(self.clear_student_form)

        # Programs page
        for btn in self.pagePrograms.findChildren(QtWidgets.QPushButton):
            if btn.text() == "Add Program":
                btn.clicked.connect(self.add_program)
            elif btn.text() == "Delete Program":
                btn.clicked.connect(self.delete_program)
            elif btn.text() == "Clear Form":
                btn.clicked.connect(self.clear_program_form)

        # Colleges page
        for btn in self.pageColleges.findChildren(QtWidgets.QPushButton):
            if btn.text() == "Add College":
                btn.clicked.connect(self.add_college)
            elif btn.text() == "Delete College":
                btn.clicked.connect(self.delete_college)
            elif btn.text() == "Clear Form":
                btn.clicked.connect(self.clear_college_form)

    #Navigation
    def switch_page(self, index, title):
        self.stackedWidget.setCurrentIndex(index)
        self.headerTitle.setText(title)

        for i, btn in enumerate([self.navButton, self.btnManage, self.btnPrograms, self.btnColleges]):
            btn.setChecked(i == index)

        if index == 0:
            self.load_students()
        elif index == 2:
            self.load_programs()
        elif index == 3:
            self.load_colleges()

    def load_initial_data(self):
        self.load_colleges()
        self.load_programs()
        self.load_students()

    #Data loaders
    def load_students(self, students=None):
        if students is None:
            students = self.csv.read_students()
        self.tableStudents.setRowCount(0)
        for r, s in enumerate(students):
            self.tableStudents.insertRow(r)
            for c, val in enumerate([s["id"], s["first_name"], s["last_name"],
                                      s["program_code"], s["year_level"], s["gender"]]):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tableStudents.setItem(r, c, item)

    def load_programs(self):
        self.tablePrograms.setRowCount(0)
        for r, p in enumerate(self.csv.read_programs()):
            self.tablePrograms.insertRow(r)
            for c, val in enumerate([p["code"], p["name"], p["college_code"]]):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tablePrograms.setItem(r, c, item)

    def load_colleges(self):
        self.tableColleges.setRowCount(0)
        for r, col in enumerate(self.csv.read_colleges()):
            self.tableColleges.insertRow(r)
            for c, val in enumerate([col["code"], col["name"]]):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tableColleges.setItem(r, c, item)

    # Dashboard
    def search_students(self):
        field_map = {
            "Student ID": "id",
            "First Name": "first_name",
            "Last Name": "last_name",
            "Program": "program_code",
        }
        field = field_map.get(self.comboSearchField.currentText(), "id")
        value = self.lineSearchInput.text().strip()
        if not value:
            self.load_students()
            return
        self.load_students(self.csv.search_students(field, value))

    def sort_students(self):
        field_map = {
            "Student ID": "id",
            "First Name": "first_name",
            "Last Name": "last_name",
            "Program": "program_code",
            "Year Level": "year_level",
        }
        field = field_map.get(self.comboSortField.currentText(), "id")
        self.load_students(self.csv.sort_students(field))

    def edit_student_from_dashboard(self):
        selected = self.tableStudents.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a student to edit!")
            return

        sid          = self.tableStudents.item(selected, 0).text()
        first_name   = self.tableStudents.item(selected, 1).text()
        last_name    = self.tableStudents.item(selected, 2).text()
        program_code = self.tableStudents.item(selected, 3).text()
        year_level   = self.tableStudents.item(selected, 4).text()
        gender       = self.tableStudents.item(selected, 5).text()

        self.csv.delete_student(sid)

        self.switch_page(1, "Manage Students")
        self.lineStudentId.setText(sid)
        self.lineFirstName.setText(first_name)
        self.lineLastName.setText(last_name)

        idx = self.comboGender.findText(gender)
        if idx >= 0:
            self.comboGender.setCurrentIndex(idx)

        for i in range(self.comboProgramCode.count()):
            if self.comboProgramCode.itemData(i) == program_code:
                self.comboProgramCode.setCurrentIndex(i)
                break

        idx = self.comboYearLevel.findText(year_level)
        if idx >= 0:
            self.comboYearLevel.setCurrentIndex(idx)

    def delete_student_from_dashboard(self):
        selected = self.tableStudents.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a student to delete!")
            return

        sid = self.tableStudents.item(selected, 0).text()
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete student {sid}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.csv.delete_student(sid)
            QMessageBox.information(self, "Success", "Student deleted successfully!")
            self.load_students()

    # Manage Students
    def add_student(self):
        sid          = self.lineStudentId.text().strip()
        first_name   = self.lineFirstName.text().strip()
        last_name    = self.lineLastName.text().strip()
        gender       = self.comboGender.currentText()
        program_code = self.comboProgramCode.currentData()
        year_level   = self.comboYearLevel.currentText()

        if not all([sid, first_name, last_name, gender, program_code]):
            QMessageBox.warning(self, "Input Error", "Please fill in all fields!")
            return

        try:
            self.csv.add_student(sid, first_name, last_name, gender, program_code, year_level)
            QMessageBox.information(self, "Success", "Student added successfully!")
            self.clear_student_form()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def clear_student_form(self):
        self.lineStudentId.clear()
        self.lineFirstName.clear()
        self.lineLastName.clear()
        self.comboGender.setCurrentIndex(0)
        self.comboProgramCode.setCurrentIndex(0)
        self.comboYearLevel.setCurrentIndex(0)

    #  Programs page
    def add_program(self):
        code         = self.lineProgramCode.text().strip()
        name         = self.lineProgramName.text().strip()
        college_code = self.comboCollegeCode.currentData()

        if not all([code, name, college_code]):
            QMessageBox.warning(self, "Input Error", "Please fill in all fields!")
            return

        try:
            self.csv.add_program(code, name, college_code)
            QMessageBox.information(self, "Success", "Program added successfully!")
            self.load_programs()
            self.populate_combo_boxes()
            self.clear_program_form()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def delete_program(self):
        selected = self.tablePrograms.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a program to delete!")
            return

        code = self.tablePrograms.item(selected, 0).text()
        if self.csv.program_has_students(code):
            QMessageBox.warning(self, "Error", "Cannot delete program. Students are enrolled in this program!")
            return

        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete program {code}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.csv.delete_program(code)
            QMessageBox.information(self, "Success", "Program deleted successfully!")
            self.load_programs()
            self.populate_combo_boxes()

    def clear_program_form(self):
        self.lineProgramCode.clear()
        self.lineProgramName.clear()
        self.comboCollegeCode.setCurrentIndex(0)

    #  Colleges page
    def add_college(self):
        code = self.lineCollegeCode.text().strip()
        name = self.lineCollegeName.text().strip()

        if not all([code, name]):
            QMessageBox.warning(self, "Input Error", "Please fill in all fields!")
            return

        try:
            self.csv.add_college(code, name)
            QMessageBox.information(self, "Success", "College added successfully!")
            self.load_colleges()
            self.populate_combo_boxes()
            self.clear_college_form()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def delete_college(self):
        selected = self.tableColleges.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a college to delete!")
            return

        code = self.tableColleges.item(selected, 0).text()
        if self.csv.college_has_programs(code):
            QMessageBox.warning(self, "Error", "Cannot delete college. Programs exist under this college!")
            return

        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete college {code}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.csv.delete_college(code)
            QMessageBox.information(self, "Success", "College deleted successfully!")
            self.load_colleges()
            self.populate_combo_boxes()

    def clear_college_form(self):
        self.lineCollegeCode.clear()
        self.lineCollegeName.clear()


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = EstudyoApp()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()