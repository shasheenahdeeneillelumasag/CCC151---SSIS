import sys
import csv
import os
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import (
    QMessageBox, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel,
    QLineEdit, QComboBox, QPushButton,  QDialogButtonBox, QGroupBox
)
from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QPixmap, QIcon, QRegularExpressionValidator, QColor

# CSV file paths
COLLEGES_CSV = "colleges.csv"
PROGRAMS_CSV = "programs.csv"
STUDENTS_CSV = "students.csv"

NULL_DISPLAY = "-NULL-"

#  CSV Manager
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
            self.write_students([{
                "id": "2024-0001",
                "first_name": "Shasheenah Deeneille",
                "last_name": "Lumasag",
                "gender": "Female",
                "program_code": "BSCS",
                "year_level": "3",
            }])

    def read_colleges(self):  return self._read_csv(COLLEGES_CSV)
    def read_programs(self):  return self._read_csv(PROGRAMS_CSV)
    def read_students(self):  return self._read_csv(STUDENTS_CSV)

    def write_colleges(self, rows): self._write_csv(COLLEGES_CSV, ["code", "name"], rows)
    def write_programs(self, rows): self._write_csv(PROGRAMS_CSV, ["code", "name", "college_code"], rows)
    def write_students(self, rows): self._write_csv(STUDENTS_CSV, ["id", "first_name", "last_name", "gender", "program_code", "year_level"], rows)

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

    #  College operations
    def add_college(self, code, name):
        colleges = self.read_colleges()
        if any(c["code"] == code for c in colleges):
            raise ValueError("College code already exists!")
        colleges.append({"code": code, "name": name})
        self.write_colleges(colleges)

    def edit_college(self, old_code, new_code, new_name):
        colleges = self.read_colleges()
        if new_code != old_code and any(c["code"] == new_code for c in colleges):
            raise ValueError("College code already exists!")
        for c in colleges:
            if c["code"] == old_code:
                c["code"] = new_code
                c["name"] = new_name
        self.write_colleges(colleges)

        if old_code != new_code:
            programs = self.read_programs()
            for p in programs:
                if p["college_code"] == old_code:
                    p["college_code"] = new_code
            self.write_programs(programs)

    def delete_college(self, code):
        self.write_colleges([c for c in self.read_colleges() if c["code"] != code])
        programs = self.read_programs()
        for p in programs:
            if p["college_code"] == code:
                p["college_code"] = NULL_DISPLAY
        self.write_programs(programs)

    def college_has_programs(self, code):
        return any(p["college_code"] == code for p in self.read_programs())

    #  Program operations
    def add_program(self, code, name, college_code):
        programs = self.read_programs()
        if any(p["code"] == code for p in programs):
            raise ValueError("Program code already exists!")
        programs.append({"code": code, "name": name, "college_code": college_code})
        self.write_programs(programs)

    def edit_program(self, old_code, new_code, new_name, new_college_code):
        programs = self.read_programs()
        if new_code != old_code and any(p["code"] == new_code for p in programs):
            raise ValueError("Program code already exists!")
        for p in programs:
            if p["code"] == old_code:
                p["code"] = new_code
                p["name"] = new_name
                p["college_code"] = new_college_code
        self.write_programs(programs)

        if old_code != new_code:
            students = self.read_students()
            for s in students:
                if s["program_code"] == old_code:
                    s["program_code"] = new_code
            self.write_students(students)

    def delete_program(self, code):
        self.write_programs([p for p in self.read_programs() if p["code"] != code])

        students = self.read_students()
        for s in students:
            if s["program_code"] == code:
                s["program_code"] = NULL_DISPLAY
        self.write_students(students)

    def program_has_students(self, code):
        return any(s["program_code"] == code for s in self.read_students())

    #  Student operations
    def add_student(self, sid, first_name, last_name, gender, program_code, year_level):
        students = self.read_students()
        if any(s["id"] == sid for s in students):
            raise ValueError("Student ID already exists!")
        students.append({"id": sid, "first_name": first_name, "last_name": last_name,
                         "gender": gender, "program_code": program_code, "year_level": year_level})
        self.write_students(students)

    def edit_student(self, old_id, new_id, first_name, last_name, gender, program_code, year_level):
        students = self.read_students()
        if new_id != old_id and any(s["id"] == new_id for s in students):
            raise ValueError("Student ID already exists!")
        for s in students:
            if s["id"] == old_id:
                s["id"] = new_id
                s["first_name"] = first_name
                s["last_name"] = last_name
                s["gender"] = gender
                s["program_code"] = program_code
                s["year_level"] = year_level
        self.write_students(students)

    def delete_student(self, sid):
        self.write_students([s for s in self.read_students() if s["id"] != sid])

    def search_students(self, field, value):
        return [s for s in self.read_students() if value.lower() in s.get(field, "").lower()]

    def sort_students(self, field):
        return sorted(self.read_students(), key=lambda s: s.get(field, "").lower())

    def search_colleges(self, value):
        return [c for c in self.read_colleges() if
                value.lower() in c["code"].lower() or value.lower() in c["name"].lower()]

    def sort_colleges(self, field):
        return sorted(self.read_colleges(), key=lambda c: c.get(field, "").lower())

    def search_programs(self, value):
        return [p for p in self.read_programs() if
                value.lower() in p["code"].lower() or value.lower() in p["name"].lower() or
                value.lower() in p["college_code"].lower()]

    def sort_programs(self, field):
        return sorted(self.read_programs(), key=lambda p: p.get(field, "").lower())

#  Edit Dialogs
DIALOG_STYLE = """
QDialog { background-color: #f0f7ff; }
QGroupBox {
    background-color: white;
    border: 1px solid #bbdefb;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 12px;
    font-weight: bold;
    color: #1a3a5c;
    font-size: 14px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 4px 12px;
    color: #1a3a5c;
}
QLabel { color: #1a3a5c; font-weight: 600; font-size: 13px; }
QLineEdit, QComboBox {
    padding: 8px 12px;
    border: 1.5px solid #90caf9;
    border-radius: 6px;
    background-color: white;
    font-size: 13px;
    min-height: 32px;
}
QLineEdit:focus, QComboBox:focus { border: 1.5px solid #1976D2; }
QPushButton#btnSaveDialog {
    background-color: #1565C0;
    color: white;
    border-radius: 6px;
    padding: 9px 28px;
    font-size: 13px;
    font-weight: 700;
}
QPushButton#btnSaveDialog:hover { background-color: #0d47a1; }
QPushButton#btnCancelDialog {
    background-color: #eceff1;
    color: #37474f;
    border-radius: 6px;
    padding: 9px 28px;
    font-size: 13px;
    font-weight: 600;
}
QPushButton#btnCancelDialog:hover { background-color: #cfd8dc; }
"""

def _is_null(val):
    """Check if a value is a null sentinel."""
    return val.strip().upper() in ("-NULL-", "-Null-", "NULL", "")


def _apply_student_id_validator(line_edit):
    """Apply XXXX-XXXX numeric validator to a QLineEdit."""
    rx = QRegularExpression(r"^\d{0,4}-?\d{0,4}$")
    validator = QRegularExpressionValidator(rx)
    line_edit.setValidator(validator)

    def _format_on_change(text):
        digits = text.replace("-", "")
        if len(digits) > 4:
            formatted = digits[:4] + "-" + digits[4:8]
            if text != formatted:
                line_edit.blockSignals(True)
                line_edit.setText(formatted)
                line_edit.setCursorPosition(len(formatted))
                line_edit.blockSignals(False)

    line_edit.textChanged.connect(_format_on_change)


def _validate_student_id_format(sid):
    """Return True if sid matches XXXX-XXXX with only digits."""
    import re
    return bool(re.fullmatch(r"\d{4}-\d{4}", sid))


def _apply_code_validator(line_edit):
    """Restrict a QLineEdit to letters, spaces, and parentheses only — auto-uppercased."""
    rx = QRegularExpression(r"^[A-Za-z ()\s]*$")
    validator = QRegularExpressionValidator(rx)
    line_edit.setValidator(validator)
    line_edit.textChanged.connect(
        lambda t: (line_edit.blockSignals(True),
                   line_edit.setText(t.upper()),
                   line_edit.blockSignals(False))
        if t != t.upper() else None
    )


def _apply_name_validator(line_edit):
    """Restrict a QLineEdit to letters, spaces, and parentheses only — no digits or special chars. No auto-caps."""
    rx = QRegularExpression(r"^[A-Za-z ()\s]*$")
    validator = QRegularExpressionValidator(rx)
    line_edit.setValidator(validator)


class EditStudentDialog(QDialog):
    def __init__(self, parent, student, programs, all_students=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Student")
        self.setMinimumWidth(480)
        self.setStyleSheet(DIALOG_STYLE)
        self.student = student
        self.all_students = all_students or []

        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)

        grp = QGroupBox("Student Information")
        form = QFormLayout(grp)
        form.setSpacing(10)
        form.setContentsMargins(16, 20, 16, 16)

        self.lineId = QLineEdit(student["id"])
        _apply_student_id_validator(self.lineId)

        self.lineFirst = QLineEdit(student["first_name"])
        self.lineLast = QLineEdit(student["last_name"])
        self.comboGender = QComboBox()
        self.comboGender.addItems(["Male", "Female"])
        idx = self.comboGender.findText(student["gender"])
        if idx >= 0: self.comboGender.setCurrentIndex(idx)

        self.comboProgram = QComboBox()
        prog_code = student["program_code"]
        if _is_null(prog_code):
            self.comboProgram.addItem(NULL_DISPLAY, NULL_DISPLAY)
        for p in programs:
            self.comboProgram.addItem(f"{p['code']} - {p['name']}", p["code"])
        matched = False
        for i in range(self.comboProgram.count()):
            if self.comboProgram.itemData(i) == prog_code:
                self.comboProgram.setCurrentIndex(i)
                matched = True
                break
        if not matched:
            self.comboProgram.setCurrentIndex(0)

        self.comboYear = QComboBox()
        self.comboYear.addItems(["1", "2", "3", "4"])
        iy = self.comboYear.findText(student["year_level"])
        if iy >= 0: self.comboYear.setCurrentIndex(iy)

        form.addRow("Student ID:", self.lineId)
        form.addRow("First Name:", self.lineFirst)
        form.addRow("Last Name:", self.lineLast)
        form.addRow("Gender:", self.comboGender)
        form.addRow("Program:", self.comboProgram)
        form.addRow("Year Level:", self.comboYear)
        layout.addWidget(grp)

        btnRow = QHBoxLayout()
        btnRow.addStretch()
        btnSave = QPushButton("Save Changes")
        btnSave.setObjectName("btnSaveDialog")
        btnCancel = QPushButton("Cancel")
        btnCancel.setObjectName("btnCancelDialog")
        btnRow.addWidget(btnCancel)
        btnRow.addWidget(btnSave)
        layout.addLayout(btnRow)

        btnSave.clicked.connect(self._on_save)
        btnCancel.clicked.connect(self.reject)

    def _on_save(self):
        sid = self.lineId.text().strip()
        first = self.lineFirst.text().strip()
        last = self.lineLast.text().strip()

        if not all([sid, first, last]):
            QMessageBox.warning(self, "Input Error", "Please fill in all input fields.")
            return

        if not _validate_student_id_format(sid):
            QMessageBox.warning(self, "Invalid ID",
                                "Student ID must be in the format XXXX-XXXX (digits only, e.g. 2024-0001).")
            return

        old_id = self.student["id"]
        if sid != old_id:
            if any(s["id"] == sid for s in self.all_students):
                QMessageBox.warning(self, "Duplicate ID",
                                    f"Student ID '{sid}' already exists. Please use a different ID.")
                self.lineId.setStyleSheet("background-color: #ffebee; color: #c62828; border: 1.5px solid #c62828;")
                return

        self.accept()

    def get_data(self):
        return {
            "id": self.lineId.text().strip(),
            "first_name": self.lineFirst.text().strip(),
            "last_name": self.lineLast.text().strip(),
            "gender": self.comboGender.currentText(),
            "program_code": self.comboProgram.currentData(),
            "year_level": self.comboYear.currentText(),
        }

class EditCollegeDialog(QDialog):
    def __init__(self, parent, college):
        super().__init__(parent)
        self.setWindowTitle("Edit College")
        self.setMinimumWidth(420)
        self.setStyleSheet(DIALOG_STYLE)

        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)

        grp = QGroupBox("College Information")
        form = QFormLayout(grp)
        form.setSpacing(10)
        form.setContentsMargins(16, 20, 16, 16)

        self.lineCode = QLineEdit(college["code"])
        _apply_code_validator(self.lineCode)
        self.lineName = QLineEdit(college["name"])
        form.addRow("College Code:", self.lineCode)
        form.addRow("College Name:", self.lineName)
        layout.addWidget(grp)

        btnRow = QHBoxLayout()
        btnRow.addStretch()
        btnSave = QPushButton("Save Changes")
        btnSave.setObjectName("btnSaveDialog")
        btnCancel = QPushButton("Cancel")
        btnCancel.setObjectName("btnCancelDialog")
        btnRow.addWidget(btnCancel)
        btnRow.addWidget(btnSave)
        layout.addLayout(btnRow)

        btnSave.clicked.connect(self.accept)
        btnCancel.clicked.connect(self.reject)

    def get_data(self):
        return {"code": self.lineCode.text().strip(), "name": self.lineName.text().strip()}


class EditProgramDialog(QDialog):
    def __init__(self, parent, program, colleges):
        super().__init__(parent)
        self.setWindowTitle("Edit Program")
        self.setMinimumWidth(480)
        self.setStyleSheet(DIALOG_STYLE)

        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)

        grp = QGroupBox("Program Information")
        form = QFormLayout(grp)
        form.setSpacing(10)
        form.setContentsMargins(16, 20, 16, 16)

        self.lineCode = QLineEdit(program["code"])
        _apply_code_validator(self.lineCode)
        self.lineName = QLineEdit(program["name"])
        _apply_name_validator(self.lineName)
        self.comboCollege = QComboBox()

        coll_code = program["college_code"]
        if _is_null(coll_code):
            self.comboCollege.addItem(NULL_DISPLAY, NULL_DISPLAY)
        for c in colleges:
            self.comboCollege.addItem(f"{c['code']} - {c['name']}", c["code"])
        matched = False
        for i in range(self.comboCollege.count()):
            if self.comboCollege.itemData(i) == coll_code:
                self.comboCollege.setCurrentIndex(i)
                matched = True
                break
        if not matched:
            self.comboCollege.setCurrentIndex(0)

        form.addRow("Program Code:", self.lineCode)
        form.addRow("Program Name:", self.lineName)
        form.addRow("College:", self.comboCollege)
        layout.addWidget(grp)

        btnRow = QHBoxLayout()
        btnRow.addStretch()
        btnSave = QPushButton("Save Changes")
        btnSave.setObjectName("btnSaveDialog")
        btnCancel = QPushButton("Cancel")
        btnCancel.setObjectName("btnCancelDialog")
        btnRow.addWidget(btnCancel)
        btnRow.addWidget(btnSave)
        layout.addLayout(btnRow)

        btnSave.clicked.connect(self.accept)
        btnCancel.clicked.connect(self.reject)

    def get_data(self):
        return {
            "code": self.lineCode.text().strip(),
            "name": self.lineName.text().strip(),
            "college_code": self.comboCollege.currentData(),
        }


#  Main Application
class EstudyoApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.csv = CSVManager()
        uic.loadUi("estudyo_main.ui", self)
        self.setWindowIcon(QIcon("icons/estudyo_logo.svg"))

        self._current_students = None
        self._current_programs = None
        self._current_colleges = None

        self.setup_ui()
        self.setup_connections()
        self.load_initial_data()
        self.show()

    def setup_ui(self):
        self.setup_table_properties(self.tableStudents)
        self.setup_table_properties(self.tablePrograms)
        self.setup_table_properties(self.tableColleges)
        self.stackedWidget.setCurrentIndex(0)
        self.populate_combo_boxes()

        _apply_student_id_validator(self.lineStudentId)

        _apply_code_validator(self.lineCollegeCode)
        _apply_code_validator(self.lineProgramCode)
        _apply_name_validator(self.lineProgramName)

        # Load logo
        for path in ["icons/estudyo_logo.svg", "estudyo_logo.svg", "icons/estudyo_logo.png", "estudyo_logo.png"]:
            if os.path.exists(path):
                pixmap = QPixmap(path)
                self.logoLabel.setPixmap(
                    pixmap.scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                )
                self.logoLabel.setScaledContents(False)
                break

        self._apply_extra_styles()

    def _apply_extra_styles(self):
        extra_qss = """
        /* ── Sidebar nav ── */
        QPushButton#navButton, QPushButton#btnManage,
        QPushButton#btnPrograms, QPushButton#btnColleges {
            background-color: transparent;
            color: #e8f4fd;
            border: none;
            border-left: 4px solid transparent;
            text-align: left;
            padding: 14px 20px 14px 20px;
            font-size: 14px;
            font-weight: 600;
            min-width: 220px;
        }
        QPushButton#navButton:hover, QPushButton#btnManage:hover,
        QPushButton#btnPrograms:hover, QPushButton#btnColleges:hover {
            background-color: rgba(255,255,255,0.12);
            border-left: 4px solid #64b5f6;
        }
        QPushButton#navButton:checked, QPushButton#btnManage:checked,
        QPushButton#btnPrograms:checked, QPushButton#btnColleges:checked {
            background-color: rgba(255,255,255,0.18);
            border-left: 4px solid #42a5f5;
            color: white;
        }

        /* ── Search / Sort (blue) ── */
        QPushButton#btnSearch, QPushButton#btnSort {
            background-color: #1565C0;
            color: white;
            border-radius: 6px;
            padding: 8px 18px;
            font-weight: 700;
        }
        QPushButton#btnSearch:hover, QPushButton#btnSort:hover {
            background-color: #0d47a1;
        }

        /* ── Edit (teal-blue) ── */
        QPushButton#btnEdit {
            background-color: #0288d1;
            color: white;
            border-radius: 6px;
            padding: 8px 18px;
            font-weight: 700;
        }
        QPushButton#btnEdit:hover { background-color: #01579b; }

        /* ── Delete (red) ── */
        QPushButton#btnDelete {
            background-color: #c62828;
            color: white;
            border-radius: 6px;
            padding: 8px 18px;
            font-weight: 700;
        }
        QPushButton#btnDelete:hover { background-color: #b71c1c; }

        /* ── Add / Save (green-blue) ── */
        QPushButton#btnAdd {
            background-color: #1976D2;
            color: white;
            border-radius: 6px;
            padding: 8px 20px;
            font-weight: 700;
        }
        QPushButton#btnAdd:hover { background-color: #1565C0; }

        /* ── Clear (grey-blue) ── */
        QPushButton#btnClear {
            background-color: #546e7a;
            color: white;
            border-radius: 6px;
            padding: 8px 18px;
            font-weight: 700;
        }
        QPushButton#btnClear:hover { background-color: #37474f; }

        /* ── Search/filter row labels ── */
        QFrame#searchFrame QLabel { color: #1a3a5c; font-weight: 600; }

        /* ── Header ── */
        QFrame#headerFrame { background-color: #1a3a5c; }
        QLabel#headerTitle { color: #1a3a5c; font-size: 26px; font-weight: bold; padding-left: 16px; }

        /* ── Table header ── */
        QHeaderView::section {
            background-color: #1565C0;
            color: white;
            padding: 10px;
            border: none;
            border-right: 1px solid #1976D2;
            font-weight: 700;
            font-size: 13px;
        }
        QTableWidget::item:selected { background-color: #bbdefb; color: #0d1b2a; }
        """
        self.setStyleSheet(self.styleSheet() + extra_qss)

    def setup_table_properties(self, table):
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)

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
        self.navButton.clicked.connect(lambda: self.switch_page(0, "Dashboard"))
        self.btnManage.clicked.connect(lambda: self.switch_page(1, "Students"))
        self.btnPrograms.clicked.connect(lambda: self.switch_page(2, "Programs"))
        self.btnColleges.clicked.connect(lambda: self.switch_page(3, "Colleges"))

        self.btnSearch.clicked.connect(self.search_students)
        self.btnSort.clicked.connect(self.sort_students)
        self.btnEdit.clicked.connect(self.edit_student_from_dashboard)
        self.btnDelete.clicked.connect(self.delete_student_from_dashboard)

        self.btnAddStudent.clicked.connect(self.add_student)
        self.btnClearStudent.clicked.connect(self.clear_student_form)

        self.btnAddProgram.clicked.connect(self.add_program)
        self.btnClearProgram.clicked.connect(self.clear_program_form)
        self.btnEditProgram.clicked.connect(self.edit_program_from_table)
        self.btnDeleteProgram.clicked.connect(self.delete_program)

        self.btnAddCollege.clicked.connect(self.add_college)
        self.btnClearCollege.clicked.connect(self.clear_college_form)
        self.btnEditCollege.clicked.connect(self.edit_college_from_table)
        self.btnDeleteCollege.clicked.connect(self.delete_college)

        self.btnSearchProgram.clicked.connect(self.search_programs_table)
        self.btnSortProgram.clicked.connect(self.sort_programs_table)
        self.btnSearchCollege.clicked.connect(self.search_colleges_table)
        self.btnSortCollege.clicked.connect(self.sort_colleges_table)

    #  Navigation
    def switch_page(self, index, title):
        self.stackedWidget.setCurrentIndex(index)
        self.headerTitle.setText(title)
        for i, btn in enumerate([self.navButton, self.btnManage, self.btnPrograms, self.btnColleges]):
            btn.setChecked(i == index)
        if index == 0:
            self.load_students()
        elif index == 2:
            self._current_programs = None
            self.load_programs()
        elif index == 3:
            self._current_colleges = None
            self.load_colleges()

    def load_initial_data(self):
        self.load_colleges()
        self.load_programs()
        self.load_students()

    def _make_null_item(self, val):
        """Create a red, bold table item for null values."""
        item = QTableWidgetItem(NULL_DISPLAY)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setForeground(QColor("#c62828"))
        font = item.font()
        font.setBold(True)
        item.setFont(font)
        return item

    def _make_item(self, val):
        """Create a standard or null table item based on value."""
        normalized = val.strip().upper()
        if normalized in ("-NULL-", "NULL", ""):
            return self._make_null_item(val)
        item = QTableWidgetItem(val)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        return item

    #  Data loaders
    def load_students(self, students=None):
        if students is None:
            students = self.csv.read_students()
        self._current_students = students
        self.tableStudents.setRowCount(0)
        for r, s in enumerate(students):
            self.tableStudents.insertRow(r)
            for c, val in enumerate([s["id"], s["first_name"], s["last_name"], s["program_code"], s["year_level"], s["gender"]]):
                self.tableStudents.setItem(r, c, self._make_item(val))

    def load_programs(self, programs=None):
        if programs is None:
            programs = self.csv.read_programs()
        self._current_programs = programs
        self.tablePrograms.setRowCount(0)
        for r, p in enumerate(programs):
            self.tablePrograms.insertRow(r)
            for c, val in enumerate([p["code"], p["name"], p["college_code"]]):
                self.tablePrograms.setItem(r, c, self._make_item(val))

    def load_colleges(self, colleges=None):
        if colleges is None:
            colleges = self.csv.read_colleges()
        self._current_colleges = colleges
        self.tableColleges.setRowCount(0)
        for r, col in enumerate(colleges):
            self.tableColleges.insertRow(r)
            for c, val in enumerate([col["code"], col["name"]]):
                self.tableColleges.setItem(r, c, self._make_item(val))

    #  Dashboard / Students
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
        results = self.csv.search_students(field, value)
        self.load_students(results)
        if not results:
            QMessageBox.information(self, "No Results", "No students found matching your search.")

    def sort_students(self):
        field_map = {
            "Student ID": "id",
            "First Name": "first_name",
            "Last Name": "last_name",
            "Program": "program_code",
            "Year Level": "year_level",
        }
        field = field_map.get(self.comboSortField.currentText(), "id")
        base = self._current_students if self._current_students is not None else self.csv.read_students()
        sorted_data = sorted(base, key=lambda s: s.get(field, "").lower())
        self.load_students(sorted_data)

    def _refresh_students_view(self):
        """Re-apply current search filter then reload — used after edit/delete."""
        field_map = {
            "Student ID": "id",
            "First Name": "first_name",
            "Last Name": "last_name",
            "Program": "program_code",
        }
        value = self.lineSearchInput.text().strip()
        if value:
            field = field_map.get(self.comboSearchField.currentText(), "id")
            results = self.csv.search_students(field, value)
        else:
            results = self.csv.read_students()
        self.load_students(results)

    def edit_student_from_dashboard(self):
        selected = self.tableStudents.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "No Selection", "Please select a student to edit.")
            return

        sid          = self.tableStudents.item(selected, 0).text()
        first_name   = self.tableStudents.item(selected, 1).text()
        last_name    = self.tableStudents.item(selected, 2).text()
        program_code = self.tableStudents.item(selected, 3).text()
        year_level   = self.tableStudents.item(selected, 4).text()
        gender       = self.tableStudents.item(selected, 5).text()

        if program_code.strip().upper() in ("-NULL-", "NULL"):
            program_code = NULL_DISPLAY

        student = {
            "id": sid, "first_name": first_name, "last_name": last_name,
            "gender": gender, "program_code": program_code, "year_level": year_level
        }
        programs = self.csv.read_programs()
        all_students = self.csv.read_students()
        dialog = EditStudentDialog(self, student, programs, all_students)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if not all([data["id"], data["first_name"], data["last_name"]]):
                QMessageBox.warning(self, "Input Error", "Please fill in all input fields.")
                return
            try:
                self.csv.edit_student(
                    sid, data["id"], data["first_name"], data["last_name"],
                    data["gender"], data["program_code"], data["year_level"]
                )
                QMessageBox.information(self, " Success", "Student updated successfully!")
                self._refresh_students_view()
            except ValueError as e:
                QMessageBox.warning(self, "Error", str(e))

    def delete_student_from_dashboard(self):
        selected = self.tableStudents.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "No Selection", "Please select a student to delete.")
            return
        sid = self.tableStudents.item(selected, 0).text()
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete student {sid}?\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.csv.delete_student(sid)
            QMessageBox.information(self, " Deleted", "Student deleted successfully!")
            self._refresh_students_view()

    #  Manage Students
    def add_student(self):
        sid          = self.lineStudentId.text().strip()
        first_name   = self.lineFirstName.text().strip()
        last_name    = self.lineLastName.text().strip()
        gender       = self.comboGender.currentText()
        program_code = self.comboProgramCode.currentData()
        year_level   = self.comboYearLevel.currentText()

        if not all([sid, first_name, last_name, gender, program_code]):
            QMessageBox.warning(self, "Input Error", "Please fill in all input fields.")
            return

        if not _validate_student_id_format(sid):
            QMessageBox.warning(self, "Invalid ID",
                                "Student ID must be in the format XXXX-XXXX (digits only, e.g. 2024-0001).")
            return

        try:
            self.csv.add_student(sid, first_name, last_name, gender, program_code, year_level)
            QMessageBox.information(self, " Success", "Student added successfully!")
            self.clear_student_form()
            self.load_students()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def clear_student_form(self):
        self.lineStudentId.clear()
        self.lineFirstName.clear()
        self.lineLastName.clear()
        self.comboGender.setCurrentIndex(0)
        self.comboProgramCode.setCurrentIndex(0)
        self.comboYearLevel.setCurrentIndex(0)

    #  Programs
    def add_program(self):
        code         = self.lineProgramCode.text().strip().upper()
        name         = self.lineProgramName.text().strip()
        college_code = self.comboCollegeCode.currentData()
        if not all([code, name, college_code]):
            QMessageBox.warning(self, "Input Error", "Please fill in all input fields.")
            return
        try:
            self.csv.add_program(code, name, college_code)
            QMessageBox.information(self, " Success", "Program added successfully!")
            self.load_programs()
            self.populate_combo_boxes()
            self.clear_program_form()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def edit_program_from_table(self):
        selected = self.tablePrograms.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "No Selection", "Please select a program to edit.")
            return
        code = self.tablePrograms.item(selected, 0).text()
        name = self.tablePrograms.item(selected, 1).text()
        college_code = self.tablePrograms.item(selected, 2).text()
        if college_code.strip().upper() in ("-NULL-", "NULL"):
            college_code = NULL_DISPLAY
        program = {"code": code, "name": name, "college_code": college_code}
        colleges = self.csv.read_colleges()
        dialog = EditProgramDialog(self, program, colleges)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if not all([data["code"], data["name"]]):
                QMessageBox.warning(self, "Input Error", "Please fill in all input fields.")
                return
            try:
                self.csv.edit_program(code, data["code"], data["name"], data["college_code"])
                QMessageBox.information(self, " Success", "Program updated successfully!")

                self._refresh_programs_view()
                self.populate_combo_boxes()
            except ValueError as e:
                QMessageBox.warning(self, "Error", str(e))

    def delete_program(self):
        selected = self.tablePrograms.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "No Selection", "Please select a program to delete.")
            return
        code = self.tablePrograms.item(selected, 0).text()
        has_students = self.csv.program_has_students(code)
        msg = (f"Are you sure you want to delete program '{code}'?\n\n"
               + ("  Students enrolled in this program will have their program set to null."
                  if has_students else ""))
        reply = QMessageBox.question(self, "Confirm Delete", msg, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.csv.delete_program(code)
            QMessageBox.information(self, " Deleted", "Program deleted successfully!")
            self._refresh_programs_view()
            self.populate_combo_boxes()

    def clear_program_form(self):
        self.lineProgramCode.clear()
        self.lineProgramName.clear()
        self.comboCollegeCode.setCurrentIndex(0)

    def search_programs_table(self):
        value = self.lineSearchProgram.text().strip()
        if not value:
            self.load_programs()
            return
        results = self.csv.search_programs(value)
        self.load_programs(results)
        if not results:
            QMessageBox.information(self, "No Results", "No programs found matching your search.")

    def sort_programs_table(self):
        field_map = {"Program Code": "code", "Program Name": "name", "College Code": "college_code"}
        field = field_map.get(self.comboSortProgram.currentText(), "code")
        base = self._current_programs if self._current_programs is not None else self.csv.read_programs()
        sorted_data = sorted(base, key=lambda p: p.get(field, "").lower())
        self.load_programs(sorted_data)

    def _refresh_programs_view(self):
        """Re-apply current search then sort to refresh programs table."""
        value = self.lineSearchProgram.text().strip()
        if value:
            results = self.csv.search_programs(value)
        else:
            results = self.csv.read_programs()
        self.load_programs(results)

    #  Colleges
    def add_college(self):
        code = self.lineCollegeCode.text().strip().upper()
        name = self.lineCollegeName.text().strip()
        if not all([code, name]):
            QMessageBox.warning(self, "Input Error", "Please fill in all input fields.")
            return
        try:
            self.csv.add_college(code, name)
            QMessageBox.information(self, " Success", "College added successfully!")
            self.load_colleges()
            self.populate_combo_boxes()
            self.clear_college_form()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def edit_college_from_table(self):
        selected = self.tableColleges.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "No Selection", "Please select a college to edit.")
            return
        code = self.tableColleges.item(selected, 0).text()
        name = self.tableColleges.item(selected, 1).text()
        college = {"code": code, "name": name}
        dialog = EditCollegeDialog(self, college)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if not all([data["code"], data["name"]]):
                QMessageBox.warning(self, "Input Error", "Please fill in all input fields.")
                return
            try:
                self.csv.edit_college(code, data["code"], data["name"])
                QMessageBox.information(self, " Success", "College updated successfully!")
                self._refresh_colleges_view()
                self.populate_combo_boxes()
            except ValueError as e:
                QMessageBox.warning(self, "Error", str(e))

    def delete_college(self):
        selected = self.tableColleges.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "No Selection", "Please select a college to delete.")
            return
        code = self.tableColleges.item(selected, 0).text()
        has_programs = self.csv.college_has_programs(code)
        msg = (f"Are you sure you want to delete college '{code}'?\n\n"
               + ("  Programs under this college will have their college set to null."
                  if has_programs else ""))
        reply = QMessageBox.question(self, "Confirm Delete", msg,
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.csv.delete_college(code)
            QMessageBox.information(self, " Deleted", "College deleted successfully!")
            self._refresh_colleges_view()
            self.populate_combo_boxes()

    def clear_college_form(self):
        self.lineCollegeCode.clear()
        self.lineCollegeName.clear()

    def search_colleges_table(self):
        value = self.lineSearchCollege.text().strip()
        if not value:
            self.load_colleges()
            return
        results = self.csv.search_colleges(value)
        self.load_colleges(results)
        if not results:
            QMessageBox.information(self, "No Results", "No colleges found matching your search.")

    def sort_colleges_table(self):
        field_map = {"College Code": "code", "College Name": "name"}
        field = field_map.get(self.comboSortCollege.currentText(), "code")
        base = self._current_colleges if self._current_colleges is not None else self.csv.read_colleges()
        sorted_data = sorted(base, key=lambda c: c.get(field, "").lower())
        self.load_colleges(sorted_data)

    def _refresh_colleges_view(self):
        """Re-apply current search to refresh colleges table."""
        value = self.lineSearchCollege.text().strip()
        if value:
            results = self.csv.search_colleges(value)
        else:
            results = self.csv.read_colleges()
        self.load_colleges(results)


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    win = EstudyoApp()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()