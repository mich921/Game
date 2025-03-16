import matplotlib.pyplot as plt

class Analytics:
    def __init__(self, task_manager):
        self.task_manager = task_manager

    def generate_report(self, start_date, end_date):
        tasks = self.task_manager.get_tasks()
        completed_tasks = [task for task in tasks if task.status == "Завершено" and start_date <= task.due_date <= end_date]
        overdue_tasks = self.task_manager.get_overdue_tasks()

        report = {
            "total_tasks": len(tasks),
            "completed_tasks": len(completed_tasks),
            "overdue_tasks": len(overdue_tasks),
            "completion_rate": len(completed_tasks) / len(tasks) if len(tasks) > 0 else 0
        }
        return report

    def plot_tasks_by_category(self):
        tasks = self.task_manager.get_tasks()
        categories = {}
        for task in tasks:
            if task.category in categories:
                categories[task.category] += 1
            else:
                categories[task.category] = 1

        plt.bar(categories.keys(), categories.values())
        plt.xlabel("Категории")
        plt.ylabel("Количество задач")
        plt.title("Распределение задач по категориям")
        plt.show()