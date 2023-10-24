import tkinter as tk
from tkinter import ttk
import sqlite3

# Подключение к базе данных и создание объекта курсора
conn = sqlite3.connect('employees.db')
cursor = conn.cursor()

# Создание таблицы 'employees', если она не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS employees 
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                number TEXT,
                email TEXT)''')

conn.commit()

# Функция для добавления сотрудника в базу данных
def add_employee():
    # Получение данных из полей ввода
    name = name_entry.get()
    number = number_entry.get()
    email = email_entry.get()

    # Проверка наличия данных в полях
    if name !="" and number!="" and email !="":
        # Формирование данных и SQL-запроса для добавления сотрудника
        data = (name, number, email)
        query = "INSERT INTO employees (name, number, email) VALUES (?, ?, ?)"
        cursor.execute(query, data)
        conn.commit()
        show_employees()  # Обновление отображения списка сотрудников
        clear_entries()  # Очистка полей ввода

# Функция для обновления данных сотрудника
def update_employee():
    # Получение данных из полей ввода
    id = id_entry.get()
    name = name_entry.get()
    number = number_entry.get()
    email = email_entry.get()

    # Проверка наличия данных в полях
    if id != "" and name != "" and number != "" and email != "":
        # Формирование данных и SQL-запроса для обновления сотрудника
        data = (name, number, email, id)
        query = "UPDATE employees SET name=?, number=?, email=? WHERE id=?"
        cursor.execute(query, data)
        conn.commit()
        show_employees()  # Обновление отображения списка сотрудников
        clear_entries()  # Очистка полей ввода

# Функция для удаления сотрудника
def delete_employee():
    # Получение данных из поля ввода
    id = id_entry.get() 

    # Проверка наличия данных в поле
    if id != "":
        # SQL-запрос для удаления сотрудника по ID
        query= "DELETE FROM employees WHERE id=?"
        cursor.execute(query, (id,))
        conn.commit()
        show_employees()  # Обновление отображения списка сотрудников
        clear_entries()  # Очистка полей ввода

# Функция для поиска сотрудника по имени
def search_employee():
    # Получение данных из поля ввода
    name = name_entry.get()

    # Проверка наличия данных в поле
    if name !="":
        # SQL-запрос для поиска сотрудника по имени
        query = "SELECT * FROM employees WHERE name=?"
        cursor.execute(query, (name,))
        result = cursor.fetchone()
        
        if result:
            # Вывод найденных данных в поля ввода
            id_entry.delete(0, tk.END)
            id_entry.insert(tk.END, result[0])
            number_entry.delete(0, tk.END)
            number_entry.insert(tk.END, result[2])
            email_entry.delete(0, tk.END)
            email_entry.insert(tk.END, result[3])
        else:
            clear_entries()  # Очистка полей ввода

# Функция для отображения списка сотрудников
def show_employees():
    # Очистка списка сотрудников перед обновлением
    for row in treeview.get_children():
        treeview.delete(row)

    # SQL-запрос для получения всех сотрудников
    query = "SELECT * FROM employees"
    cursor.execute(query)
    results = cursor.fetchall()

    # Добавление сотрудников в список
    for result in results:
        treeview.insert("", tk.END, values=result)

# Функция для очистки полей ввода
def clear_entries():
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    number_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

# Создание графического интерфейса
root = tk.Tk()
root.title("Employee Database")

# Создание меток и полей ввода для данных сотрудника
id_label = ttk.Label(root, text="ID:")
id_label.grid(row=0, column=0)
id_entry = ttk.Entry(root)
id_entry.grid(row=0, column=1)

name_label = ttk.Label(root, text="Имя:")
name_label.grid(row=1, column=0)
name_entry = ttk.Entry(root)
name_entry.grid(row=1, column=1)

number_label = ttk.Label(root, text="Номер:")
number_label.grid(row=2,column=0)
number_entry = ttk.Entry(root)
number_entry.grid(row=2, column=1)

email_label = ttk.Label(root, text="Электронная почта:")
email_label.grid(row=3, column=0)
email_entry = ttk.Entry(root)
email_entry.grid(row=3, column=1)

# Создание кнопок и привязка функций к ним
add_button = ttk.Button(root, text="Добавить", command=add_employee)
add_button.grid(row=4, column=0)

update_button = ttk.Button(root, text="Обновить", command=update_employee)
update_button.grid(row=4, column=1)

delete_button = ttk.Button(root, text="Удалить", command=delete_employee)
delete_button.grid(row=4, column=2)

search_button = ttk.Button(root, text="Поиск", command=search_employee)
search_button.grid(row=4, column=3)

# Создание таблицы для отображения списка сотрудников
treeview = ttk.Treeview(root, columns=("ID", "Имя", "Номер", "Электронная почта"), show="headings")
treeview.heading("ID", text="ID")
treeview.heading("Имя", text="Имя")
treeview.heading("Номер", text="Номер")
treeview.heading("Электронная почта", text="Электронная почта")
treeview.grid(row=5, columnspan=4)

show_employees()  # Отображение списка сотрудников

root.mainloop()

# Закрытие подключения к базе данных
conn.close()
