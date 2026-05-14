import tkinter as tk
from tkinter import ttk, messagebox
import random
import json

class RandomTaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator — Баданин Максим")
        self.history_file = "task_history.json"
        
        # Список доступных задач по категориям
        self.tasks_pool = {
            "Учёба": ["Прочитать статью", "Выучить 5 слов", "Посмотреть лекцию"],
            "Спорт": ["Сделать зарядку", "Пробежать 1 км", "Присесть 20 раз"],
            "Работа": ["Разобрать почту", "Написать отчет", "Запланировать звонок"]
        }
        
        self.history = self.load_history()

        # Интерфейс
        tk.Label(root, text="Выберите категорию:", font=('Arial', 10)).pack(pady=5)
        self.category_var = tk.StringVar(value="Учёба")
        self.category_cb = ttk.Combobox(root, textvariable=self.category_var, 
                                        values=list(self.tasks_pool.keys()), state="readonly")
        self.category_cb.pack(pady=5)

        tk.Button(root, text="Сгенерировать задачу", command=self.generate_task, 
                  bg="#4CAF50", fg="white", font=('Arial', 10, 'bold')).pack(pady=10)

        # Поле вывода текущей задачи
        self.result_label = tk.Label(root, text="Нажми кнопку, чтобы получить задачу", 
                                     font=('Arial', 11, 'italic'), fg="blue")
        self.result_label.pack(pady=10)

        # История
        tk.Label(root, text="История сгенерированных задач:").pack(pady=5)
        self.history_listbox = tk.Listbox(root, width=50, height=10)
        self.history_listbox.pack(padx=10, pady=5)

        # Фильтр истории
        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=5)
        tk.Label(filter_frame, text="Фильтр:").pack(side="left")
        self.filter_var = tk.StringVar(value="Все")
        self.filter_cb = ttk.Combobox(filter_frame, textvariable=self.filter_var, 
                                      values=["Все"] + list(self.tasks_pool.keys()), width=10)
        self.filter_cb.pack(side="left", padx=5)
        tk.Button(filter_frame, text="Применить", command=self.update_history_display).pack(side="left")

        self.update_history_display()

    def generate_task(self):
        cat = self.category_var.get()
        task = random.choice(self.tasks_pool[cat])
        self.result_label.config(text=f"Твоя задача: {task}", fg="black")
        
        # Добавляем в историю
        self.history.append({"task": task, "type": cat})
        self.save_history()
        self.update_history_display()

    def save_history(self):
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=4, ensure_ascii=False)

    def load_history(self):
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def update_history_display(self):
        self.history_listbox.delete(0, tk.END)
        f_type = self.filter_var.get()
        
        for item in reversed(self.history):
            if f_type == "Все" or item["type"] == f_type:
                self.history_listbox.insert(tk.END, f"[{item['type']}] {item['task']}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTaskGenerator(root)
    root.mainloop()
