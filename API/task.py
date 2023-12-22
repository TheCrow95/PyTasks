import os
from pathlib import Path
import logging
import json

logging.basicConfig(level=logging.DEBUG)
TASKS_DIR = os.path.join(Path.home(), ".todo")
TASKS_FILEPATH = os.path.join(TASKS_DIR, "tasks.json")


def get_tasks():
    if os.path.exists(TASKS_FILEPATH):
        with open(TASKS_FILEPATH, "r") as f:
            return json.load(f)
    return {}


def add_task(name):
    tasks = get_tasks()
    if name in tasks.keys():
        logging.error("une tâche avec le même nom existe déjà")
        return False

    tasks[name] = False
    if not os.path.exists(TASKS_DIR):
        os.makedirs(TASKS_DIR)
    with open(TASKS_FILEPATH, "w") as f:
        json.dump(tasks, f, indent=4)
        logging.info("La tâche a été ajouté.")
    return True


if __name__ == '__main__':
    t = get_tasks()