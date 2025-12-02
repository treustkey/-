# главный файл приложения
import tkinter as tk
from tkinter import ttk
import sys
import os

# добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controllers.project_controller import ProjectController
from views.main_window import MainWindow


def main():
    # создание главного окна
    root = tk.Tk()

    # настройка стиля
    style = ttk.Style()
    style.theme_use('clam')

    # инициализация контроллера
    controller = ProjectController()

    # создание главного окна приложения
    app = MainWindow(root, controller)

    # запуск главного цикла
    root.mainloop()


if __name__ == "__main__":
    main()
