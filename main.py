import sys

from PyQt5.QtWidgets import (
    QApplication,
    QLineEdit,
    QLabel,
    QWidget,
    QVBoxLayout,
    QSpinBox,
    QPushButton,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
)

import mysql.connector

conn = mysql.connector.connect(
    host="localhost", user="javod", password="hHh(26Y2%C~w", database="oquv_markaz"
)

cursor = conn.cursor()


class Join_Dialog(QWidget):
    join_mode: str
    v_layout: QVBoxLayout
    join_table: QTableWidget

    def __init__(self, join_mode: str):
        self.join_mode = join_mode
        super().__init__()

        self.join_table = None

        self.setWindowTitle(self.join_mode)

        self.setMinimumSize(400, 300)

        self.init_ui()

    def init_ui(self):
        self.v_layout = QVBoxLayout()

        buttons_h_layout = QHBoxLayout()

        students_button = QPushButton("Students")
        students_button.clicked.connect(self.students)
        buttons_h_layout.addWidget(students_button)

        teachers_button = QPushButton("Teachers")
        teachers_button.clicked.connect(self.teachers)
        buttons_h_layout.addWidget(teachers_button)

        self.v_layout.addLayout(buttons_h_layout)
        self.setLayout(self.v_layout)

    def teachers(self):
        try:
            if self.join_mode == "UNION":
                cursor.execute(
                    "SELECT * FROM teachers LEFT JOIN students ON teachers.id = students.teacher_id "
                    + self.join_mode
                    + " SELECT * FROM teachers RIGHT JOIN students ON teachers.id = students.teacher_id;"
                )
            else:
                cursor.execute(
                    "SELECT * FROM teachers "
                    + self.join_mode
                    + " students ON teachers.id = students.teacher_id"
                )
            if self.join_table is None:
                self.join_table = QTableWidget()
                self.v_layout.addWidget(self.join_table)

            self.join_table.setColumnCount(5)
            self.join_table.setHorizontalHeaderLabels(
                [
                    "Teacher ID",
                    "Teacher Name",
                    "Student ID",
                    "Student Name",
                    "Student Age",
                ]
            )
            self.join_table.setRowCount(0)
            for row_idx, (
                teacher_id,
                teacher_name,
                student_id,
                student_name,
                student_age,
                t_id,
            ) in enumerate(cursor.fetchall()):
                self.join_table.insertRow(row_idx)
                self.join_table.setItem(row_idx, 0, QTableWidgetItem(str(teacher_id)))
                self.join_table.setItem(row_idx, 1, QTableWidgetItem(teacher_name))
                self.join_table.setItem(row_idx, 2, QTableWidgetItem(str(student_id)))
                self.join_table.setItem(row_idx, 3, QTableWidgetItem(student_name))
                self.join_table.setItem(row_idx, 4, QTableWidgetItem(str(student_age)))

        except Exception as exp:
            print(exp)

    def students(self):
        try:
            if self.join_mode == "UNION":
                cursor.execute(
                    "SELECT * FROM students LEFT JOIN teachers ON students.teacher_id = teachers.id "
                    + self.join_mode
                    + " SELECT * FROM students RIGHT JOIN teachers ON students.teacher_id = teachers.id;"
                )
            else:
                cursor.execute(
                    "SELECT * FROM students "
                    + self.join_mode
                    + " teachers ON students.teacher_id = teachers.id"
                )
            if self.join_table is None:
                self.join_table = QTableWidget()
                self.v_layout.addWidget(self.join_table)

            self.join_table.setColumnCount(5)
            self.join_table.setHorizontalHeaderLabels(
                [
                    "Student ID",
                    "Student Name",
                    "Student Age",
                    "Teacher ID",
                    "Teacher Name",
                ]
            )
            self.join_table.setRowCount(0)
            for row_idx, (
                student_id,
                student_name,
                student_age,
                teacher_id,
                t_id,
                teacher_name,
            ) in enumerate(cursor.fetchall()):
                self.join_table.insertRow(row_idx)
                self.join_table.setItem(row_idx, 0, QTableWidgetItem(str(student_id)))
                self.join_table.setItem(row_idx, 1, QTableWidgetItem(student_name))
                self.join_table.setItem(row_idx, 2, QTableWidgetItem(str(student_age)))
                self.join_table.setItem(row_idx, 3, QTableWidgetItem(str(teacher_id)))
                self.join_table.setItem(row_idx, 4, QTableWidgetItem(teacher_name))

        except Exception as exp:
            print(exp)


class OquvMarkazApp(QWidget):
    teacher_name: QLineEdit

    student_name: QLineEdit
    student_age: QSpinBox
    teacher_id: QSpinBox

    teacher_table: QTableWidget
    student_table: QTableWidget

    inner_join_dialog: Join_Dialog
    left_join_dialog: Join_Dialog
    right_join_dialog: Join_Dialog
    union_dialog: Join_Dialog

    def __init__(self):
        super().__init__()

        try:
            self.init_ui()
        except Exception as exp:
            print(exp)

    def init_ui(self):
        self.setWindowTitle("O'quv Markaz")

        v_layout = QVBoxLayout()

        self.teacher_name = QLineEdit(self)
        self.teacher_name.setPlaceholderText("Enter teacher name")
        v_layout.addWidget(self.teacher_name)

        add_teacher_button = QPushButton("Add Teacher", self)
        add_teacher_button.clicked.connect(self.add_teacher)
        v_layout.addWidget(add_teacher_button)

        self.student_name = QLineEdit(self)
        self.student_name.setPlaceholderText("Enter student name")
        v_layout.addWidget(self.student_name)

        age_h_layout = QHBoxLayout()
        age_label = QLabel("Student Age:")
        age_h_layout.addWidget(age_label)
        self.student_age = QSpinBox(self)
        self.student_age.setRange(9, 60)
        self.student_age.setSingleStep(1)
        age_h_layout.addWidget(self.student_age)
        v_layout.addLayout(age_h_layout)

        t_id_h_layout = QHBoxLayout()
        t_id_label = QLabel("Teacher ID:")
        t_id_h_layout.addWidget(t_id_label)
        self.teacher_id = QSpinBox(self)
        self.teacher_id.setMinimum(1)
        self.teacher_id.setSingleStep(1)
        t_id_h_layout.addWidget(self.teacher_id)
        v_layout.addLayout(t_id_h_layout)

        add_student_button = QPushButton("Add Student")
        add_student_button.clicked.connect(self.add_student)
        v_layout.addWidget(add_student_button)

        self.teacher_table = QTableWidget()
        self.teacher_table.setColumnCount(2)
        self.teacher_table.setHorizontalHeaderLabels(["Teacher ID", "Teacher Name"])
        v_layout.addWidget(self.teacher_table)

        self.student_table = QTableWidget()
        self.student_table.setColumnCount(4)
        self.student_table.setHorizontalHeaderLabels(
            ["Student ID", "Student Name", "Student Age", "Teacher ID"]
        )
        v_layout.addWidget(self.student_table)

        buttons_h_layout = QHBoxLayout()
        inner_join_button = QPushButton("INNER JOIN")
        inner_join_button.clicked.connect(self.inner_join)
        buttons_h_layout.addWidget(inner_join_button)

        left_join_button = QPushButton("LEFT JOIN")
        left_join_button.clicked.connect(self.left_join)
        buttons_h_layout.addWidget(left_join_button)

        right_join_button = QPushButton("RIGHT JOIN")
        right_join_button.clicked.connect(self.right_join)
        buttons_h_layout.addWidget(right_join_button)

        union__button = QPushButton("UNION")
        union__button.clicked.connect(self.union)
        buttons_h_layout.addWidget(union__button)

        v_layout.addLayout(buttons_h_layout)

        self.load_teachers()
        self.load_students()

        self.setLayout(v_layout)

        self.setStyleSheet(
            """
                QWidget {
                    font-size: 22px;
                }
            """
        )

    def union(self):
        self.union_dialog = Join_Dialog("UNION")
        self.union_dialog.show()

    def right_join(self):
        self.right_join_dialog = Join_Dialog("RIGHT JOIN")
        self.right_join_dialog.show()

    def left_join(self):
        self.left_join_dialog = Join_Dialog("LEFT JOIN")
        self.left_join_dialog.show()

    def inner_join(self):
        self.inner_join_dialog = Join_Dialog("INNER JOIN")
        self.inner_join_dialog.show()

    def load_teachers(self):
        self.teacher_table.setRowCount(0)
        cursor.execute("SELECT * FROM teachers")
        for row_idx, (teacher_id, name) in enumerate(cursor.fetchall()):
            self.teacher_table.insertRow(row_idx)
            self.teacher_table.setItem(row_idx, 0, QTableWidgetItem(str(teacher_id)))
            self.teacher_table.setItem(row_idx, 1, QTableWidgetItem(name))

    def load_students(self):
        self.student_table.setRowCount(0)
        cursor.execute("SELECT * FROM students")
        for row_idx, (student_id, name, age, teacher_id) in enumerate(
            cursor.fetchall()
        ):
            self.student_table.insertRow(row_idx)
            self.student_table.setItem(row_idx, 0, QTableWidgetItem(str(student_id)))
            self.student_table.setItem(row_idx, 1, QTableWidgetItem(name))
            self.student_table.setItem(row_idx, 2, QTableWidgetItem(str(age)))
            self.student_table.setItem(row_idx, 3, QTableWidgetItem(str(teacher_id)))

    def add_student(self):
        try:
            name = self.student_name.text()
            age = int(self.student_age.text())
            teacher_id = int(self.teacher_id.text())

            if name and age and teacher_id:
                cursor.execute(
                    "INSERT INTO students (name, age, teacher_id) VALUES (%s, %s, %s)",
                    (name, age, teacher_id),
                )
                conn.commit()
                self.student_name.clear()
                self.student_age.clear()
                self.teacher_id.clear()
                self.load_students()
        except Exception as exp:
            print(exp)

    def add_teacher(self):
        try:
            name = self.teacher_name.text()

            if name:
                cursor.execute("INSERT INTO teachers (name) VALUES (%s)", (name,))
                conn.commit()
                self.teacher_name.clear()
                self.load_teachers()
        except Exception as exp:
            print(exp)


def main():
    app = QApplication(sys.argv)
    window = OquvMarkazApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
