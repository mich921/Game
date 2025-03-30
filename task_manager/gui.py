"""Клиентская часть"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from .task import Task
from .storage import Storage
from .task_manager import TaskManager


class TaskManagerApp:
    def __init__(self, root: tk.Tk) -> None:
        """
        Инициализация главного окна приложения и основных переменных
        :param root: Корневое окно приложения
        :return: None
        """
        self.root = root
        self.root.title("Менеджер задач")
        self.root.geometry("1000x800")

        storage = Storage()
        self.task_manager = TaskManager(storage)
        self.original_tasks = []  # Исходный список задач
        self.sorted_tasks = []  # Отсортированный список задач
        self.sort_column = None  # Текущий столбец для сортировки
        self.sort_order = "default"  # Порядок сортировки: "asc", "desc", "default"

        self.create_widgets()
        self.update_task_list()

    def create_widgets(self) -> None:
        """
        Создание и размещение виджетов на главном окне
        :return: None
        """
        # Frame для кнопок управления (включая кнопку сброса сортировки)
        self.top_button_frame = ttk.Frame(self.root)
        self.top_button_frame.pack(fill=tk.X, padx=10, pady=5)

        # Кнопка сброса сортировки
        self.reset_sorting_button = ttk.Button(
            self.top_button_frame, text="Сбросить сортировку", command=self.reset_sorting
        )
        self.reset_sorting_button.pack(side=tk.LEFT, padx=5)

        # Frame для списка задач
        self.task_list_frame = ttk.Frame(self.root)
        self.task_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Treeview для отображения задач
        self.task_tree = ttk.Treeview(
            self.task_list_frame,
            columns=TaskManager.ALL_SORTS,
            show="headings"
        )
        self.task_tree.heading(
            TaskManager.SORT_TITLE, text="Заголовок", command=lambda: self.sort_tasks(TaskManager.SORT_TITLE)
        )
        self.task_tree.heading(
            TaskManager.SORT_DESCRIPTION, text="Описание", command=lambda: self.sort_tasks(TaskManager.SORT_DESCRIPTION)
        )
        self.task_tree.heading(
            TaskManager.SORT_DATE, text="Срок выполнения", command=lambda: self.sort_tasks(TaskManager.SORT_DATE)
        )
        self.task_tree.heading(
            TaskManager.SORT_PRIORITY, text="Приоритет", command=lambda: self.sort_tasks(TaskManager.SORT_PRIORITY)
        )
        self.task_tree.heading(
            TaskManager.SORT_CATEGORY, text="Категория", command=lambda: self.sort_tasks(TaskManager.SORT_CATEGORY)
        )
        self.task_tree.heading(
            TaskManager.SORT_STATUS, text="Статус", command=lambda: self.sort_tasks(TaskManager.SORT_STATUS)
        )
        self.task_tree.pack(fill=tk.BOTH, expand=True)

        # Frame для кнопок управления
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(fill=tk.X, padx=10, pady=10)

        # Кнопка добавления задачи
        self.add_button = ttk.Button(self.button_frame, text="Добавить задачу", command=self.open_add_task_dialog)
        self.add_button.pack(side=tk.LEFT, padx=5)

        # Кнопка редактирования задачи
        self.edit_button = ttk.Button(
            self.button_frame, text="Редактировать задачу", command=self.open_edit_task_dialog
        )
        self.edit_button.pack(side=tk.LEFT, padx=5)

        # Кнопка удаления задачи
        self.delete_button = ttk.Button(self.button_frame, text="Удалить задачу", command=self.delete_task)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        # Кнопка для отчета о выполненных задачах
        self.completed_report_button = ttk.Button(
            self.button_frame, text="Отчет по выполненным", command=self.show_completed_report
        )
        self.completed_report_button.pack(side=tk.LEFT, padx=5)

        # Кнопка для отчета о просроченных задачах
        self.overdue_report_button = ttk.Button(
            self.button_frame, text="Отчет по просроченным", command=self.show_overdue_report
        )
        self.overdue_report_button.pack(side=tk.LEFT, padx=5)

        # Кнопка для визуализации данных
        self.visualize_button = ttk.Button(self.button_frame, text="Визуализация", command=self.visualize_data)
        self.visualize_button.pack(side=tk.LEFT, padx=5)

        # Кнопка для импорта из JSON
        self.import_json_button = ttk.Button(
            self.button_frame, text="Импорт из JSON", command=self.import_from_json
        )
        self.import_json_button.pack(side=tk.LEFT, padx=5)

        # Кнопка для импорта из CSV
        self.import_csv_button = ttk.Button(
            self.button_frame, text="Импорт из CSV", command=self.import_from_csv
        )
        self.import_csv_button.pack(side=tk.LEFT, padx=5)

    def import_from_json(self) -> None:
        """
        Импорт задач из JSON-файла
        :return: None
        """
        file_path = filedialog.askopenfilename(
            title="Выберите JSON файл",
            filetypes=[("JSON files", "*.json")]
        )
        if file_path:
            try:
                self.task_manager.import_from_json(file_path)
                self.update_task_list()
                messagebox.showinfo("Успех", "Задачи успешно импортированы из JSON файла")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось импортировать задачи: {e}")

    def import_from_csv(self) -> None:
        """
        Импорт задач из CSV-файла
        :return: None
        """
        file_path = filedialog.askopenfilename(
            title="Выберите CSV файл",
            filetypes=[("CSV files", "*.csv")]
        )
        if file_path:
            try:
                self.task_manager.import_from_csv(file_path)
                self.update_task_list()
                messagebox.showinfo("Успех", "Задачи успешно импортированы из CSV файла")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось импортировать задачи: {e}")

    def reset_sorting(self) -> None:
        """
        Сброс сортировки и обновление списка задач
        :return: None
        """
        self.sort_column = None
        self.sort_order = "default"
        self.update_task_list()

    def sort_tasks(self, column: str) -> None:
        """
        Сортировка задач по выбранному столбцу
        :param column: Название столбца для сортировки
        :return: None
        """
        if self.sort_column == column:
            if self.sort_order == "asc":
                self.sort_order = "desc"
            elif self.sort_order == "desc":
                self.sort_order = "default"
            else:
                self.sort_order = "asc"
        else:
            self.sort_column = column
            self.sort_order = "asc"

        self.update_task_list()

    def open_edit_task_dialog(self) -> None:
        """
        Открытие окна для редактирования выбранной задачи
        :return: None
        """
        # Получение выбранной задачи
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите задачу для редактирования")
            return

        # Получение индекса задачи в отсортированном списке
        selected_index = self.task_tree.index(selected_item[0])
        task = self.sorted_tasks[selected_index]

        # Окно для редактирования задачи
        self.edit_task_window = tk.Toplevel(self.root)
        self.edit_task_window.title("Редактировать задачу")

        # Поля для ввода данных (предзаполненные)
        ttk.Label(self.edit_task_window, text="Заголовок:").grid(row=0, column=0, padx=5, pady=5)
        self.edit_title_entry = ttk.Entry(self.edit_task_window)
        self.edit_title_entry.insert(0, task.title)
        self.edit_title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.edit_task_window, text="Описание:").grid(row=1, column=0, padx=5, pady=5)
        self.edit_description_entry = ttk.Entry(self.edit_task_window)
        self.edit_description_entry.insert(0, task.description)
        self.edit_description_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.edit_task_window, text="Срок выполнения:").grid(row=2, column=0, padx=5, pady=5)
        self.edit_due_date_entry = DateEntry(self.edit_task_window, date_pattern="dd-mm-yyyy")
        self.edit_due_date_entry.set_date(task.due_date)
        self.edit_due_date_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.edit_task_window, text="Приоритет:").grid(row=3, column=0, padx=5, pady=5)
        self.edit_priority_entry = ttk.Combobox(self.edit_task_window, values=Task.ALL_PRIORITIES)
        self.edit_priority_entry.set(task.priority)
        self.edit_priority_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.edit_task_window, text="Категория:").grid(row=4, column=0, padx=5, pady=5)
        self.edit_category_entry = ttk.Combobox(self.edit_task_window, values=Task.ALL_CATEGORIES)
        self.edit_category_entry.set(task.category)
        self.edit_category_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self.edit_task_window, text="Статус:").grid(row=5, column=0, padx=5, pady=5)
        self.edit_status_entry = ttk.Combobox(self.edit_task_window, values=Task.ALL_STATUSES)
        self.edit_status_entry.set(task.status)
        self.edit_status_entry.grid(row=5, column=1, padx=5, pady=5)

        # Кнопка сохранения изменений
        ttk.Button(
            self.edit_task_window, text="Сохранить", command=lambda: self.save_edited_task(selected_index)
        ).grid(row=6, column=0, columnspan=2, pady=10)

    def save_edited_task(self, selected_index: int) -> None:
        """
        Сохранение изменений в задаче
        :param selected_index: Индекс задачи в отсортированном списке
        :return: None
        """
        try:
            updated_task = Task(
                title=self.edit_title_entry.get(),
                description=self.edit_description_entry.get(),
                due_date=self.edit_due_date_entry.get_date(),
                priority=self.edit_priority_entry.get(),
                category=self.edit_category_entry.get(),
                status=self.edit_status_entry.get()
            )
            original_index = self.original_tasks.index(self.sorted_tasks[selected_index])
            self.task_manager.edit_task(original_index, updated_task)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить задачу: {e}")

        self.update_task_list()
        self.edit_task_window.destroy()

    def update_task_list(self) -> None:
        """Обновление списка задач с учетом сортировки"""
        # Получаем исходный список задач
        self.original_tasks = self.task_manager.get_tasks()

        # Применяем сортировку (если нужно)
        if self.sort_column and self.sort_order != "default":
            reverse = (self.sort_order == "desc")
            self.sorted_tasks = self.task_manager.sort_tasks(self.original_tasks, self.sort_column, reverse)
        else:
            self.sorted_tasks = self.original_tasks.copy()

        # Очищаем Treeview
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        # Заполняем Treeview
        for task in self.sorted_tasks:
            self.task_tree.insert("", tk.END, values=(
                task.title,
                task.description,
                task.due_date.strftime("%d-%m-%Y"),
                task.priority,
                task.category,
                task.status
            ))

    def open_add_task_dialog(self) -> None:
        """
        Открытие окна для добавления новой задачи
        :return: None
        """
        # Окно для добавления новой задачи
        self.add_task_window = tk.Toplevel(self.root)
        self.add_task_window.title("Добавить задачу")

        # Поля для ввода данных
        ttk.Label(self.add_task_window, text="Заголовок:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = ttk.Entry(self.add_task_window)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.add_task_window, text="Описание:").grid(row=1, column=0, padx=5, pady=5)
        self.description_entry = ttk.Entry(self.add_task_window)
        self.description_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.add_task_window, text="Срок выполнения:").grid(row=2, column=0, padx=5, pady=5)
        self.due_date_entry = DateEntry(self.add_task_window, date_pattern="dd-mm-yyyy")
        self.due_date_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.add_task_window, text="Приоритет:").grid(row=3, column=0, padx=5, pady=5)
        self.priority_entry = ttk.Combobox(self.add_task_window, values=Task.ALL_PRIORITIES)
        self.priority_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.add_task_window, text="Категория:").grid(row=4, column=0, padx=5, pady=5)
        self.category_entry = ttk.Combobox(self.add_task_window, values=Task.ALL_CATEGORIES)
        self.category_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self.add_task_window, text="Статус:").grid(row=5, column=0, padx=5, pady=5)
        self.status_entry = ttk.Combobox(self.add_task_window, values=Task.ALL_STATUSES)
        self.status_entry.grid(row=5, column=1, padx=5, pady=5)

        # Кнопка сохранения задачи
        ttk.Button(
            self.add_task_window, text="Сохранить", command=self.save_task
        ).grid(row=6, column=0, columnspan=2, pady=10)

    def save_task(self) -> None:
        """
        Сохранение новой задачи
        :return: None
        """
        # Получение данных из полей ввода
        title = self.title_entry.get()
        description = self.description_entry.get()
        due_date = self.due_date_entry.get_date()
        priority = self.priority_entry.get()
        category = self.category_entry.get()
        status = self.status_entry.get()

        # Создание новой задачи
        try:
            new_task = Task(title, description, due_date, priority, category, status)
            self.task_manager.add_task(new_task)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить задачу: {e}")

        # Обновление списка задач
        self.update_task_list()

        # Закрытие окна добавления задачи
        self.add_task_window.destroy()

    def delete_task(self) -> None:
        """
        Удаление выбранной задачи
        :return: None
        """
        # Получение выбранной задачи
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите задачу для удаления")
            return

        # Получение индекса задачи в отсортированном списке
        selected_index = self.task_tree.index(selected_item[0])
        # Получение самой задачи из отсортированного списка
        task_to_delete = self.sorted_tasks[selected_index]
        # Находим индекс этой задачи в исходном списке
        original_index = self.original_tasks.index(task_to_delete)

        # Удаление задачи по оригинальному индексу
        self.task_manager.delete_task(original_index)

        # Обновление списка задач
        self.update_task_list()

    def show_completed_report(self) -> None:
        """
        Отображение отчета по выполненным задачам
        :return: None
        """
        # Получение выполненных задач
        completed_tasks = self.task_manager.get_tasks_by_status("Завершено")

        # Отображение отчета
        report_window = tk.Toplevel(self.root)
        report_window.title("Отчет по выполненным задачам")

        report_text = tk.Text(report_window, wrap=tk.WORD)
        report_text.pack(fill=tk.BOTH, expand=True)

        if completed_tasks:
            for task in completed_tasks:
                report_text.insert(tk.END, f"Заголовок: {task.title}\n")
                report_text.insert(tk.END, f"Описание: {task.description}\n")
                report_text.insert(tk.END, f"Срок выполнения: {task.due_date}\n")
                report_text.insert(tk.END, f"Категория: {task.category}\n")
                report_text.insert(tk.END, "-" * 40 + "\n")
        else:
            report_text.insert(tk.END, "Нет выполненных задач\n")

    def show_overdue_report(self) -> None:
        """
        Отображение отчета по просроченным задачам
        :return: None
        """
        # Получение просроченных задач
        overdue_tasks = self.task_manager.get_overdue_tasks()

        # Отображение отчета
        report_window = tk.Toplevel(self.root)
        report_window.title("Отчет по просроченным задачам")

        report_text = tk.Text(report_window, wrap=tk.WORD)
        report_text.pack(fill=tk.BOTH, expand=True)

        if overdue_tasks:
            for task in overdue_tasks:
                report_text.insert(tk.END, f"Заголовок: {task.title}\n")
                report_text.insert(tk.END, f"Описание: {task.description}\n")
                report_text.insert(tk.END, f"Срок выполнения: {task.due_date}\n")
                report_text.insert(tk.END, f"Категория: {task.category}\n")
                report_text.insert(tk.END, "-" * 40 + "\n")
        else:
            report_text.insert(tk.END, "Нет просроченных задач\n")

    def visualize_data(self) -> None:
        """
        Открытие окна для выбора критерия визуализации данных
        :return: None
        """
        # Окно для выбора критерия визуализации
        visualize_window = tk.Toplevel(self.root)
        visualize_window.title("Выбор критерия визуализации")

        # Выпадающий список для выбора критерия
        ttk.Label(visualize_window, text="Выберите критерий:").pack(padx=10, pady=5)
        criteria_var = tk.StringVar(value="Категория")  # По умолчанию выбрана категория
        criteria_combobox = ttk.Combobox(
            visualize_window, textvariable=criteria_var, values=["Категория", "Приоритет", "Статус"]
        )
        criteria_combobox.pack(padx=10, pady=5)

        # Кнопка для построения графика
        ttk.Button(
            visualize_window, text="Построить график", command=lambda: self._draw_graph(criteria_var.get())
        ).pack(padx=10, pady=10)

    def _draw_graph(self, criteria: str) -> None:
        """
        Построение графика по выбранному критерию
        :param criteria: Критерий для визуализации (Категория, Приоритет, Статус)
        :return: None
        """
        # Получение данных в зависимости от выбранного критерия
        tasks = self.task_manager.get_tasks()
        data = {}

        # Определяем все возможные значения для выбранного критерия
        if criteria == "Категория":
            all_values = Task.ALL_CATEGORIES
        elif criteria == "Приоритет":
            all_values = Task.ALL_PRIORITIES
        elif criteria == "Статус":
            all_values = Task.ALL_STATUSES
        else:
            raise Exception('Ошибка выбора отчета')

        # Инициализация данных нулевыми значениями
        for value in all_values:
            data[value] = 0

        # Подсчет задач для каждого значения
        for task in tasks:
            key = None
            if criteria == "Категория":
                key = task.category
            elif criteria == "Приоритет":
                key = task.priority
            elif criteria == "Статус":
                key = task.status

            if key in data:
                data[key] += 1

        # Создание графика
        fig, ax = plt.subplots()
        ax.bar(data.keys(), data.values())
        ax.set_xlabel(criteria)
        ax.set_ylabel("Количество задач")
        ax.set_title(f"Распределение задач по {criteria.lower()}")

        # Отображение графика в новом окне
        graph_window = tk.Toplevel(self.root)
        graph_window.title(f"График по {criteria.lower()}")

        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def run_gui() -> None:
    """
    Запуск графического интерфейса приложения
    :return: None
    """
    root = tk.Tk()
    TaskManagerApp(root)
    root.mainloop()
