"""Проверка всех заданий: запускает doctest-примеры из docstring модулей.

Окна при этом не открываются — проверяется логика, вынесенная в функции.
Запуск: python check.py
"""
import doctest

import listbox_pick
import progress
import qt_hello
import qt_table
import stopwatch

MODULES = [listbox_pick, progress, qt_hello, stopwatch, qt_table]

if __name__ == "__main__":
    failed = 0
    total = 0
    for module in MODULES:
        result = doctest.testmod(module)
        failed += result.failed
        total += result.attempted
        status = "OK" if result.failed == 0 else "ОШИБКИ"
        print(f"{module.__name__:<13} примеров: {result.attempted:>2}  "
              f"{status}")
    print(f"Всего примеров: {total}, провалено: {failed}")
