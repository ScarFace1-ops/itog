import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os
from datetime import datetime

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("600x500")
        
        # История паролей
        self.history = []
        self.load_history()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Длина пароля
        ttk.Label(self.root, text="Длина пароля:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.length_var = tk.IntVar(value=12)
        self.length_scale = ttk.Scale(
            self.root, from_=4, to=50,
            variable=self.length_var, orient="horizontal"
        )
        self.length_scale.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.length_label = ttk.Label(self.root, text="12")
        self.length_label.grid(row=0, column=2, padx=10, pady=10)
        
        # Чекбоксы для символов
        self.digits_var = tk.BooleanVar(value=True)
        self.letters_var = tk.BooleanVar(value=True)
        self.special_var = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(self.root, text="Цифры (0-9)", variable=self.digits_var).grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        ttk.Checkbutton(self.root, text="Буквы (a-z, A-Z)", variable=self.letters_var).grid(
            row=2, column=0, padx=10, pady=5, sticky="w"
        )
        ttk.Checkbutton(self.root, text="Спецсимволы (!@#$%)", variable=self.special_var).grid(
            row=3, column=0, padx=10, pady=5, sticky="w"
        )
        
        # Кнопка генерации
        self.generate_btn = ttk.Button(self.root, text="Сгенерировать пароль", command=self.generate_password)
        self.generate_btn.grid(row=4, column=0, columnspan=3, pady=20)
        
        # Поле вывода пароля
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(
            self.root, textvariable=self.password_var, state="readonly", width=40
        )
        self.password_entry.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        
        # Таблица истории
        columns = ("ID", "Пароль", "Длина", "Дата создания")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=8)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        
        # Прокрутка для таблицы
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=6, column=3, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Обновление отображения длины
        self.length_scale.bind("<Motion>", self.update_length_label)
        # Настройка весов строк и столбцов
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(6, weight=1)
    
    def update_length_label(self, event=None):
        length = int(self.length_scale.get())
        self.length_label.config(text=str(length))
    def generate_password(self):
        # Проверка выбора хотя бы одного типа символов
        if not (self.digits_var.get() or self.letters_var.get() or self.special_var.get()):
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов!")
            return
        # Получение длины пароля
        length = self.length_var.get()
        if length < 4:
            messagebox.showerror("Ошибка", "Минимальная длина пароля — 4 символа!")
            return
        if length > 50:
            messagebox.showerror("Ошибка", "Максимальная длина пароля — 50 символов!")
            return
        # Формирование набора символов
        chars = ""
        if self.digits_var.get():
            chars += string.digits
        if self.letters_var.get():
            chars += string.ascii_letters
        if self.special_var.get():
            chars += "!@#$%^&*"
        # Генерация пароля
        password = ''.join(random.choice(chars) for _ in range(length))
        # Отображение пароля
        self.password_var.set(password)
        # Добавление в историю
        self.add_to_history(password, length)
    def add_to_history(self, password, length):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "id": len(self.history) + 1,
            "password": password,
            "length": length,
            "timestamp": timestamp
        }
        self.history.append(entry)
        self.update_history_table()
        self.save_history()
    
    def update_history_table(self):
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Заполнение таблицы
        for entry in self.history:
            self.tree.insert("", "end", values=(
                entry["id"], entry["password"], entry["length"], entry["timestamp"]
            ))
    
    def save_history(self):
        try:
            with open("password_history.json", "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=4, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {e}")
    
    def load_history(self):
        if os.path.exists("password_history.json"):
            try:
                with open("password_history.json", "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить историю: {e}")
                self.history = []
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
