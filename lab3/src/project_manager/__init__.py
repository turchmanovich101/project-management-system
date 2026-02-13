# -*- coding: utf-8 -*-
"""
Пакет для керування проектами та задачами (Lab3).
Містить повні CRUD операції + File Storage (збереження у JSON).
"""

# Імпортуємо всі функції з модуля manager
from .manager import (
    # Create (створення)
    create_project,      # Функція створення проекту
    add_task,           # Функція додавання задачі до проекту
    
    # Read (читання)
    list_projects,      # Функція виведення списку проектів
    list_tasks,         # Функція виведення списку задач проекту
    
    # Update (оновлення)
    update_project,     # Функція оновлення даних проекту
    update_task,        # Функція оновлення даних задачі
    
    # Delete (видалення)
    delete_project,     # Функція видалення проекту та його задач
    delete_task         # Функція видалення задачі
)

# Імпортуємо функції для роботи з файлами
from .storage import (
    save_to_file,       # Збереження даних у JSON файл
    load_from_file      # Завантаження даних з JSON файлу
)

# Список публічних імен, які будуть доступні при імпорті пакета
__all__ = [
    'create_project',
    'add_task',
    'list_projects',
    'list_tasks',
    'update_project',
    'update_task',
    'delete_project',
    'delete_task',
    'save_to_file',
    'load_from_file'
]
