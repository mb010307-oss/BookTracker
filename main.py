import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary — Дневник погоды")
        self.data_file = "weather_data.json"
        self.records = self.load_data()

        # Поля ввода
        tk.Label(root, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(root)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=0, column=1)

        tk.Label(root, text="Температура (°C):").grid(row=1, column=0)
        self.temp_entry = tk.Entry(root)
        self.temp_entry.grid(row=1, column=1)

        tk.Label(root, text="Описание (ясно, дождь...):").grid(row=2, column=0)
        self.desc_entry = tk.Entry(root)
        self.desc_entry.grid(row=2, column=1)

        tk.Label(root, text="Осадки:").grid(row=3, column=0)
        self.precip_var = tk.StringVar(value="Нет")
        self.precip_cb = ttk.Combobox(root, textvariable=self.precip_var, values=["Да", "Нет"], state="readonly")
        self.precip_cb.grid(row=3, column=1)

        tk.Button(root, text="Добавить запись", command=self.add_record, bg="lightblue").grid(row=4, column=0, columnspan=2, pady=10)

        # Фильтры
        filter_frame = tk.LabelFrame(root, text="Фильтрация")
        filter_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="we")
        
        tk.Label(filter_frame, text="Мин. темп:").pack(side="left")
        self.filter_temp = tk.Entry(filter_frame, width=5)
        self.filter_temp.pack(side="left", padx=5)
        
        tk.Button(filter_frame, text="Применить", command=self.refresh_table).pack(side="left", padx=5)
        tk.Button(filter_frame, text="Сброс", command=self.reset_filter).pack(side="left")

        # Таблица
        self.tree = ttk.Treeview(root, columns=("Дата", "Темп", "Описание", "Осадки"), show='headings')
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Темп", text="Темп. °C")
        self.tree.heading("Описание", text="Описание")
        self.tree.heading("Осадки", text="Осадки")
        self.tree.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.refresh_table()

    def add_record(self):
        try:
            date_str = self.date_entry.get()
            datetime.strptime(date_str, "%Y-%m-%d") # Валидация даты
            
            temp = float(self.temp_entry.get()) # Валидация числа
            desc = self.desc_entry.get().strip()
            
            if not desc:
                raise ValueError("Описание не может быть пустым")

            self.records.append({
                "date": date_str,
                "temp": temp,
                "desc": desc,
                "precip": self.precip_var.get()
            })
            self.save_data()
            self.refresh_table()
            self.temp_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            
        except ValueError as e:
            messagebox.showerror("Ошибка ввода", f"Проверьте данные: {e}\nФормат даты: ГГГГ-ММ-ДД")

    def save_data(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.records, f, indent=4, ensure_ascii=False)

    def load_data(self):
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def reset_filter(self):
        self.filter_temp.delete(0, tk.END)
        self.refresh_table()

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        min_temp_filter = self.filter_temp.get()
        
        for r in self.records:
            if min_temp_filter:
                try:
                    if r["temp"] < float(min_temp_filter):
                        continue
                except ValueError:
                    pass
            
            self.tree.insert("", "end", values=(r["date"], r["temp"], r["desc"], r["precip"]))

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()
