# main.py

import threading
from task_manager.gui import run_gui
# from task_manager.background_tasks import start_background_scheduler

if __name__ == "__main__":
    # Запуск фоновой задачи в отдельном потоке
    # background_thread = threading.Thread(target=start_background_scheduler, daemon=True)
    # background_thread.start()

    # Запуск графического интерфейса
    run_gui()