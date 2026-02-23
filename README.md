# Estudyo — Simple Student Information System
### CCC151 - Information Management

---

## Overview

**Estudyo** is a desktop-based Simple Student Information System (SSIS) built with Python and PyQt6. It allows users to manage student records, academic programs, and colleges through a clean and intuitive graphical interface. Data is stored locally using CSV files.

---

## Features

### Student Management
- Add, edit, and delete student records
- Student ID validation enforced in `XXXX-XXXX` format (digits only)
- Duplicate student ID detection
- Search students by Student ID, First Name, Last Name, or Program
- Sort students by any field

### Program Management
- Add, edit, and delete academic programs
- Program code restricted to letters, spaces, and parentheses — auto-uppercased
- Program name restricted to letters, spaces, and parentheses (no digits)

### College Management
- Add, edit, and delete colleges
- College code restricted to letters, spaces, and parentheses — auto-uppercased

### Cascading Null Handling
- Deleting a college sets affected programs' college to `-NULL-`
- Deleting a program sets affected students' program to `-NULL-`
- `-NULL-` values are displayed in **red bold** across all tables
- Edit dialogs correctly show `-NULL-` when a record has no assigned program/college

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3 | Core language |
| PyQt6 | GUI framework |
| Qt Designer (`.ui`) | UI layout |
| CSV | Local data storage |

---

## Project Structure

```
├── estudyo_app.py        # Main application logic
├── estudyo_main.ui       # Qt Designer UI layout
├── students.csv          # Student records
├── programs.csv          # Program records
├── colleges.csv          # College records
├── student.svg           # Student nav icon
├── program.svg           # Program nav icon
├── college.svg           # College nav icon
└── estudyo_logo.png/svg  # App logo
```

---

## How to Run

**1. Install dependencies:**
```bash
pip install PyQt6
```

**2. Run the application:**
```bash
python estudyo_app.py
```

> Make sure all CSV files and icon/SVG assets are in the same directory as `estudyo_app.py`.

---
