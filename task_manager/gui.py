import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from .task_manager import TaskManager
from .task import Task


class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Менеджер задач")
        self.root.geometry("1000x800")

        self.task_manager = TaskManager()

        self.create_widgets()
        self.update_task_list()

    def create_widgets(self):
        # Frame для списка задач
        self.task_list_frame = ttk.Frame(self.root)
        self.task_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Treeview для отображения задач
        self.task_tree = ttk.Treeview(self.task_list_frame, columns=("Title", "Description", "Due Date", "Priority", "Category", "Status"), show="headings")
        self.task_tree.heading("Title", text="Заголовок")
        self.task_tree.heading("Description", text="Описание")
        self.task_tree.heading("Due Date", text="Срок выполнения")
        self.task_tree.heading("Priority", text="Приоритет")
        self.task_tree.heading("Category", text="Категория")
        self.task_tree.heading("Status", text="Статус")
        self.task_tree.pack(fill=tk.BOTH, expand=True)

        # Frame для кнопок управления
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(fill=tk.X, padx=10, pady=10)

        # Кнопка добавления задачи
        self.add_button = ttk.Button(self.button_frame, text="Добавить задачу", command=self.open_add_task_dialog)
        self.add_button.pack(side=tk.LEFT, padx=5)

        # Кнопка редактирования задачи
        self.edit_button = ttk.Button(self.button_frame, text="Редактировать задачу", command=self.open_edit_task_dialog)
        self.edit_button.pack(side=tk.LEFT, padx=5)

        # Кнопка удаления задачи
        self.delete_button = ttk.Button(self.button_frame, text="Удалить задачу", command=self.delete_task)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        # Кнопка для отчета о выполненных задачах
        self.completed_report_button = ttk.Button(self.button_frame, text="Отчет по выполненным", command=self.show_completed_report)
        self.completed_report_button.pack(side=tk.LEFT, padx=5)

        # Кнопка для отчета о просроченных задачах
        self.overdue_report_button = ttk.Button(self.button_frame, text="Отчет по просроченным", command=self.show_overdue_report)
        self.overdue_report_button.pack(side=tk.LEFT, padx=5)

        # Кнопка для визуализации данных
        self.visualize_button = ttk.Button(self.button_frame, text="Визуализация", command=self.visualize_data)
        self.visualize_button.pack(side=tk.LEFT, padx=5)

    def open_edit_task_dialog(self):
        # Получение выбранной задачи
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите задачу для редактирования")
            return

        # Получение ID задачи
        self.selected_task_id = self.task_tree.index(selected_item[0])
        task = self.task_manager.get_task(self.selected_task_id)

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
        ttk.Button(self.edit_task_window, text="Сохранить", command=self.save_edited_task).grid(row=6, column=0, columnspan=2, pady=10)

    def save_edited_task(self):
        # Получение данных из полей ввода
        title = self.edit_title_entry.get()
        description = self.edit_description_entry.get()
        due_date = self.edit_due_date_entry.get_date()
        priority = self.edit_priority_entry.get()
        category = self.edit_category_entry.get()
        status = self.edit_status_entry.get()

        # Создание обновленной задачи
        updated_task = Task(title, description, due_date, priority, category, status)

        # Сохранение изменений
        self.task_manager.edit_task(self.selected_task_id, updated_task)

        # Обновление списка задач
        self.update_task_list()

        # Закрытие окна редактирования
        self.edit_task_window.destroy()

    def update_task_list(self):
        # Очистка текущего списка задач
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        # Загрузка задач из TaskManager
        tasks = self.task_manager.get_tasks()
        for task in tasks:
            self.task_tree.insert("", tk.END, values=(
                task.title,
                task.description,
                task.due_date.strftime("%Y-%m-%d %H:%M:%S"),
                task.priority,
                task.category,
                task.status
            ))

    def open_add_task_dialog(self):
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
        self.due_date_entry = DateEntry(self.add_task_window, date_pattern="yyyy-mm-dd")
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
        ttk.Button(self.add_task_window, text="Сохранить", command=self.save_task).grid(row=6, column=0, columnspan=2, pady=10)

    def save_task(self):
        # Получение данных из полей ввода
        title = self.title_entry.get()
        description = self.description_entry.get()
        due_date = self.due_date_entry.get_date()
        priority = self.priority_entry.get()
        category = self.category_entry.get()
        status = self.status_entry.get()

        # Создание новой задачи
        new_task = Task(title, description, due_date, priority, category, status)
        self.task_manager.add_task(new_task)

        # Обновление списка задач
        self.update_task_list()

        # Закрытие окна добавления задачи
        self.add_task_window.destroy()

    def delete_task(self):
        # Получение выбранной задачи
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите задачу для удаления")
            return

        # Удаление задачи
        task_id = self.task_tree.index(selected_item[0])
        self.task_manager.delete_task(task_id)

        # Обновление списка задач
        self.update_task_list()

    def show_completed_report(self):
        # Получение выполненных задач
        completed_tasks = [task for task in self.task_manager.get_tasks() if task.status == "Завершено"]

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
            report_text.insert(tk.END, "Нет выполненных задач.\n")

    def show_overdue_report(self):
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
            report_text.insert(tk.END, "Нет просроченных задач.\n")

    def visualize_data(self):
        # Окно для выбора критерия визуализации
        visualize_window = tk.Toplevel(self.root)
        visualize_window.title("Выбор критерия визуализации")

        # Выпадающий список для выбора критерия
        ttk.Label(visualize_window, text="Выберите критерий:").pack(padx=10, pady=5)
        criteria_var = tk.StringVar(value="Категория")  # По умолчанию выбрана категория
        criteria_combobox = ttk.Combobox(visualize_window, textvariable=criteria_var,
                                         values=["Категория", "Приоритет", "Статус"])
        criteria_combobox.pack(padx=10, pady=5)

        # Кнопка для построения графика
        ttk.Button(visualize_window, text="Построить график",
                   command=lambda: self._draw_graph(criteria_var.get())).pack(padx=10, pady=10)

    def _draw_graph(self, criteria):
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


def run_gui():
    root = tk.Tk()
    TaskManagerApp(root)
    root.mainloop()
