# -*- coding: utf-8 -*-
"""
Модуль repositories.py - Repository Pattern для Lab5.
Забезпечує шар абстракції між бізнес-логікою та базою даних.
Відділяє операції з даними від решти коду.
"""

from sqlalchemy.orm import Session
from .models import Project, Task


class ProjectRepository:
    """
    Repository для роботи з проектами.
    Інкапсулює всі операції з таблицею projects.
    """
    
    def __init__(self, session: Session):
        """
        Ініціалізує repository з сесією БД.
        
        Параметри:
            session (Session): Сесія SQLAlchemy для роботи з БД
        """
        self.session = session  # Зберігаємо сесію для використання в методах
    
    def create(self, name: str, description: str = "", status: str = "active") -> Project:
        """
        Створює новий проект.
        
        Параметри:
            name (str): Назва проекту
            description (str): Опис проекту
            status (str): Статус проекту
        
        Повертає:
            Project: Створений проект з присвоєним ID
        """
        # Створюємо новий об'єкт Project
        project = Project(
            name=name,
            description=description,
            status=status
        )
        
        # Додаємо до сесії та зберігаємо
        self.session.add(project)
        self.session.commit()
        
        # Оновлюємо об'єкт щоб отримати згенерований ID та інші поля
        self.session.refresh(project)
        
        return project
    
    def get_by_id(self, project_id: int) -> Project | None:
        """
        Знаходить проект за ID.
        
        Параметри:
            project_id (int): ID проекту
        
        Повертає:
            Project або None: Проект якщо знайдено, інакше None
        """
        # query().get() - швидкий пошук за первинним ключем
        return self.session.get(Project, project_id)
    
    def get_all(self) -> list[Project]:
        """
        Повертає всі проекти.
        
        Повертає:
            list[Project]: Список всіх проектів
        """
        # query().all() - вибирає всі записи
        return self.session.query(Project).all()
    
    def get_by_status(self, status: str) -> list[Project]:
        """
        Знаходить проекти за статусом.
        
        Параметри:
            status (str): Статус для фільтрації
        
        Повертає:
            list[Project]: Список проектів з вказаним статусом
        """
        # filter() - додає WHERE умову до запиту
        return self.session.query(Project).filter(Project.status == status).all()
    
    def update(self, project_id: int, **kwargs) -> Project | None:
        """
        Оновлює проект.
        
        Параметри:
            project_id (int): ID проекту для оновлення
            **kwargs: Поля для оновлення (name, description, status)
        
        Повертає:
            Project або None: Оновлений проект або None якщо не знайдено
        """
        # Знаходимо проект
        project = self.get_by_id(project_id)
        
        if not project:
            return None
        
        # Оновлюємо поля, які передано в kwargs
        for key, value in kwargs.items():
            if hasattr(project, key):  # Перевіряємо чи існує таке поле
                setattr(project, key, value)  # Встановлюємо нове значення
        
        # Зберігаємо зміни
        self.session.commit()
        self.session.refresh(project)
        
        return project
    
    def delete(self, project_id: int) -> bool:
        """
        Видаляє проект та всі його задачі.
        
        Параметри:
            project_id (int): ID проекту для видалення
        
        Повертає:
            bool: True якщо видалено успішно, False якщо проект не знайдено
        """
        project = self.get_by_id(project_id)
        
        if not project:
            return False
        
        # Видаляємо проект (задачі видаляться автоматично завдяки cascade)
        self.session.delete(project)
        self.session.commit()
        
        return True
    
    def count(self) -> int:
        """
        Повертає кількість проектів.
        
        Повертає:
            int: Кількість проектів у БД
        """
        return self.session.query(Project).count()


class TaskRepository:
    """
    Repository для роботи з задачами.
    Інкапсулює всі операції з таблицею tasks.
    """
    
    def __init__(self, session: Session):
        """
        Ініціалізує repository з сесією БД.
        
        Параметри:
            session (Session): Сесія SQLAlchemy
        """
        self.session = session
    
    def create(self, project_id: int, title: str, description: str = "",
               status: str = "todo", priority: str = "medium") -> Task | None:
        """
        Створює нову задачу.
        
        Параметри:
            project_id (int): ID проекту
            title (str): Назва задачі
            description (str): Опис задачі
            status (str): Статус задачі
            priority (str): Пріоритет задачі
        
        Повертає:
            Task або None: Створена задача або None якщо проект не існує
        """
        # Перевіряємо чи існує проект
        project = self.session.get(Project, project_id)
        if not project:
            return None
        
        # Створюємо задачу
        task = Task(
            project_id=project_id,
            title=title,
            description=description,
            status=status,
            priority=priority
        )
        
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        
        return task
    
    def get_by_id(self, task_id: int) -> Task | None:
        """
        Знаходить задачу за ID.
        
        Параметри:
            task_id (int): ID задачі
        
        Повертає:
            Task або None: Задача якщо знайдено
        """
        return self.session.get(Task, task_id)
    
    def get_all(self) -> list[Task]:
        """
        Повертає всі задачі.
        
        Повертає:
            list[Task]: Список всіх задач
        """
        return self.session.query(Task).all()
    
    def get_by_project(self, project_id: int) -> list[Task]:
        """
        Знаходить всі задачі проекту.
        
        Параметри:
            project_id (int): ID проекту
        
        Повертає:
            list[Task]: Список задач проекту
        """
        return self.session.query(Task).filter(Task.project_id == project_id).all()
    
    def get_by_status(self, status: str) -> list[Task]:
        """
        Знаходить задачі за статусом.
        
        Параметри:
            status (str): Статус для фільтрації
        
        Повертає:
            list[Task]: Список задач з вказаним статусом
        """
        return self.session.query(Task).filter(Task.status == status).all()
    
    def get_by_priority(self, priority: str) -> list[Task]:
        """
        Знаходить задачі за пріоритетом.
        
        Параметри:
            priority (str): Пріоритет для фільтрації
        
        Повертає:
            list[Task]: Список задач з вказаним пріоритетом
        """
        return self.session.query(Task).filter(Task.priority == priority).all()
    
    def update(self, task_id: int, **kwargs) -> Task | None:
        """
        Оновлює задачу.
        
        Параметри:
            task_id (int): ID задачі
            **kwargs: Поля для оновлення
        
        Повертає:
            Task або None: Оновлена задача або None якщо не знайдено
        """
        task = self.get_by_id(task_id)
        
        if not task:
            return None
        
        # Оновлюємо поля
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)
        
        self.session.commit()
        self.session.refresh(task)
        
        return task
    
    def delete(self, task_id: int) -> bool:
        """
        Видаляє задачу.
        
        Параметри:
            task_id (int): ID задачі для видалення
        
        Повертає:
            bool: True якщо видалено успішно
        """
        task = self.get_by_id(task_id)
        
        if not task:
            return False
        
        self.session.delete(task)
        self.session.commit()
        
        return True
    
    def count(self) -> int:
        """
        Повертає кількість задач.
        
        Повертає:
            int: Кількість задач у БД
        """
        return self.session.query(Task).count()
