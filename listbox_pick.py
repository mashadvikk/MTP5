"""Средняя 4. Список (Listbox) и выбор элемента.

Список городов Тульской области: при выборе города справа выводятся
сведения о нём, поле поиска фильтрует список по мере ввода.

>>> filter_cities(CITIES, "ов")
['Ефремов', 'Кимовск', 'Новомосковск', 'Узловая']
>>> filter_cities(CITIES, "")[:2]
['Алексин', 'Богородицк']
>>> describe("Тула")
'Тула\\nНаселение: 465 тыс. чел.\\nОснован: 1146 г.'
"""
import tkinter as tk

CITIES = {
    "Алексин": (56, 1348),
    "Богородицк": (30, 1663),
    "Венёв": (14, 1371),
    "Ефремов": (35, 1637),
    "Кимовск": (25, 1952),
    "Новомосковск": (122, 1930),
    "Тула": (465, 1146),
    "Узловая": (51, 1874),
    "Щёкино": (55, 1870),
}


def filter_cities(cities, text):
    """Города, в названии которых есть text (без учёта регистра)."""
    text = text.strip().lower()
    return sorted(name for name in cities if text in name.lower())


def describe(name):
    population, year = CITIES[name]
    return f"{name}\nНаселение: {population} тыс. чел.\nОснован: {year} г."


class CityPicker(tk.Frame):
    def __init__(self, master):
        super().__init__(master, padx=12, pady=12)
        tk.Label(self, text="Поиск:").grid(row=0, column=0, sticky="w")
        self.query = tk.StringVar()
        self.query.trace_add("write", lambda *_: self.refresh())
        tk.Entry(self, textvariable=self.query, width=22).grid(
            row=0, column=1, sticky="we", pady=(0, 6))

        self.listbox = tk.Listbox(self, height=9, width=24,
                                  exportselection=False)
        self.listbox.grid(row=1, column=0, columnspan=2, sticky="ns")
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        self.info = tk.Label(self, text="Выберите город", width=24,
                             justify="left", anchor="nw",
                             font=("Segoe UI", 11), relief="groove",
                             padx=10, pady=10)
        self.info.grid(row=1, column=2, sticky="nsew", padx=(12, 0))
        self.refresh()

    def refresh(self):
        self.listbox.delete(0, "end")
        for name in filter_cities(CITIES, self.query.get()):
            self.listbox.insert("end", name)

    def on_select(self, _event=None):
        selection = self.listbox.curselection()
        if selection:
            self.info.config(text=describe(self.listbox.get(selection[0])))


if __name__ == "__main__":
    root = tk.Tk()
    root.title("ЛР5 — Список городов (Listbox)")
    CityPicker(root).pack()
    root.mainloop()
