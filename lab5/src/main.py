# -*- coding: utf-8 -*-
"""
Головний файл для Lab5 - Repository Pattern.
Демонструє використання шару абстракції для роботи з БД.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project_manager import Base, ProjectRepository, TaskRepository


def main():
    """
    Основна функція для демонстрації Repository Pattern.
    """
    print("=" * 60)
    print("СИСТЕМА КЕРУВАННЯ ПРОЕКТАМИ - Lab5")
    print("Repository Pattern (Шар абстракції для БД)")
    print("=" * 60)
    print()
    
    # Створюємо engine та сесію
    engine = create_engine('sqlite:///database.db', echo=False)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Створюємо repositories
    project_repo = ProjectRepository(session)
    task_repo = TaskRepository(session)
    
    print("✓ Підключено до БД через Repository Pattern")
    print()
    
    # Перевіряємо чи є дані
    if project_repo.count() == 0:
        print("Створюємо початкові дані через repositories...")
        print()
        
        # Створюємо проекти через repository
        project1 = project_repo.create(
            name="Веб-платформа",
            description="E-commerce сайт",
            status="active"
        )
        print(f"✓ Створено проект: {project1.name} (ID: {project1.id})")
        
        project2 = project_repo.create(
            name="Мобільний додаток",
            description="Кросплатформний додаток",
            status="active"
        )
        print(f"✓ Створено проект: {project2.name} (ID: {project2.id})")
        print()
        
        # Створюємо задачі через repository
        task1 = task_repo.create(
            project_id=project1.id,
            title="Дизайн системи",
            description="UX/UI дизайн",
            status="in_progress",
            priority="high"
        )
        print(f"✓ Створено задачу: {task1.title}")
        
        task2 = task_repo.create(
            project_id=project1.id,
            title="Backend розробка",
            description="API endpoints",
            status="todo",
            priority="high"
        )
        print(f"✓ Створено задачу: {task2.title}")
        
        task3 = task_repo.create(
            project_id=project2.id,
            title="Налаштування середовища",
            description="React Native setup",
            status="done",
            priority="medium"
        )
        print(f"✓ Створено задачу: {task3.title}")
        print()
    
    # Демонстрація методів Repository
    print("=" * 60)
    print("ДЕМОНСТРАЦІЯ REPOSITORY PATTERN")
    print("=" * 60)
    print()
    
    # 1. Читання всіх проектів
    print("📂 Всі проекти (через ProjectRepository.get_all()):")
    all_projects = project_repo.get_all()
    for project in all_projects:
        print(f"   • {project.name} [{project.status}]")
    print()
    
    # 2. Фільтрація за статусом
    print("🔍 Активні проекти (через ProjectRepository.get_by_status()):")
    active_projects = project_repo.get_by_status("active")
    for project in active_projects:
        print(f"   • {project.name}")
    print()
    
    # 3. Читання задач проекту
    if all_projects:
        first_project = all_projects[0]
        print(f"📝 Задачі проекту '{first_project.name}' (через TaskRepository.get_by_project()):")
        project_tasks = task_repo.get_by_project(first_project.id)
        for task in project_tasks:
            print(f"   • {task.title} [{task.status}] (пріоритет: {task.priority})")
        print()
    
    # 4. Фільтрація задач за пріоритетом
    print("⚡ Високопріоритетні задачі (через TaskRepository.get_by_priority()):")
    high_priority_tasks = task_repo.get_by_priority("high")
    for task in high_priority_tasks:
        print(f"   • {task.title} (проект ID: {task.project_id})")
    print()
    
    # 5. Оновлення через repository
    if all_projects:
        print(f"📝 Оновлюємо проект через ProjectRepository.update()...")
        updated_project = project_repo.update(
            all_projects[0].id,
            description="Оновлений опис через Repository Pattern"
        )
        if updated_project:
            print(f"✓ Проект '{updated_project.name}' оновлено")
        print()
    
    # 6. Створення нової задачі
    if all_projects:
        print("➕ Додаємо задачу через TaskRepository.create()...")
        new_task = task_repo.create(
            project_id=all_projects[0].id,
            title="Code review",
            description="Перевірка якості коду",
            status="todo",
            priority="medium"
        )
        if new_task:
            print(f"✓ Задачу '{new_task.title}' створено з ID: {new_task.id}")
        print()
    
    # 7. Статистика через repositories
    print("=" * 60)
    print("СТАТИСТИКА (через Repository методи)")
    print("=" * 60)
    
    total_projects = project_repo.count()
    total_tasks = task_repo.count()
    todo_tasks = len(task_repo.get_by_status("todo"))
    in_progress_tasks = len(task_repo.get_by_status("in_progress"))
    done_tasks = len(task_repo.get_by_status("done"))
    
    print(f"Всього проектів: {total_projects}")
    print(f"Всього задач: {total_tasks}")
    print(f"  • TO DO: {todo_tasks}")
    print(f"  • IN PROGRESS: {in_progress_tasks}")
    print(f"  • DONE: {done_tasks}")
    print()
    
    # Закриваємо сесію
    session.close()
    
    print("=" * 60)
    print("ПЕРЕВАГИ REPOSITORY PATTERN")
    print("=" * 60)
    print("✓ Чистий код - бізнес-логіка відділена від SQL")
    print("✓ Тестування - легко створити mock repositories")
    print("✓ Читабельність - зрозумілі методи замість SQL запитів")
    print("✓ Зміна БД - легко замінити SQLite на PostgreSQL")
    print("✓ Повторне використання - один раз написано, багато разів використано")
    print("=" * 60)


if __name__ == "__main__":
    main()
