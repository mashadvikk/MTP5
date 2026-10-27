"""Средняя 6. Прогрессбар.

«Скачивание» файла заданного размера: скорость выбирается ползунком,
полоса ttk.Progressbar обновляется таймером after(), рядом выводится
оставшееся время. Вторая полоса в неопределённом режиме показывает
«поиск обновлений», когда длительность заранее неизвестна.

>>> seconds_left(50, 200, 25)
6
>>> seconds_left(200, 200, 25)
0
>>> fmt_size(1536)
'1.5 МБ'
"""
import math
import tkinter as tk
from tkinter import ttk

FILE_SIZE = 2048  # КБ
TICK_MS = 100


def seconds_left(done, total, speed):
    """Сколько секунд осталось при скорости speed КБ/с (вверх)."""
    return math.ceil((total - done) / speed) if done < total else 0


def fmt_size(kb):
    return f"{kb / 1024:.1f} МБ" if kb >= 1024 else f"{kb} КБ"


class Downloader(tk.Frame):
    def __init__(self, master):
        super().__init__(master, padx=16, pady=12)
        self.done = 0
        self.job = None

        tk.Label(self, text=f"Файл lab5.zip, {fmt_size(FILE_SIZE)}",
                 font=("Segoe UI", 11, "bold")).pack(anchor="w")
        self.bar = ttk.Progressbar(self, length=340, maximum=FILE_SIZE)
        self.bar.pack(pady=6)
        self.status = tk.Label(self, text="Ожидание", anchor="w")
        self.status.pack(fill="x")

        self.speed = tk.IntVar(value=150)
        tk.Scale(self, from_=50, to=500, resolution=50, orient="horizontal",
                 label="Скорость, КБ/с", variable=self.speed,
                 length=340).pack(pady=4)

        buttons = tk.Frame(self)
        buttons.pack()
        tk.Button(buttons, text="Скачать", width=10,
                  command=self.start).pack(side="left", padx=3)
        tk.Button(buttons, text="Пауза", width=10,
                  command=self.pause).pack(side="left", padx=3)
        tk.Button(buttons, text="Заново", width=10,
                  command=self.restart).pack(side="left", padx=3)

        ttk.Separator(self).pack(fill="x", pady=10)
        self.search = ttk.Progressbar(self, length=340, mode="indeterminate")
        self.search.pack()
        self.search_btn = tk.Button(self, text="Искать обновления",
                                    command=self.toggle_search)
        self.search_btn.pack(pady=4)

    def start(self):
        if self.job is None and self.done < FILE_SIZE:
            self.tick()

    def pause(self):
        if self.job is not None:
            self.after_cancel(self.job)
            self.job = None
            self.status.config(text="Пауза")

    def restart(self):
        self.pause()
        self.done = 0
        self.bar["value"] = 0
        self.status.config(text="Ожидание")

    def tick(self):
        step = self.speed.get() * TICK_MS // 1000
        self.done = min(FILE_SIZE, self.done + step)
        self.bar["value"] = self.done
        left = seconds_left(self.done, FILE_SIZE, self.speed.get())
        self.status.config(text=f"{fmt_size(self.done)} из "
                                f"{fmt_size(FILE_SIZE)}, осталось {left} с")
        if self.done < FILE_SIZE:
            self.job = self.after(TICK_MS, self.tick)
        else:
            self.job = None
            self.status.config(text="Загрузка завершена")

    def toggle_search(self):
        if self.search_btn.cget("text") == "Искать обновления":
            self.search.start(15)
            self.search_btn.config(text="Остановить поиск")
        else:
            self.search.stop()
            self.search_btn.config(text="Искать обновления")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("ЛР5 — Прогрессбар")
    Downloader(root).pack()
    root.mainloop()
