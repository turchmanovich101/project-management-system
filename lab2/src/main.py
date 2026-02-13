# -*- coding: utf-8 -*-
"""
Головний файл для демонстрації роботи системи керування проектами (Lab1).
Цей файл показує приклади використання базових функцій CRUD.
"""

# Імпортуємо всі необхідні функції з нашого пакета project_manager
from project_manager import create_project, add_task, list_projects, list_tasks


def main():
    """
    Основна функція, яка демонструє роботу системи.
    Створює тестові проекти та задачі, потім виводить їх на екран.
    """
    print("=" * 60)
    print("СИСТЕМА КЕРУВАННЯ ПРОЕКТАМИ - Lab1")
    print("Базові CRUD операції")
    print("=" * 60)
    print()
    
    # Створюємо перший проект
    print("Створюємо проект 'Веб-розробка'...")
    project1_id = create_project(
        name="Веб-розробка",                    # Назва проекту
        description="Розробка нового веб-сайту", # Опис проекту
        status="active"                          # Статус проекту
    )
    print(f"✓ Проект створено з ID: {project1_id}")
    print()
    
    # Створюємо другий проект
    print("Створюємо проект 'Мобільний додаток'...")
    project2_id = create_project(
        name="Мобільний додаток",
        description="Розробка додатку для iOS та Android",
        status="active"
    )
    print(f"✓ Проект створено з ID: {project2_id}")
    print()
    
    # Додаємо задачі до першого проекту
    print(f"Додаємо задачі до проекту 'Веб-розробка' (ID: {project1_id})...")
    
    # Задача 1: Дизайн
    task1_id = add_task(
        project_id=project1_id,               # ID проекту
        title="Створити дизайн головної сторінки", # Назва задачі
        description="Розробити макет у Figma",     # Опис
        status="todo",                              # Статус: todo (не розпочато)
        priority="high"                             # Пріоритет: високий
    )
    print(f"  ✓ Задача додана з ID: {task1_id}")
    
    # Задача 2: Розробка
    task2_id = add_task(
        project_id=project1_id,
        title="Розробити backend API",
        description="Створити REST API для роботи з даними",
        status="todo",
        priority="high"
    )
    print(f"  ✓ Задача додана з ID: {task2_id}")
    
    # Задача 3: Тестування
    task3_id = add_task(
        project_id=project1_id,
        title="Написати тести",
        description="Unit та integration тести",
        status="todo",
        priority="medium"
    )
    print(f"  ✓ Задача додана з ID: {task3_id}")
    print()
    
    # Додаємо задачі до другого проекту
    print(f"Додаємо задачі до проекту 'Мобільний додаток' (ID: {project2_id})...")
    
    task4_id = add_task(
        project_id=project2_id,
        title="Налаштувати проект",
        description="Ініціалізувати React Native проект",
        status="todo",
        priority="high"
    )
    print(f"  ✓ Задача додана з ID: {task4_id}")
    print()
    
    # Виводимо список всіх проектів
    print("=" * 60)
    print("СПИСОК УСІХ ПРОЕКТІВ")
    print("=" * 60)
    
    # Отримуємо список проектів
    all_projects = list_projects()
    
    # Якщо проектів немає
    if not all_projects:
        print("Проектів поки немає")
    else:
        # Виводимо кожен проект
        for project in all_projects:
            print(f"\nПроект ID: {project['id']}")
            print(f"  Назва: {project['name']}")
            print(f"  Опис: {project['description']}")
            print(f"  Статус: {project['status']}")
    
    print()
    print("=" * 60)
    print("ЗАДАЧІ ПО ПРОЕКТАМ")
    print("=" * 60)
    
    # Виводимо задачі для кожного проекту
    for project in all_projects:
        print(f"\n📁 Проект: {project['name']} (ID: {project['id']})")
        print("-" * 60)
        
        # Отримуємо задачі конкретного проекту
        project_tasks = list_tasks(project_id=project['id'])
        
        # Якщо задач немає
        if not project_tasks:
            print("  Задач поки немає")
        else:
            # Виводимо кожну задачу
            for task in project_tasks:
                print(f"\n  ✓ Задача ID: {task['id']}")
                print(f"    Назва: {task['title']}")
                print(f"    Опис: {task['description']}")
                print(f"    Статус: {task['status']}")
                print(f"    Пріоритет: {task['priority']}")
    
    print()
    print("=" * 60)
    print("ВСІ ЗАДАЧІ (БЕЗ ФІЛЬТРУ)")
    print("=" * 60)
    
    # Отримуємо всі задачі без фільтрації
    all_tasks = list_tasks()
    print(f"\nЗагальна кількість задач: {len(all_tasks)}")
    
    for task in all_tasks:
        print(f"\n  Task #{task['id']}: {task['title']}")
        print(f"    Проект ID: {task['project_id']}")
        print(f"    Статус: {task['status']} | Пріоритет: {task['priority']}")
    
    print()
    print("=" * 60)
    print("ДЕМОНСТРАЦІЯ ЗАВЕРШЕНА")
    print("=" * 60)


# Точка входу в програму
# Цей блок виконується тільки якщо файл запускається напряму (не імпортується)
if __name__ == "__main__":
    main()  # Викликаємо головну функцію
