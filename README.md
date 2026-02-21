# Estudyo – Student Information System
Version 2.0 | Built with Python + PyQt6

# Overview
Estudyo is a desktop Student Information System that lets you manage students, academic programs, and colleges through a clean, user-friendly interface. All data is stored locally in CSV files — no database required.

## Features

###  Dashboard (Students)
- View all students in a sortable, searchable table
- Search by Student ID, First Name, Last Name, or Program
- Sort by any column (toggle ascending/descending)
- Edit student details via a dialog box
- Delete a student with a confirmation dialog

###  Add Student
- Add a new student with: ID, First Name, Last Name, Gender, Program, Year Level
- Dropdown for Program (auto-populated from programs list)
- Clear Form button to reset fields

###  Manage Programs
- Add, Edit, and Delete academic programs
- Search programs by code, name, or college
- Sort by Program Code, Program Name, or College Code
- Editing opens a dialog box — changes are saved in-place
-  Deleting a program sets affected students' `program_code` to `NULL` (no data loss)

###  Manage Colleges
- Add, Edit, and Delete colleges
- Search by college code or name
- Sort by College Code or College Name
- Editing opens a dialog box — cascade-updates program records
- Deleting a college sets affected programs' `college_code` to `NULL` (no data loss)

##  Design
- Blue / Dark Blue / Light Blue color palette (`#1a3a5c`, `#2980b9`, `#d6eaf8`)
- Color-coded action buttons:
  - 🟢 Green — Add / Save
  - 🟠 Orange — Edit
  - 🔴 Red — Delete
  - 🔵 Blue — Search / Sort / Refresh
  - ⚫ Gray — Clear Form
- Alternating row colors and clean table headers

##  File Structure
📂 project/
├── estudyo_app.py       ← Main application (run this)
├── colleges.csv         ← College data
├── programs.csv         ← Program data
├── students.csv         ← Student data
├── estudyo_logo.svg     ← App logo (optional)
├── student.svg          ← Icon (optional)
├── program.svg          ← Icon (optional)
├── college.svg          ← Icon (optional)
└── README.md            ← This file

## 🚀 How to Run

### Requirements
- Python 3.8 or higher
- PyQt6

### Installation
```bash
pip install PyQt6
```

### Run the Application
```bash
python estudyo_app.py
```

**Note:** CSV files are created automatically on first run if they don't exist.

---

##  Tips
- Click a row in any table to select it before editing or deleting.
- Press Enter in any search box to trigger the search.
- Sort buttons toggle between ascending and descending order.
- All changes are saved immediately to CSV.
