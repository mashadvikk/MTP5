"""Повышенная 9. Приложение PyQt с таблицей.

Список покупок: товар, цена и количество редактируются прямо в
таблице, столбец «Сумма» и итог пересчитываются автоматически.
Таблицу можно сохранить в CSV и загрузить обратно.

>>> row_sum("120,50", "2")
241.0
>>> row_sum("abc", "2") is None
True
>>> total([("Хлеб", "45", "2"), ("Сыр", "390", "1")])
480.0
"""
import csv
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QVBoxLayout, QWidget)

HEADERS = ["Товар", "Цена, руб.", "Кол-во", "Сумма, руб."]
ITEMS = [("Молоко", "89.90", "2"), ("Хлеб", "45", "1"),
         ("Яблоки, кг", "129.50", "1.5"), ("Сыр", "390", "1"),
         ("Чай", "215", "1")]


def to_number(text):
    try:
        return float(text.replace(",", ".").strip())
    except ValueError:
        return None


def row_sum(price, qty):
    """Сумма строки или None, если цена или количество не число."""
    p, q = to_number(price), to_number(qty)
    return round(p * q, 2) if p is not None and q is not None else None


def total(rows):
    sums = (row_sum(price, qty) for _, price, qty in rows)
    return round(sum(s for s in sums if s is not None), 2)


class ShoppingList(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ЛР5 — Список покупок (PyQt5)")
        self.resize(520, 330)
        self.table = QTableWidget(0, len(HEADERS))
        self.table.setHorizontalHeaderLabels(HEADERS)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnWidth(0, 170)
        self.total_label = QLabel()
        self.total_label.setStyleSheet("font-weight: bold;")

        buttons = QHBoxLayout()
        for text, slot in (("Добавить", self.add_empty),
                           ("Удалить", self.delete_row),
                           ("Сохранить CSV", self.save),
                           ("Открыть CSV", self.load)):
            button = QPushButton(text)
            button.clicked.connect(slot)
            buttons.addWidget(button)

        layout = QVBoxLayout(self)
        layout.addWidget(self.table)
        layout.addWidget(self.total_label)
        layout.addLayout(buttons)

        self.fill(ITEMS)
        self.table.itemChanged.connect(self.recalc)

    def fill(self, rows):
        self.table.blockSignals(True)
        self.table.setRowCount(0)
        for row in rows:
            self.append(row)
        self.table.blockSignals(False)
        self.recalc()

    def append(self, values):
        r = self.table.rowCount()
        self.table.insertRow(r)
        for c, value in enumerate(values):
            self.table.setItem(r, c, QTableWidgetItem(value))
        cell = QTableWidgetItem()
        cell.setFlags(cell.flags() & ~Qt.ItemIsEditable)
        cell.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.table.setItem(r, 3, cell)

    def rows(self):
        return [tuple(self.table.item(r, c).text()
                      if self.table.item(r, c) else "" for c in range(3))
                for r in range(self.table.rowCount())]

    def recalc(self, *_):
        self.table.blockSignals(True)
        for r, (_, price, qty) in enumerate(self.rows()):
            s = row_sum(price, qty)
            self.table.item(r, 3).setText(f"{s:.2f}" if s is not None
                                          else "ошибка")
        self.table.blockSignals(False)
        self.total_label.setText(f"Позиций: {self.table.rowCount()}, "
                                 f"итого: {total(self.rows()):.2f} руб.")

    def add_empty(self):
        self.table.blockSignals(True)
        self.append(("", "0", "1"))
        self.table.blockSignals(False)
        self.recalc()

    def delete_row(self):
        if self.table.currentRow() >= 0:
            self.table.removeRow(self.table.currentRow())
            self.recalc()

    def save(self):
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить", "покупки.csv",
                                              "CSV (*.csv)")
        if path:
            with open(path, "w", newline="", encoding="utf-8") as f:
                csv.writer(f, delimiter=";").writerows(self.rows())

    def load(self):
        path, _ = QFileDialog.getOpenFileName(self, "Открыть", "",
                                              "CSV (*.csv)")
        if path:
            with open(path, encoding="utf-8") as f:
                rows = csv.reader(f, delimiter=";")
                self.fill([tuple(row[:3]) for row in rows if len(row) >= 3])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShoppingList()
    window.show()
    sys.exit(app.exec_())
