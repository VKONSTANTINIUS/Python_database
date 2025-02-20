import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


# Підключення до бази даних
conn = sqlite3.connect("school.db")
cursor = conn.cursor()

root = tk.Tk()
root.title("База даних школи")
root.geometry("800x600")

frame = tk.Frame(root)
frame.pack(pady=20)

columns_student = ("ID", "Повне ім’я", "Дата народження", "Клас", "Предмет", "Дата", "Оцінка")
tree_student = ttk.Treeview(frame, columns=columns_student, show="headings")

# Форма введення даних в таблицю Учні
def add_student_form():
    student_form = tk.Toplevel(root)
    student_form.title("Додати інформацію")
    student_form.geometry("300x300")

    tk.Label(student_form, text="Повне ім’я").pack()
    entry_name = tk.Entry(student_form)
    entry_name.pack()

    tk.Label(student_form, text="Дата народження").pack()
    entry_birth = tk.Entry(student_form)
    entry_birth.pack()

    tk.Label(student_form, text="Клас").pack()
    entry_class = tk.Entry(student_form)
    entry_class.pack()

    tk.Label(student_form, text="Предмет").pack()
    entry_subject = ttk.Combobox(student_form, values=["Математика","Співи","Українська мова","Читання"])
    entry_subject.pack()

    tk.Label(student_form, text="Дата").pack()
    entry_date = tk.Entry(student_form)
    entry_date.pack()

    tk.Label(student_form, text="Оцінка").pack()
    entry_grade = tk.Entry(student_form)
    entry_grade.pack()

    def add_student_button():
        add_student(entry_name, entry_birth, entry_class, entry_subject, entry_date, entry_grade, student_form)


    tk.Button(student_form, text="Додати", command=add_student_button).pack()

# Функція для додавання даних в таблицю Учні
def add_student(entry_name, entry_birth, entry_class, entry_subject, entry_date, entry_grade, student_form):
    try:
        full_name = entry_name.get()
        birth_date = entry_birth.get()
        class_name = entry_class.get()
        subject = entry_subject.get()
        date = entry_date.get()
        grade = int(entry_grade.get())

        if not (1 <= grade <= 12):
            raise ValueError("Оцінка має бути від 1 до 12")

        cursor.execute("INSERT INTO students (full_name, birth_date, class, subject, date, grade) VALUES (?, ?, ?, ?, ?, ?)",
                                            (full_name, birth_date, class_name, subject, date, grade))
        conn.commit()

        refresh_table()
                
    except:
        messagebox.showwarning("Попередження", "Перевірте правильність введення даних")

# Функція для видалення даних з таблиці Учні
def delete_student():
    try:
        selected_item = tree_student.selection()[0]
        student_id = tree_student.item(selected_item)['values'][0]

        cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
        conn.commit()

        refresh_table()
    except:
        messagebox.showwarning("Попередження", "Будь ласка, виберіть студента для видалення.")

# Функція для оновлення таблиці Учні - автоматчне оновлення таблиці після введення/видалення даних
def refresh_table():
    for item in tree_student.get_children():
        tree_student.delete(item)
    cursor.execute("SELECT * FROM students")
    for row in cursor.fetchall():
        tree_student.insert("", "end", values=row)

# вікно таблиці Вчителі
def teacher_table():
    
    def refresh_teacher_table():
        for item in tree_teachers.get_children():
            tree_teachers.delete(item)
        cursor.execute("SELECT * FROM teachers")
        for row in cursor.fetchall():
            tree_teachers.insert("", "end", values=row)

    def add_teacher(teacher_name):
        try:
            full_name = teacher_name.get()
            cursor.execute("INSERT INTO teachers (teacher_full_name) VALUES (?)", (full_name,))
            conn.commit()
            refresh_teacher_table()
            
        except:
            messagebox.showwarning("Попередження", "Перевірте правильність введення даних")  
              

    def add_teacher_button():
        add_teacher(teacher_name)

    def delete_teacher():
        try:
            selected_item = tree_teachers.selection()[0]
            teacher_id = tree_teachers.item(selected_item)['values'][0]

            cursor.execute("DELETE FROM teachers WHERE teacher_id=?", (teacher_id,))
            conn.commit()
            refresh_teacher_table()
            
        except:
            messagebox.showwarning("Попередження", "Будь ласка, виберіть вчителя для видалення.")   


    teacher_table = tk.Toplevel(root)
    teacher_table.title("Вчителі")
    teacher_table.geometry("500x500")
    columns_teacher = ("ID", "Повне ім’я")   
    tree_teachers = ttk.Treeview(teacher_table, columns=columns_teacher, show="headings")       
    
    for col in columns_teacher:
        tree_teachers.heading(col, text=col)
    cursor.execute("SELECT * FROM teachers")
    for row in cursor.fetchall():
        tree_teachers.insert("", "end", values=row)    
    tree_teachers.grid(row=0, column=0, columnspan=4)

    tk.Label(teacher_table, text="Повне ім’я").grid(row=1, column=0)
    teacher_name = tk.Entry(teacher_table)
    teacher_name.grid(row=1, column=1)
    tk.Button(teacher_table, text="Додати", command=add_teacher_button).grid(row=1, column=2)
    tk.Button(teacher_table, text="Видалити", command=delete_teacher).grid(row=1, column=3)    



def main():    

    # Створення таблиці "Учні"
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        birth_date TEXT NOT NULL,
        class TEXT NOT NULL,
        subject TEXT NOT NULL,
        date TEXT NOT NULL,
        grade INTEGER CHECK(grade BETWEEN 1 AND 12) NOT NULL
    )
    ''')
    
    # Створення таблиці "Вчителі"
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS teachers (
        teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_full_name TEXT NOT NULL        
    )
    ''')

    # Налаштування головного меню   

    menubar = tk.Menu(root)
    root.config(menu=menubar)

    students_menu = tk.Menu(menubar, tearoff=0)

    menubar.add_cascade(label="Учні", menu=students_menu)
    students_menu.add_command(label="Учні", command=refresh_table)
    students_menu.add_command(label="● Додати", command=add_student_form)
    students_menu.add_command(label="● Видалити ", command=delete_student)

    students_menu.add_separator()

    students_menu.add_command(label="Вийти", command=root.quit)

    teacher_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Вчителі", menu=teacher_menu) 
    teacher_menu.add_command(label="Показати дані", command=teacher_table)
        
    for col in columns_student:
        tree_student.heading(col, text=col)
    tree_student.pack()
    refresh_table()



main()

root.mainloop()

conn.close()  


