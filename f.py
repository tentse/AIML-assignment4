import mysql.connector
from tkinter import *
from tkinter import messagebox
from datetime import datetime, timedelta

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ten-tsering",
    database="hostel_db"
)
cursor = conn.cursor()

# Create students table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    roll_no VARCHAR(20) PRIMARY KEY NOT NULL,
    name VARCHAR(100),
    phone_number VARCHAR(20),
    address VARCHAR(255),
    room_type ENUM('3-sharing', '2-sharing'),
    semester INT,
    course_type VARCHAR(50),
    branch VARCHAR(50),
    due_amount DECIMAL(10, 2),
    deadline DATE,
    joining_date DATE
)
""")

# Create left_students table if not exists
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS left_students (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     roll_no VARCHAR(20) NOT NULL,
#     name VARCHAR(100),
#     phone_number VARCHAR(20),
#     address VARCHAR(255),
#     room_type ENUM('3-sharing', '2-sharing'),
#     semester INT,
#     course_type VARCHAR(50),
#     branch VARCHAR(50),
#     joining_date DATE,
#     leaving_date DATE,
#     FOREIGN KEY (roll_no) REFERENCES students(roll_no) ON DELETE CASCADE
# )
# """)

cursor.execute("""
CREATE TABLE IF NOT EXISTS students_left (
    id INT AUTO_INCREMENT PRIMARY KEY,
    roll_no VARCHAR(20),
    name VARCHAR(100),
    joining_date DATE,
    leaving_date DATE,
)
""")

# Function to book a hostel room
def book_room():
    name = name_entry.get()
    roll_no = roll_no_entry.get()
    phone_number = phone_entry.get()
    address = address_entry.get()
    room_type = room_type_var.get()
    semester = int(semester_entry.get())
    course_type = course_entry.get()
    branch = branch_entry.get()

    deadline = datetime.now() + timedelta(days=30)  # Assuming a 30-day deadline
    joining_date = datetime.now().date()  # Current date as the joining date

    sql = "INSERT INTO students (roll_no, name, phone_number, address, room_type, semester, course_type, branch, due_amount, deadline, joining_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    if room_type == "3-sharing":
        cursor.execute(sql, (roll_no, name, phone_number, address, room_type, semester, course_type, branch, 70000.00, deadline, joining_date))
    else:
        cursor.execute(sql, (roll_no, name, phone_number, address, room_type, semester, course_type, branch, 90000.00, deadline, joining_date))
    conn.commit()
    messagebox.showinfo("Success", "Room booked successfully!")

# Function to evacuate from the hostel
def evacuate_from_hostel():
    roll_no = evacuate_roll_no_entry.get()

    # Fetch student details by roll number
    sql_fetch_student = "SELECT * FROM students WHERE roll_no = %s"
    cursor.execute(sql_fetch_student, (roll_no,))
    student = cursor.fetchone()

    if student:
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to evacuate from the hostel?")
        if confirm:
            # Insert student details into left_students table
            sql_insert_left_student = "INSERT INTO students_left (roll_no, name, joining_date, leaving_date) VALUES (%s, %s, %s, %s)"
            leaving_date = datetime.now().date()
            
            print(sql_insert_left_student)
            cursor.execute(sql_insert_left_student, (student[0], student[1],student[10], leaving_date))
            conn.commit()


            #Delete student from students table
            sql_delete_student = "DELETE FROM students WHERE roll_no = %s"
            cursor.execute(sql_delete_student, (roll_no,))
            conn.commit()

            messagebox.showinfo("Success", "Evacuation successful.")
        else:
            messagebox.showinfo("Cancelled", "Evacuation cancelled.")
    else:
        messagebox.showinfo("Not Found", "Student not found.")

# Function to display all student details
def display_student_details():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    if students:
        for student in students:
            print(f"Roll No: {student[0]}, Name: {student[1]}, Phone Number: {student[2]}, Address: {student[3]}, Room Type: {student[4]}, Semester: {student[5]}, Course Type: {student[6]}, Branch: {student[7]}, Due Amount: {student[8]}, Deadline: {student[9]}")
    else:
        messagebox.showinfo("Not Found", "No students found.")

# Create a Tkinter window
root = Tk()
root.title("Hostel Management System")

# Book Room Section
book_room_frame = LabelFrame(root, text="Book a Room")
book_room_frame.grid(row=0, column=0, padx=10, pady=10)

Label(book_room_frame, text="Name:").grid(row=0, column=0)
Label(book_room_frame, text="Roll No:").grid(row=1, column=0)
Label(book_room_frame, text="Phone Number:").grid(row=2, column=0)
Label(book_room_frame, text="Address:").grid(row=3, column=0)
Label(book_room_frame, text="Room Type:").grid(row=4, column=0)
Label(book_room_frame, text="Semester:").grid(row=5, column=0)
Label(book_room_frame, text="Course Type:").grid(row=6, column=0)
Label(book_room_frame, text="Branch:").grid(row=7, column=0)

name_entry = Entry(book_room_frame)
roll_no_entry = Entry(book_room_frame)
phone_entry = Entry(book_room_frame)
address_entry = Entry(book_room_frame)
room_type_var = StringVar(book_room_frame)
room_type_var.set("3-sharing")
room_type_option = OptionMenu(book_room_frame, room_type_var, "3-sharing", "2-sharing")
semester_entry = Entry(book_room_frame)
course_entry = Entry(book_room_frame)
branch_entry = Entry(book_room_frame)

name_entry.grid(row=0, column=1)
roll_no_entry.grid(row=1, column=1)
phone_entry.grid(row=2, column=1)
address_entry.grid(row=3, column=1)
room_type_option.grid(row=4, column=1)
semester_entry.grid(row=5, column=1)
course_entry.grid(row=6, column=1)
branch_entry.grid(row=7, column=1)

book_button = Button(book_room_frame, text="Book", command=book_room)
book_button.grid(row=8, columnspan=2)

# Evacuate Section
evacuate_frame = LabelFrame(root, text="Evacuate from Hostel")
evacuate_frame.grid(row=0, column=1, padx=10, pady=10)

Label(evacuate_frame, text="Roll No:").grid(row=0, column=0)
evacuate_roll_no_entry = Entry(evacuate_frame)
evacuate_roll_no_entry.grid(row=0, column=1)

evacuate_button = Button(evacuate_frame, text="Evacuate", command=evacuate_from_hostel)
evacuate_button.grid(row=1, columnspan=2)

# Display Student Details Section
display_frame = LabelFrame(root, text="Display All Student Details")
display_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

display_button = Button(display_frame, text="Display", command=display_student_details)
display_button.pack()

# Main loop
root.mainloop()

# Close the connection
cursor.close()
conn.close()
