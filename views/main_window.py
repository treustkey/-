# главное окно приложения
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
from tkcalendar import DateEntry


class MainWindow:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        # настройка окна
        self.root.title("Генератор Технических Заданий")
        self.root.geometry("900x700")

        # создание интерфейса
        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        # меню приложения
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Новый проект", command=self.new_project)
        file_menu.add_command(label="Сохранить", command=self.save_project)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)

        # меню "Экспорт"
        export_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Экспорт", menu=export_menu)
        export_menu.add_command(label="Экспорт в DOCX", command=self.export_docx)

    def create_widgets(self):
        # основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # заголовок
        title_label = ttk.Label(
            main_frame,
            text="Создание Технического Задания",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # РАЗДЕЛ 1: Основная информация
        section1_frame = ttk.LabelFrame(main_frame, text="1. Основная информация", padding="10")
        section1_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(section1_frame, text="Название проекта:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(section1_frame, width=60)
        self.name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(section1_frame, text="Тип документации:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.doc_type_var = tk.StringVar(value="ГОСТ 34.602-89")
        doc_type_combo = ttk.Combobox(
            section1_frame,
            textvariable=self.doc_type_var,
            values=["ГОСТ 34.602-89", "ГОСТ 19.201-78", "Свободная форма"],
            state="readonly",
            width=57
        )
        doc_type_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(section1_frame, text="Тип системы:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.system_type_entry = ttk.Entry(section1_frame, width=60)
        self.system_type_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(section1_frame, text="Срок выполнения:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.deadline_entry = DateEntry(
            section1_frame,
            width=57,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='dd.mm.yyyy'
        )
        self.deadline_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)

        # РАЗДЕЛ 2: Описание
        section2_frame = ttk.LabelFrame(main_frame, text="2. Описание проекта", padding="10")
        section2_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        self.description_text = scrolledtext.ScrolledText(
            section2_frame,
            width=80,
            height=6,
            wrap=tk.WORD
        )
        self.description_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # РАЗДЕЛ 3: Функциональные требования
        section3_frame = ttk.LabelFrame(main_frame, text="3. Функциональные требования", padding="10")
        section3_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        self.func_req_text = scrolledtext.ScrolledText(
            section3_frame,
            width=80,
            height=6,
            wrap=tk.WORD
        )
        self.func_req_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # кнопки действий
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        save_btn = ttk.Button(button_frame, text="Сохранить проект", command=self.save_project)
        save_btn.grid(row=0, column=0, padx=5)

        export_btn = ttk.Button(button_frame, text="Экспорт в DOCX", command=self.export_docx)
        export_btn.grid(row=0, column=1, padx=5)

        clear_btn = ttk.Button(button_frame, text="Очистить форму", command=self.clear_form)
        clear_btn.grid(row=0, column=2, padx=5)

        # настройка растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(3, weight=1)

    def new_project(self):
        self.clear_form()
        messagebox.showinfo("Новый проект", "Форма очищена. Заполните данные для нового проекта.")

    def save_project(self):
        name = self.name_entry.get().strip()

        if not name:
            messagebox.showerror("Ошибка", "Введите название проекта!")
            return

        doc_type = self.doc_type_var.get()
        system_type = self.system_type_entry.get().strip()
        deadline = self.deadline_entry.get_date()
        description = self.description_text.get("1.0", tk.END).strip()
        func_req = self.func_req_text.get("1.0", tk.END).strip()

        try:
            project_id = self.controller.save_project(
                name=name,
                documentation_type=doc_type,
                system_type=system_type,
                deadline=deadline,
                description=description,
                functional_requirements={'requirements': func_req}
            )
            messagebox.showinfo("Успех", f"Проект '{name}' сохранен (ID: {project_id})")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить проект: {str(e)}")

    def export_docx(self):
        name = self.name_entry.get().strip()

        if not name:
            messagebox.showerror("Ошибка", "Сначала заполните название проекта!")
            return

        try:
            output_path = self.controller.export_to_docx(
                name=name,
                documentation_type=self.doc_type_var.get(),
                system_type=self.system_type_entry.get().strip(),
                deadline=self.deadline_entry.get_date(),
                description=self.description_text.get("1.0", tk.END).strip(),
                functional_requirements=self.func_req_text.get("1.0", tk.END).strip()
            )
            messagebox.showinfo("Успех", f"Документ сохранен: {output_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать: {str(e)}")

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.system_type_entry.delete(0, tk.END)
        self.description_text.delete("1.0", tk.END)
        self.func_req_text.delete("1.0", tk.END)
        self.doc_type_var.set("ГОСТ 34.602-89")
        self.deadline_entry.set_date(datetime.now())
