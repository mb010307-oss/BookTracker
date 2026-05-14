import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.expenses = self.load_data()

        # Поля ввода
        tk.Label(root, text="Сумма:").grid(row=0, column=0)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=0, column=1)

        tk.Label(root, text="Категория:").grid(row=1, column=0)
        self.category_cb = ttk.Combobox(root, values=["Еда", "Транспорт", "Развлечения", "Другое"])
        self.category_cb.grid(row=1, column=1)

        tk.Label(root, text="Дата (ГГГГ-ММ-ДД):").grid(row=2, column=0)
        self.date_entry = tk.Entry(root)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=2, column=1)

        tk.Button(root, text="Добавить расход", command=self.add_expense).grid(row=3, column=0, columnspan=2)

        # Таблица
        self.tree = ttk.Treeview(root, columns=("Сумма", "Категория", "Дата"), show='headings')
        self.tree.heading("Сумма", text="Сумма")
        self.tree.heading("Категория", text="Категория")
        self.tree.heading("Дата", text="Дата")
        self.tree.grid(row=4, column=0, columnspan=2)

        # Итоговая сумма
        self.total_label = tk.Label(root, text="Итого: 0", font=('Arial', 12, 'bold'))
        self.total_label.grid(row=5, column=0, columnspan=2)

        self.refresh_table()

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0: raise ValueError
            category = self.category_cb.get()
            date_str = self.date_entry.get()
            datetime.strptime(date_str, "%Y-%m-%d") # Валидация даты

            self.expenses.append({"amount": amount, "category": category, "date": date_str})
            self.save_data()
            self.refresh_table()
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную сумму и дату (ГГГГ-ММ-ДД)")

    def save_data(self):
        with open("expenses.json", "w", encoding="utf-8") as f:
            json.dump(self.expenses, f, indent=4)

    def load_data(self):
        try:
            with open("expenses.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        total = 0
        for exp in self.expenses:
            self.tree.insert("", "end", values=(exp["amount"], exp["category"], exp["date"]))
            total += exp["amount"]
        self.total_label.config(text=f"Итого: {total}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
