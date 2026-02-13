# -*- coding: utf-8 -*-
"""
Модуль manager.py - основний модуль для керування проектами та задачами (Lab2).
Реалізує повні CRUD операції (Create, Read, Update, Delete) для проектів і задач.
"""

# Глобальні словники для зберігання даних у пам'яті
# projects: зберігає проекти у форматі {id: {"name": "...", "description": "...", "status": "..."}}
projects = {}

# tasks: зберігає задачі у форматі {id: {"project_id": ..., "title": "...", "description": "...", "status": "...", "priority": "..."}}
tasks = {}

# Лічильники для генерації унікальних ID
project_id_counter = 1  # Поточний ID для нового проекту
task_id_counter = 1     # Поточний ID для нової задачі


def create_project(name, description="", status="active"):
    """
    Створює новий проект та додає його до словника projects.
    
    Параметри:
        name (str): Назва проекту (обов'язковий параметр)
        description (str): Опис проекту (необов'язковий, за замовчуванням порожній)
        status (str): Статус проекту (необов'язковий, за замовчуванням "active")
    
    Повертає:
        int: ID створеного проекту
    
    Приклад використання:
        project_id = create_project("Мій проект", "Опис проекту", "active")
    """
    global project_id_counter  # Використовуємо глобальний лічильник ID
    
    # Створюємо словник з даними проекту
    project = {
        "name": name,              # Назва проекту
        "description": description, # Опис проекту
        "status": status           # Статус проекту (active, completed, archived)
    }
    
    # Додаємо проект до словника projects з поточним ID
    projects[project_id_counter] = project
    
    # Зберігаємо поточний ID для повернення
    current_id = project_id_counter
    
    # Збільшуємо лічильник для наступного проекту
    project_id_counter += 1
    
    # Повертаємо ID створеного проекту
    return current_id


def add_task(project_id, title, description="", status="todo", priority="medium"):
    """
    Додає нову задачу до вказаного проекту.
    
    Параметри:
        project_id (int): ID проекту, до якого додається задача
        title (str): Назва задачі (обов'язковий параметр)
        description (str): Опис задачі (необов'язковий)
        status (str): Статус задачі (необов'язковий, за замовчуванням "todo")
        priority (str): Пріоритет задачі (необов'язковий, за замовчуванням "medium")
    
    Повертає:
        int або None: ID створеної задачі, або None якщо проект не існує
    
    Приклад використання:
        task_id = add_task(1, "Назва задачі", "Опис", "todo", "high")
    """
    global task_id_counter  # Використовуємо глобальний лічильник ID задач
    
    # Перевіряємо чи існує проект з вказаним ID
    if project_id not in projects:
        # Якщо проект не знайдено, повертаємо None
        return None
    
    # Створюємо словник з даними задачі
    task = {
        "project_id": project_id,    # ID проекту, до якого належить задача
        "title": title,               # Назва задачі
        "description": description,   # Опис задачі
        "status": status,             # Статус: todo, in_progress, done
        "priority": priority          # Пріоритет: low, medium, high
    }
    
    # Додаємо задачу до словника tasks з поточним ID
    tasks[task_id_counter] = task
    
    # Зберігаємо поточний ID для повернення
    current_id = task_id_counter
    
    # Збільшуємо лічильник для наступної задачі
    task_id_counter += 1
    
    # Повертаємо ID створеної задачі
    return current_id


def list_projects():
    """
    Повертає список усіх проектів.
    
    Повертає:
        list: Список словників, де кожен словник містить дані проекту з його ID
              Формат: [{"id": 1, "name": "...", "description": "...", "status": "..."}, ...]
    
    Приклад використання:
        all_projects = list_projects()
        for project in all_projects:
            print(f"ID: {project['id']}, Назва: {project['name']}")
    """
    result = []  # Створюємо порожній список для результату
    
    # Проходимося по всіх проектах у словнику
    for project_id, project_data in projects.items():
        # Створюємо новий словник, який містить ID та всі дані проекту
        project_with_id = {"id": project_id}  # Додаємо ID
        project_with_id.update(project_data)   # Додаємо всі дані проекту (name, description, status)
        
        # Додаємо проект до результату
        result.append(project_with_id)
    
    # Повертаємо список всіх проектів
    return result


def list_tasks(project_id=None):
    """
    Повертає список задач. Якщо вказано project_id, повертає тільки задачі цього проекту.
    
    Параметри:
        project_id (int або None): ID проекту для фільтрації (необов'язковий)
                                   Якщо None - повертаються всі задачі
    
    Повертає:
        list: Список словників, де кожен словник містить дані задачі з її ID
              Формат: [{"id": 1, "project_id": 1, "title": "...", ...}, ...]
    
    Приклад використання:
        # Отримати всі задачі
        all_tasks = list_tasks()
        
        # Отримати задачі конкретного проекту
        project_tasks = list_tasks(project_id=1)
    """
    result = []  # Створюємо порожній список для результату
    
    # Проходимося по всіх задачах у словнику
    for task_id, task_data in tasks.items():
        # Якщо project_id вказано, перевіряємо чи належить задача до цього проекту
        if project_id is not None and task_data["project_id"] != project_id:
            continue  # Якщо задача належить до іншого проекту, пропускаємо її
        
        # Створюємо новий словник, який містить ID та всі дані задачі
        task_with_id = {"id": task_id}     # Додаємо ID задачі
        task_with_id.update(task_data)      # Додаємо всі дані задачі
        
        # Додаємо задачу до результату
        result.append(task_with_id)
    
    # Повертаємо список задач
    return result


def update_project(project_id, name=None, description=None, status=None):
    """
    Оновлює дані існуючого проекту.
    Оновлюються тільки ті поля, які передані (не None).
    
    Параметри:
        project_id (int): ID проекту для оновлення (обов'язковий)
        name (str або None): Нова назва проекту (якщо None - не змінюється)
        description (str або None): Новий опис проекту (якщо None - не змінюється)
        status (str або None): Новий статус проекту (якщо None - не змінюється)
    
    Повертає:
        bool: True якщо проект оновлено успішно, False якщо проект не знайдено
    
    Приклад використання:
        # Оновити тільки назву
        update_project(1, name="Нова назва")
        
        # Оновити кілька полів
        update_project(1, name="Нова назва", status="completed")
    """
    # Перевіряємо чи існує проект з вказаним ID
    if project_id not in projects:
        # Якщо проект не знайдено, повертаємо False
        return False
    
    # Отримуємо посилання на проект зі словника
    project = projects[project_id]
    
    # Оновлюємо тільки ті поля, які передані (не None)
    if name is not None:
        project["name"] = name  # Оновлюємо назву
    
    if description is not None:
        project["description"] = description  # Оновлюємо опис
    
    if status is not None:
        project["status"] = status  # Оновлюємо статус
    
    # Повертаємо True - проект успішно оновлено
    return True


def update_task(task_id, title=None, description=None, status=None, priority=None):
    """
    Оновлює дані існуючої задачі.
    Оновлюються тільки ті поля, які передані (не None).
    
    Параметри:
        task_id (int): ID задачі для оновлення (обов'язковий)
        title (str або None): Нова назва задачі (якщо None - не змінюється)
        description (str або None): Новий опис задачі (якщо None - не змінюється)
        status (str або None): Новий статус задачі (якщо None - не змінюється)
        priority (str або None): Новий пріоритет задачі (якщо None - не змінюється)
    
    Повертає:
        bool: True якщо задачу оновлено успішно, False якщо задача не знайдена
    
    Приклад використання:
        # Оновити статус задачі
        update_task(1, status="in_progress")
        
        # Оновити кілька полів
        update_task(1, title="Оновлена назва", priority="high")
    """
    # Перевіряємо чи існує задача з вказаним ID
    if task_id not in tasks:
        # Якщо задачу не знайдено, повертаємо False
        return False
    
    # Отримуємо посилання на задачу зі словника
    task = tasks[task_id]
    
    # Оновлюємо тільки ті поля, які передані (не None)
    if title is not None:
        task["title"] = title  # Оновлюємо назву
    
    if description is not None:
        task["description"] = description  # Оновлюємо опис
    
    if status is not None:
        task["status"] = status  # Оновлюємо статус
    
    if priority is not None:
        task["priority"] = priority  # Оновлюємо пріоритет
    
    # Повертаємо True - задачу успішно оновлено
    return True


def delete_project(project_id):
    """
    Видаляє проект та всі його задачі з системи.
    
    Параметри:
        project_id (int): ID проекту для видалення
    
    Повертає:
        bool: True якщо проект видалено успішно, False якщо проект не знайдено
    
    Приклад використання:
        success = delete_project(1)
        if success:
            print("Проект видалено")
        else:
            print("Проект не знайдено")
    """
    # Перевіряємо чи існує проект з вказаним ID
    if project_id not in projects:
        # Якщо проект не знайдено, повертаємо False
        return False
    
    # Видаляємо проект зі словника
    del projects[project_id]
    
    # Видаляємо всі задачі, які належали цьому проекту
    # Створюємо список ID задач для видалення (не можемо змінювати словник під час ітерації)
    tasks_to_delete = []
    
    # Знаходимо всі задачі проекту
    for task_id, task_data in tasks.items():
        if task_data["project_id"] == project_id:
            tasks_to_delete.append(task_id)  # Додаємо ID задачі до списку для видалення
    
    # Видаляємо знайдені задачі
    for task_id in tasks_to_delete:
        del tasks[task_id]
    
    # Повертаємо True - проект та його задачі успішно видалено
    return True


def delete_task(task_id):
    """
    Видаляє задачу з системи.
    
    Параметри:
        task_id (int): ID задачі для видалення
    
    Повертає:
        bool: True якщо задачу видалено успішно, False якщо задача не знайдена
    
    Приклад використання:
        success = delete_task(1)
        if success:
            print("Задачу видалено")
        else:
            print("Задачу не знайдено")
    """
    # Перевіряємо чи існує задача з вказаним ID
    if task_id not in tasks:
        # Якщо задачу не знайдено, повертаємо False
        return False
    
    # Видаляємо задачу зі словника
    del tasks[task_id]
    
    # Повертаємо True - задачу успішно видалено
    return True
