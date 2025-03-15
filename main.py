# main.py

from task_manager.task_manager import TaskManager
from task_manager.analytics import Analytics
from task_manager.notification import Notification


def main():
    task_manager = TaskManager()
    analytics = Analytics(task_manager)
    notification = Notification()

    # Пример использования
    task_manager.add_task(Task("Задача 1", "Описание задачи 1", datetime.now(), "Высокий", "Работа"))
    report = analytics.generate_report(datetime(2023, 1, 1), datetime(2023, 12, 31))
    print(report)
    analytics.plot_tasks_by_category()


if __name__ == "__main__":
    main()