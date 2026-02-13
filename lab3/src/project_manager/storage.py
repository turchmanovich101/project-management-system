# -*- coding: utf-8 -*-
"""
Модуль storage.py - збереження та завантаження даних у JSON файлах (Lab3).
Забезпечує персистентність даних між запусками програми.
"""

import json
import os


def save_to_file(projects, tasks, filename="data.json"):
    """
    Зберігає проекти та задачі у JSON файл.
    
    Параметри:
        projects (dict): Словник проектів {id: {name, description, status}}
        tasks (dict): Словник задач {id: {project_id, title, description, status, priority}}
        filename (str): Ім'я файлу для збереження (за замовчуванням "data.json")
    
    Приклад використання:
        save_to_file(projects, tasks, "my_data.json")
    """
    # Створюємо словник з усіма даними для збереження
    data = {
        "projects": projects,  # Зберігаємо всі проекти
        "tasks": tasks         # Зберігаємо всі задачі
    }
    
    # Відкриваємо файл для запису
    # mode='w' - режим запису (перезаписує файл якщо існує)
    # encoding='utf-8' - кодування UTF-8 для підтримки українських символів
    with open(filename, 'w', encoding='utf-8') as f:
        # json.dump() - записує Python об'єкт у JSON файл
        # indent=2 - форматування з відступами для читабельності
        # ensure_ascii=False - дозволяє зберігати не-ASCII символи (українські букви)
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_from_file(filename="data.json"):
    """
    Завантажує проекти та задачі з JSON файлу.
    
    Параметри:
        filename (str): Ім'я файлу для завантаження (за замовчуванням "data.json")
    
    Повертає:
        tuple: (projects, tasks, project_id_counter, task_id_counter)
               Якщо файл не існує, повертає порожні словники та лічильники = 1
    
    Приклад використання:
        projects, tasks, proj_counter, task_counter = load_from_file("my_data.json")
    """
    # Перевіряємо чи існує файл
    if not os.path.exists(filename):
        # Якщо файлу немає, повертаємо порожні дані
        # Порожні словники для проектів та задач
        # Лічильники починаються з 1
        return {}, {}, 1, 1
    
    # Відкриваємо файл для читання
    # mode='r' - режим читання
    # encoding='utf-8' - кодування UTF-8
    with open(filename, 'r', encoding='utf-8') as f:
        # json.load() - читає JSON з файлу та конвертує в Python об'єкт
        data = json.load(f)
    
    # Отримуємо проекти та задачі з завантажених даних
    projects = data.get("projects", {})  # get() повертає {} якщо ключа немає
    tasks = data.get("tasks", {})
    
    # Конвертуємо ключі зі строк в числа
    # JSON зберігає ключі словників як рядки, треба конвертувати назад в int
    projects = {int(k): v for k, v in projects.items()}
    tasks = {int(k): v for k, v in tasks.items()}
    
    # Обчислюємо наступні ID для лічильників
    # Беремо максимальний існуючий ID + 1, або 1 якщо немає проектів/задач
    project_id_counter = max(projects.keys()) + 1 if projects else 1
    task_id_counter = max(tasks.keys()) + 1 if tasks else 1
    
    # Повертаємо завантажені дані та лічильники
    return projects, tasks, project_id_counter, task_id_counter
