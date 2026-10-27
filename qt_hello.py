"""Средняя 10. Простейший GUI на PyQt5.

Окно с полем ввода имени, выпадающим списком времени суток и кнопкой:
по нажатию (или Enter) выводится приветствие.

>>> make_greeting("Маша", "Утро")
'Доброе утро, Маша!'
>>> make_greeting("  ", "Вечер")
'Добрый вечер, незнакомец!'
"""
import sys

from PyQt5.QtWidgets import (QApplication, QComboBox, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QWidget)

PARTS = {"Утро": "Доброе утро", "День": "Добрый день",
         "Вечер": "Добрый вечер", "Ночь": "Доброй ночи"}


def make_greeting(name, part):
    name = name.strip() or "незнакомец"
    return f"{PARTS[part]}, {name}!"


class HelloWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ЛР5 — Простейший GUI на PyQt5")
        self.resize(340, 180)
        self.name = QLineEdit()
        self.name.setPlaceholderText("Ваше имя")
        self.part = QComboBox()
        self.part.addItems(PARTS)
        self.button = QPushButton("Поздороваться")
        self.result = QLabel("Введите имя и нажмите кнопку")
        self.result.setStyleSheet("font-size: 15px; color: #1e5aa8;")

        layout = QVBoxLayout(self)
        for widget in (self.name, self.part, self.button, self.result):
            layout.addWidget(widget)

        self.button.clicked.connect(self.greet)
        self.name.returnPressed.connect(self.greet)

    def greet(self):
        self.result.setText(make_greeting(self.name.text(),
                                          self.part.currentText()))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HelloWindow()
    window.show()
    sys.exit(app.exec_())
