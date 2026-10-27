"""Главное меню: запуск любого задания лабораторной №5 (вариант 4)."""
import subprocess
import sys

TASKS = {
    "1": ("Средняя 4. Список (Listbox) и выбор элемента", "listbox_pick.py"),
    "2": ("Средняя 6. Прогрессбар", "progress.py"),
    "3": ("Средняя 10. Простейший GUI на PyQt5", "qt_hello.py"),
    "4": ("Повышенная 5. Таймер и секундомер", "stopwatch.py"),
    "5": ("Повышенная 9. Приложение PyQt с таблицей", "qt_table.py"),
}


def main():
    while True:
        print("\nЛабораторная №5, вариант 4. Задания:")
        for key, (title, _) in TASKS.items():
            print(f"  {key}. {title}")
        print("  0. Выход")
        choice = input("Номер задания: ").strip()
        if choice == "0":
            print("Пока!")
            return
        task = TASKS.get(choice)
        if task is None:
            print("Нет такого пункта, попробуйте ещё раз.")
            continue
        title, script = task
        print(f"--- {title} (закройте окно, чтобы вернуться) ---")
        subprocess.run([sys.executable, script], check=False)


if __name__ == "__main__":
    main()
