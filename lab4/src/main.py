# -*- coding: utf-8 -*-
"""
Головний файл для Lab4 - SQLite Database з SQLAlchemy ORM.
Демонструє роботу з реляційною базою даних.
"""

# Імпортуємо необхідні модулі
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project_manager.models import Base, Project, Task


def main():
    """
    Основна функція для демонстрації роботи з SQLite.
    """
    print("=" * 60)
    print("СИСТЕМА КЕРУВАННЯ ПРОЕКТАМИ - Lab4")
    print("SQLite Database з SQLAlchemy ORM")
    print("=" * 60)
    print()
    
    # Крок 1: Створюємо engine - з'єднання з БД
    print("📂 Підключення до бази даних...")
    # sqlite:///database.db - створює файл database.db
    # echo=False - не виводити SQL запити (для чистого виводу)
    engine = create_engine('sqlite:///database.db', echo=False)
    
    # Створюємо всі таблиці згідно з моделями
    Base.metadata.create_all(engine)
    print("✓ База даних database.db готова")
    print()
    
    # Крок 2: Створюємо фабрику сесій
    # Session - клас для створення нових сесій роботи з БД
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Крок 3: Перевіряємо чи є дані в БД
    existing_projects = session.query(Project).count()
    
    if existing_projects == 0:
        print("Створюємо початкові дані...")
        
        # Створюємо проекти
        project1 = Project(
            name="Веб-додаток",
            description="Розробка сайту для компанії",
            status="active"
        )
        
        project2 = Project(
            name="Мобільний додаток",
            description="iOS та Android додаток",
            status="active"
        )
        
        # Додаємо проекти до сесії
        session.add(project1)
        session.add(project2)
        
        # Зберігаємо зміни (commit)
        # SQLAlchemy автоматично присвоїть ID проектам
        session.commit()
        
        print(f"✓ Створено проект '{project1.name}' з ID: {project1.id}")
        print(f"✓ Створено проект '{project2.name}' з ID: {project2.id}")
        print()
        
        # Створюємо задачі для першого проекту
        task1 = Task(
            project_id=project1.id,
            title="Дизайн головної сторінки",
            description="Створити макет у Figma",
            status="todo",
            priority="high"
        )
        
        task2 = Task(
            project_id=project1.id,
            title="Розробити Backend API",
            description="REST endpoints для роботи з даними",
            status="in_progress",
            priority="high"
        )
        
        task3 = Task(
            project_id=project2.id,
            title="Налаштувати проект",
            description="Ініціалізувати React Native",
            status="todo",
            priority="medium"
        )
        
        # Додаємо задачі
        session.add_all([task1, task2, task3])
        session.commit()
        
        print(f"✓ Створено 3 задачі")
        print()
    else:
        print(f"✓ Знайдено {existing_projects} проектів у базі даних")
        print()
    
    # Крок 4: Читаємо всі проекти з БД
    print("=" * 60)
    print("ПРОЕКТИ З БАЗИ ДАНИХ")
    print("=" * 60)
    
    # query(Project).all() - вибирає всі проекти
    projects = session.query(Project).all()
    
    for project in projects:
        print(f"\n📁 {project.name} (ID: {project.id})")
        print(f"   Опис: {project.description}")
        print(f"   Статус: {project.status}")
        print(f"   Створено: {project.created_at.strftime('%Y-%m-%d %H:%M') if project.created_at else 'N/A'}")
        
        # Виводимо задачі проекту
        # Завдяки relationship у моделях можемо просто звернутися project.tasks
        if project.tasks:
            print(f"   Задачі ({len(project.tasks)}):")
            for task in project.tasks:
                print(f"     • {task.title}")
                print(f"       Статус: {task.status} | Пріоритет: {task.priority}")
        else:
            print("   Задач немає")
    
    print()
    print("=" * 60)
    print("ДЕМОНСТРАЦІЯ ОПЕРАЦІЙ")
    print("=" * 60)
    print()
    
    if projects:
        # Крок 5: Update - Оновлення проекту
        first_project = projects[0]
        print(f"📝 Оновлюємо проект '{first_project.name}'...")
        
        # Змінюємо поля об'єкта
        first_project.description = "Оновлений опис через SQLAlchemy"
        
        # Зберігаємо зміни
        session.commit()
        print("✓ Опис проекту оновлено")
        print()
        
        # Крок 6: Create - Додаємо нову задачу
        print(f"➕ Додаємо нову задачу...")
        new_task = Task(
            project_id=first_project.id,
            title="Написати документацію",
            description="README та API docs",
            status="todo",
            priority="low"
        )
        
        session.add(new_task)
        session.commit()
        print(f"✓ Задачу '{new_task.title}' додано з ID: {new_task.id}")
        print()
        
        # Крок 7: Read - Фільтрація задач
        print("🔍 Фільтруємо задачі за статусом 'todo'...")
        
        # filter() - SQL WHERE умова
        todo_tasks = session.query(Task).filter(Task.status == "todo").all()
        
        print(f"✓ Знайдено {len(todo_tasks)} задач зі статусом 'todo':")
        for task in todo_tasks:
            print(f"   • {task.title} (Проект ID: {task.project_id})")
        print()
    
    # Крок 8: Статистика
    print("=" * 60)
    print("ФІНАЛЬНА СТАТИСТИКА")
    print("=" * 60)
    
    total_projects = session.query(Project).count()
    total_tasks = session.query(Task).count()
    
    print(f"Всього проектів: {total_projects}")
    print(f"Всього задач: {total_tasks}")
    print(f"Файл БД: database.db")
    print()
    
    # Закриваємо сесію
    session.close()
    
    print("💡 Дані збережено у SQLite базі даних!")
    print("   Перезапустіть програму - дані завантажаться з БД.")
    print("=" * 60)


if __name__ == "__main__":
    main()
