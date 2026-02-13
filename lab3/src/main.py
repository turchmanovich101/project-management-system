# -*- coding: utf-8 -*-
"""
Головний файл для демонстрації Lab3 - File Storage.
Показує як зберігати та завантажувати дані з JSON файлів.
"""

# Імпортуємо всі необхідні функції
from project_manager import (
    create_project, add_task, list_projects, list_tasks,
    update_project, delete_task,
    save_to_file, load_from_file
)
import project_manager.manager as manager


def main():
    """
    Основна функція для демонстрації File Storage.
    """
    print("=" * 60)
    print("СИСТЕМА КЕРУВАННЯ ПРОЕКТАМИ - Lab3")
    print("File Storage (Збереження даних у JSON)")
    print("=" * 60)
    print()
    
    # Крок 1: Завантажуємо існуючі дані (якщо є)
    print("📂 Завантаження даних з файлу...")
    projects, tasks, proj_counter, task_counter = load_from_file("data.json")
    
    # Оновлюємо глобальні змінні менеджера
    manager.projects = projects
    manager.tasks = tasks
    manager.project_id_counter = proj_counter
    manager.task_id_counter = task_counter
    
    print(f"✓ Завантажено {len(projects)} проектів та {len(tasks)} задач")
    print()
    
    # Крок 2: Створюємо нові дані (якщо БД порожня)
    if not projects:
        print("Створюємо початкові дані...")
        
        # Створюємо проекти
        project1_id = create_project("Веб-додаток", "Розробка сайту", "active")
        project2_id = create_project("Мобільний додаток", "iOS та Android", "active")
        
        # Додаємо задачі
        add_task(project1_id, "Дизайн головної сторінки", "Figma макет", "todo", "high")
        add_task(project1_id, "Backend API", "REST endpoints", "in_progress", "high")
        add_task(project2_id, "Налаштування проекту", "React Native", "todo", "medium")
        
        print("✓ Створено 2 проекти та 3 задачі")
        print()
    
    # Крок 3: Виводимо поточний стан
    print("=" * 60)
    print("ПОТОЧНІ ПРОЕКТИ")
    print("=" * 60)
    
    all_projects = list_projects()
    for project in all_projects:
        print(f"\n📁 {project['name']} (ID: {project['id']})")
        print(f"   Опис: {project['description']}")
        print(f"   Статус: {project['status']}")
        
        # Виводимо задачі проекту
        project_tasks = list_tasks(project_id=project['id'])
        if project_tasks:
            print(f"   Задачі ({len(project_tasks)}):")
            for task in project_tasks:
                print(f"     • {task['title']} [{task['status']}] (пріоритет: {task['priority']})")
        else:
            print("   Задач немає")
    
    print()
    print("=" * 60)
    print("ДЕМОНСТРАЦІЯ ОПЕРАЦІЙ")
    print("=" * 60)
    print()
    
    # Крок 4: Виконуємо операції
    if all_projects:
        first_project = all_projects[0]
        
        # Оновлюємо проект
        print(f"📝 Оновлюємо проект '{first_project['name']}'...")
        update_project(first_project['id'], description="Оновлений опис проекту")
        print("✓ Проект оновлено")
        print()
        
        # Додаємо нову задачу
        print(f"➕ Додаємо нову задачу до проекту '{first_project['name']}'...")
        new_task_id = add_task(
            first_project['id'],
            "Тестування системи",
            "Unit та integration тести",
            "todo",
            "medium"
        )
        print(f"✓ Задачу додано з ID: {new_task_id}")
        print()
    
    # Крок 5: Зберігаємо всі зміни
    print("💾 Зберігаємо дані у файл...")
    save_to_file(manager.projects, manager.tasks, "data.json")
    print("✓ Дані збережено в data.json")
    print()
    
    # Крок 6: Показуємо фінальну статистику
    print("=" * 60)
    print("ФІНАЛЬНА СТАТИСТИКА")
    print("=" * 60)
    print(f"Проектів: {len(manager.projects)}")
    print(f"Задач: {len(manager.tasks)}")
    print(f"Файл: data.json")
    print()
    
    print("💡 Перезапустіть програму - дані завантажаться з файлу!")
    print("=" * 60)


# Точка входу
if __name__ == "__main__":
    main()
