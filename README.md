# Student Management System
This is a simple Student Management System built using Python and PyQt6 for the GUI. The application allows you to manage student records stored in a SQLite database.  
## Libraries Used
1. sys: This is a built-in Python module that provides access to some variables used or maintained by the Python interpreter.  
2. sqlite3: This is a built-in Python module used to work with the SQLite database.  
3. PyQt6: This is a set of Python bindings for The Qt Company’s Qt application framework and runs on all platforms supported by Qt including Windows, macOS, Linux, iOS and Android.  
## Mechanism
The application provides a simple GUI to interact with the SQLite database. The main window displays a table of student records, each with an ID, Name, Course, and Mobile number. The application allows you to perform the following operations:  
* Insert: You can add a new student record by clicking on the "Add Student" button. This opens a dialog where you can enter the student's name, select their course from a dropdown, and enter their mobile number.  
* Search: You can search for a student by name by clicking on the "Search Student" button. This opens a dialog where you can enter the student's name. The application then queries the database for matching records and highlights them in the table.  
* Edit: You can edit a student record by clicking on a row in the table and then clicking the "Edit record" button. This opens a dialog pre-filled with the student's current details, which you can then edit.  
* Delete: You can delete a student record by clicking on a row in the table and then clicking the "Delete record" button. This opens a confirmation dialog. If you confirm the deletion, the application removes the record from the database.  
The application uses SQLite to store the student records. SQLite is a C library that provides a lightweight disk-based database. It doesn’t require a separate server process and allows accessing the database using a nonstandard variant of the SQL query language. Some applications can use SQLite for internal data storage.  
# Running the Application
To run the application, you need to have Python and PyQt6 installed. You can then run the application by executing the Python script in your terminal:
```commandline
python main.py
```

This will open the application window, where you can start managing student records.