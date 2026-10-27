"""Повышенная 5. Программа таймер/секундомер.

Две вкладки ttk.Notebook: секундомер с кругами и таймер обратного
отсчёта. Время считается по time.perf_counter(), а не по числу
срабатываний after(), поэтому секундомер не «отстаёт».

>>> format_time(0)
'00:00.0'
>>> format_time(75.38)
'01:15.3'
>>> format_time(3725)
'1:02:05.0'
>>> parse_minutes("2:30")
150
>>> parse_minutes("45")
2700
"""
import time
import tkinter as tk
from tkinter import messagebox, ttk


def format_time(seconds):
    """Секунды → строка ММ:СС.д (с часами, если их больше нуля)."""
    tenths = int(seconds * 10)
    h, rest = divmod(tenths, 36000)
    m, rest = divmod(rest, 600)
    s, d = divmod(rest, 10)
    return f"{h}:{m:02d}:{s:02d}.{d}" if h else f"{m:02d}:{s:02d}.{d}"


def parse_minutes(text):
    """«ММ:СС» или «М» (целые минуты) → секунды."""
    if ":" in text:
        m, s = text.split(":")
        return int(m) * 60 + int(s)
    return int(text) * 60


class Stopwatch(tk.Frame):
    def __init__(self, master):
        super().__init__(master, padx=10, pady=10)
        self.started = None
        self.elapsed = 0.0
        self.display = tk.Label(self, text=format_time(0),
                                font=("Consolas", 32))
        self.display.pack()
        buttons = tk.Frame(self)
        buttons.pack(pady=6)
        self.start_btn = tk.Button(buttons, text="Старт", width=8,
                                   command=self.toggle)
        self.start_btn.pack(side="left", padx=2)
        tk.Button(buttons, text="Круг", width=8,
                  command=self.lap).pack(side="left", padx=2)
        tk.Button(buttons, text="Сброс", width=8,
                  command=self.reset).pack(side="left", padx=2)
        self.laps = tk.Listbox(self, height=5, width=30)
        self.laps.pack()

    def current(self):
        if self.started is None:
            return self.elapsed
        return self.elapsed + time.perf_counter() - self.started

    def toggle(self):
        if self.started is None:
            self.started = time.perf_counter()
            self.start_btn.config(text="Стоп")
            self.update_display()
        else:
            self.elapsed = self.current()
            self.started = None
            self.start_btn.config(text="Старт")

    def lap(self):
        n = self.laps.size() + 1
        self.laps.insert("end", f"Круг {n}: {format_time(self.current())}")

    def reset(self):
        self.started = None
        self.elapsed = 0.0
        self.start_btn.config(text="Старт")
        self.display.config(text=format_time(0))
        self.laps.delete(0, "end")

    def update_display(self):
        self.display.config(text=format_time(self.current()))
        if self.started is not None:
            self.after(50, self.update_display)


class Timer(tk.Frame):
    def __init__(self, master):
        super().__init__(master, padx=10, pady=10)
        self.deadline = None
        tk.Label(self, text="Время (ММ:СС или минуты):").pack()
        self.entry = tk.Entry(self, justify="center", width=10,
                              font=("Consolas", 14))
        self.entry.insert(0, "0:10")
        self.entry.pack(pady=4)
        self.display = tk.Label(self, text=format_time(10),
                                font=("Consolas", 32))
        self.display.pack()
        tk.Button(self, text="Запустить", width=12,
                  command=self.start).pack(pady=6)

    def start(self):
        try:
            seconds = parse_minutes(self.entry.get())
        except ValueError:
            messagebox.showerror("Таймер", "Неверный формат времени")
            return
        self.deadline = time.perf_counter() + seconds
        self.update_display()

    def update_display(self):
        left = max(0.0, self.deadline - time.perf_counter())
        self.display.config(text=format_time(left))
        if left > 0:
            self.after(50, self.update_display)
        else:
            self.bell()
            self.display.config(text="Время вышло!")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("ЛР5 — Секундомер и таймер")
    tabs = ttk.Notebook(root)
    tabs.add(Stopwatch(tabs), text="Секундомер")
    tabs.add(Timer(tabs), text="Таймер")
    tabs.pack(padx=8, pady=8)
    root.mainloop()
