# -*- coding: utf-8 -*-
"""
Модуль тестів для перевірки функціональності системи керування проектами (Lab1).
Використовує pytest для автоматичного тестування.
"""

import pytest  # Імпортуємо бібліотеку pytest для тестування
import sys     # Імпортуємо sys для роботи з шляхами
import os      # Імпортуємо os для роботи з файловою системою

# Додаємо шлях до src директорії, щоб можна було імпортувати наш пакет
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Імпортуємо наш менеджер проектів
from project_manager import manager


@pytest.fixture(autouse=True)
def reset_data():
    """
    Фікстура pytest, яка автоматично виконується перед кожним тестом.
    Очищає всі дані (проекти і задачі) і скидає лічильники ID.
    
    autouse=True означає, що ця фікстура застосовується до всіх тестів автоматично.
    """
    # Очищаємо словники з даними
    manager.projects.clear()    # Видаляємо всі проекти
    manager.tasks.clear()       # Видаляємо всі задачі
    
    # Скидаємо лічильники ID до початкових значень
    manager.project_id_counter = 1  # Перший проект матиме ID = 1
    manager.task_id_counter = 1     # Перша задача матиме ID = 1


def test_create_project():
    """
    Тест функції create_project().
    Перевіряє:
    1. Чи створюється проект
    2. Чи повертається правильний ID
    3. Чи зберігаються правильні дані проекту
    """
    # Створюємо тестовий проект
    project_id = manager.create_project(
        name="Тестовий проект",
        description="Це тестовий опис",
        status="active"
    )
    
    # Перевіряємо, що повернено ID = 1 (перший проект)
    assert project_id == 1, "ID першого проекту повинен бути 1"
    
    # Перевіряємо, що проект збережено в словнику projects
    assert project_id in manager.projects, "Проект має бути в словнику projects"
    
    # Отримуємо дані проекту зі словника
    project = manager.projects[project_id]
    
    # Перевіряємо що всі поля збережені правильно
    assert project["name"] == "Тестовий проект", "Назва проекту має співпадати"
    assert project["description"] == "Це тестовий опис", "Опис проекту має співпадати"
    assert project["status"] == "active", "Статус проекту має співпадати"


def test_add_task():
    """
    Тест функції add_task().
    Перевіряє:
    1. Чи додається задача до існуючого проекту
    2. Чи повертається правильний ID задачі
    3. Чи зберігаються правильні дані задачі
    4. Чи повертається None при додаванні до неіснуючого проекту
    """
    # Спочатку створюємо проект
    project_id = manager.create_project("Проект для задач")
    
    # Додаємо задачу до проекту
    task_id = manager.add_task(
        project_id=project_id,
        title="Тестова задача",
        description="Опис задачі",
        status="todo",
        priority="high"
    )
    
    # Перевіряємо, що повернено ID = 1 (перша задача)
    assert task_id == 1, "ID першої задачі повинен бути 1"
    
    # Перевіряємо, що задача збережена в словнику tasks
    assert task_id in manager.tasks, "Задача має бути в словнику tasks"
    
    # Отримуємо дані задачі зі словника
    task = manager.tasks[task_id]
    
    # Перевіряємо що всі поля збережені правильно
    assert task["project_id"] == project_id, "ID проекту має співпадати"
    assert task["title"] == "Тестова задача", "Назва задачі має співпадати"
    assert task["description"] == "Опис задачі", "Опис задачі має співпадати"
    assert task["status"] == "todo", "Статус задачі має співпадати"
    assert task["priority"] == "high", "Пріоритет задачі має співпадати"
    
    # Перевіряємо що add_task повертає None для неіснуючого проекту
    invalid_task_id = manager.add_task(
        project_id=9999,  # Неіснуючий ID проекту
        title="Неможлива задача"
    )
    assert invalid_task_id is None, "add_task має повернути None для неіснуючого проекту"


def test_list_projects():
    """
    Тест функції list_projects().
    Перевіряє:
    1. Чи повертається порожній список коли проектів немає
    2. Чи повертаються всі створені проекти
    3. Чи містять проекти правильні дані включно з ID
    """
    # Спочатку перевіряємо порожній список
    projects = manager.list_projects()
    assert projects == [], "Список проектів має бути порожнім на початку"
    
    # Створюємо два проекти
    id1 = manager.create_project("Проект 1", "Опис 1", "active")
    id2 = manager.create_project("Проект 2", "Опис 2", "completed")
    
    # Отримуємо список проектів
    projects = manager.list_projects()
    
    # Перевіряємо кількість проектів
    assert len(projects) == 2, "Має бути 2 проекти"
    
    # Перевіряємо перший проект
    project1 = next(p for p in projects if p["id"] == id1)  # Знаходимо проект з id1
    assert project1["name"] == "Проект 1", "Назва першого проекту має співпадати"
    assert project1["description"] == "Опис 1", "Опис першого проекту має співпадати"
    assert project1["status"] == "active", "Статус першого проекту має співпадати"
    
    # Перевіряємо другий проект
    project2 = next(p for p in projects if p["id"] == id2)  # Знаходимо проект з id2
    assert project2["name"] == "Проект 2", "Назва другого проекту має співпадати"
    assert project2["description"] == "Опис 2", "Опис другого проекту має співпадати"
    assert project2["status"] == "completed", "Статус другого проекту має співпадати"


def test_list_tasks():
    """
    Тест функції list_tasks().
    Перевіряє:
    1. Чи повертається порожній список коли задач немає
    2. Чи повертаються всі задачі при виклику без параметрів
    3. Чи фільтруються задачі за project_id
    4. Чи містять задачі правильні дані включно з ID
    """
    # Створюємо два проекти
    project1_id = manager.create_project("Проект 1")
    project2_id = manager.create_project("Проект 2")
    
    # Спочатку перевіряємо порожній список
    tasks = manager.list_tasks()
    assert tasks == [], "Список задач має бути порожнім на початку"
    
    # Додаємо задачі до першого проекту
    task1_id = manager.add_task(project1_id, "Задача 1-1", status="todo")
    task2_id = manager.add_task(project1_id, "Задача 1-2", status="in_progress")
    
    # Додаємо задачу до другого проекту
    task3_id = manager.add_task(project2_id, "Задача 2-1", status="done")
    
    # Перевіряємо загальну кількість задач (без фільтру)
    all_tasks = manager.list_tasks()
    assert len(all_tasks) == 3, "Загалом має бути 3 задачі"
    
    # Перевіряємо фільтрацію задач за project_id для першого проекту
    project1_tasks = manager.list_tasks(project_id=project1_id)
    assert len(project1_tasks) == 2, "У першого проекту має бути 2 задачі"
    
    # Перевіряємо що всі задачі належать першому проекту
    for task in project1_tasks:
        assert task["project_id"] == project1_id, "Задача має належати першому проекту"
    
    # Перевіряємо фільтрацію для другого проекту
    project2_tasks = manager.list_tasks(project_id=project2_id)
    assert len(project2_tasks) == 1, "У другого проекту має бути 1 задача"
    assert project2_tasks[0]["project_id"] == project2_id, "Задача має належати другому проекту"
    assert project2_tasks[0]["title"] == "Задача 2-1", "Назва задачі має співпадати"
    assert project2_tasks[0]["status"] == "done", "Статус задачі має співпадати"
