import sys
import sqlite3
from PyQt6.QtWidgets import (QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton,
                             QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox, QToolBar,
                             QStatusBar, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon


class DatabaseConnection():
    def __init__(self, database_file="database.db"):
        self.database_file = database_file

    def connect(self):
        connection = sqlite3.connect(self.database_file)
        return connection

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 600)

        # Create menu items
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # Create actions for menu items
        add_student_action = QAction(QIcon("icons/icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)

        search_action = QAction(QIcon("icons/icons/search.png"), "Search Student", self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

        # Create table widget
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.horizontalHeader().setStyleSheet('QHeaderView::section { background-color: green }')
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Create toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        # Add actions to toolbar
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # Create status bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Connect cell click event to function
        self.table.cellClicked.connect(self.cell_clicked)

    def about(self):
        # Show about dialog
        dialog = AboutDialog()
        dialog.exec()

    def cell_clicked(self):
        # Create buttons for editing and deleting records
        edit_button = QPushButton("Edit record")
        edit_button.clicked.connect(self.edit)
        delete_button = QPushButton("Delete record")
        delete_button.clicked.connect(self.delete)

        # Remove existing buttons from status bar
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        # Add buttons to status bar
        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def edit(self):
        # Show edit dialog
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        # Show delete dialog
        dialog = DeleteDialog()
        dialog.exec()

    def load_data(self):
        # Load data from database and populate table
        connection = DatabaseConnection().connect()
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        # Show insert dialog
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        # Show search dialog
        dialog = SearchDialog()
        dialog.exec()

class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
        This mini app was created for the demonstration of GUI and Database manipulation!
        This mini app was developed by Phuc Le, with guidance from Ardit Sulce!
        """
        self.setText(content)


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Dialog")  # Set the window title
        self.setFixedWidth(300)  # Set the fixed width of the window
        self.setFixedHeight(300)  # Set the fixed height of the window

        layout = QVBoxLayout()  # Create a vertical box layout

        self.student_name = QLineEdit()  # Create a line edit for student name
        self.student_name.setPlaceholderText("Name")  # Set placeholder text
        layout.addWidget(self.student_name)  # Add the line edit to the layout

        button = QPushButton("Search")  # Create a search button
        button.clicked.connect(self.search_student)  # Connect the button click to the search_student function
        layout.addWidget(button)  # Add the button to the layout
        self.setLayout(layout)  # Set the layout of the dialog

    def search_student(self):
        name = self.student_name.text()  # Get the text from the line edit
        connection = DatabaseConnection().connect()  # Connect to the database
        cursor = connection.cursor()  # Create a cursor
        # Execute a SQL query to search for students with the given name
        result = cursor.execute("SELECT * FROM students WHERE name LIKE ?", (f'%{name}%',))
        rows = list(result)  # Convert the result to a list
        print(rows)  # Print the rows
        # Find items in the table with the given name
        items = student_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)

        for item in items:
            print(item)  # Print the item
            # Select the item in the table
            student_window.table.item(item.row(), 1).setSelected(True)

        cursor.close()  # Close the cursor
        connection.close()  # Close the connection


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Dialog")  # Set the window title
        self.setFixedWidth(300)  # Set the fixed width of the window
        self.setFixedHeight(300)  # Set the fixed height of the window

        layout = QVBoxLayout()  # Create a vertical box layout
        index = student_window.table.currentRow()  # Get the current row in the table
        student_name = student_window.table.item(index, 1).text()  # Get the student name from the table
        self.student_id = student_window.table.item(index, 0).text()  # Get the student id from the table

        self.student_name = QLineEdit(student_name)  # Create a line edit with the student name
        self.student_name.setPlaceholderText("Name")  # Set placeholder text
        layout.addWidget(self.student_name)  # Add the line edit to the layout

        course_name = student_window.table.item(index, 2).text()  # Get the course name from the table
        self.student_course = QComboBox()  # Create a combo box for the course
        courses = ['Biology', 'Math', 'Astronomy', 'Physics']  # List of courses
        self.student_course.addItems(courses)  # Add the courses to the combo box
        self.student_course.setCurrentText(course_name)  # Set the current text to the course name
        layout.addWidget(self.student_course)  # Add the combo box to the layout

        student_mobile = student_window.table.item(index, 3).text()  # Get the student mobile from the table
        self.student_mobile = QLineEdit(student_mobile)  # Create a line edit with the student mobile
        self.student_mobile.setPlaceholderText("Mobile Phone")  # Set placeholder text
        layout.addWidget(self.student_mobile)  # Add the line edit to the layout

        button = QPushButton("Update")  # Create an update button
        button.clicked.connect(self.update_student)  # Connect the button click to the update_student function
        layout.addWidget(button)  # Add the button to the layout

        self.setLayout(layout)  # Set the layout of the dialog

    def update_student(self):
        connection = DatabaseConnection().connect()  # Connect to the database
        cursor = connection.cursor()  # Create a cursor
        # Execute a SQL query to update the student with the given id
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?", (
            self.student_name.text(), self.student_course.itemText(self.student_course.currentIndex()),
            self.student_mobile.text(), self.student_id))
        connection.commit()  # Commit the changes
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection

        student_window.load_data()  # Load the data in the student window


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Dialog")  # Set the window title

        layout = QGridLayout()  # Create a grid layout
        confirmation = QLabel("Are you sure you want to delete?")  # Create a label with a confirmation message
        yes = QPushButton("Yes")  # Create a yes button
        no = QPushButton("No")  # Create a no button
        layout.addWidget(confirmation, 0, 0, 1, 2)  # Add the label to the layout
        layout.addWidget(yes, 1, 0)  # Add the yes button to the layout
        layout.addWidget(no, 1, 1)  # Add the no button to the layout
        self.setLayout(layout)  # Set the layout of the dialog
        yes.clicked.connect(self.delete_student)  # Connect the yes button click to the delete_student function

    def delete_student(self):
        index = student_window.table.currentRow()  # Get the current row in the table
        student_id = student_window.table.item(index, 0).text()  # Get the student id from the table
        connection = DatabaseConnection().connect()  # Connect to the database
        cursor = connection.cursor()  # Create a cursor
        # Execute a SQL query to delete the student with the given id
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        connection.commit()  # Commit the changes
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection
        student_window.load_data()  # Load the data in the student window
        self.close()  # Close the dialog
        confirmation_widget = QMessageBox()  # Create a message box
        confirmation_widget.setWindowTitle("Success")  # Set the window title
        confirmation_widget.setText("The record was deleted successfully!")  # Set the text
        confirmation_widget.exec()  # Show the message box


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Dialog")  # Set the window title
        self.setFixedWidth(300)  # Set the fixed width of the window
        self.setFixedHeight(300)  # Set the fixed height of the window

        layout = QVBoxLayout()  # Create a vertical box layout

        self.student_name = QLineEdit()  # Create a line edit for student name
        self.student_name.setPlaceholderText("Name")  # Set placeholder text
        layout.addWidget(self.student_name)  # Add the line edit to the layout

        self.student_course = QComboBox()  # Create a combo box for the course
        courses = ['Biology', 'Math', 'Astronomy', 'Physics']  # List of courses
        self.student_course.addItems(courses)  # Add the courses to the combo box
        layout.addWidget(self.student_course)  # Add the combo box to the layout

        self.student_mobile = QLineEdit()  # Create a line edit for student mobile
        self.student_mobile.setPlaceholderText("Mobile Phone")  # Set placeholder text
        layout.addWidget(self.student_mobile)  # Add the line edit to the layout

        button = QPushButton("Register")  # Create a register button
        button.clicked.connect(self.add_student)  # Connect the button click to the add_student function
        layout.addWidget(button)  # Add the button to the layout

        self.setLayout(layout)  # Set the layout of the dialog

    def add_student(self):
        name = self.student_name.text()  # Get the text from the line edit
        course = self.student_course.itemText(self.student_course.currentIndex())  # Get the selected course
        mobile = self.student_mobile.text()  # Get the text from the line edit
        connection = DatabaseConnection().connect()  # Connect to the database
        cursor = connection.cursor()  # Create a cursor
        # Execute a SQL query to insert a new student
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)", (name, course, mobile))
        connection.commit()  # Commit the changes
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection
        student_window.load_data()  # Load the data in the student window



app = QApplication(sys.argv)
student_window = MainWindow()
student_window.show()
student_window.load_data()
sys.exit(app.exec())