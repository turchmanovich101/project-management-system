# -*- coding: utf-8 -*-
"""
Модуль models.py - моделі бази даних для проектів та задач.
Використовує SQLAlchemy ORM для роботи з SQLite базою даних.
"""

# Імпортуємо необхідні класи з SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

# Базовий клас для всіх моделей
# Всі моделі наслідуються від цього класу
Base = declarative_base()


class Project(Base):
    """
    Модель проекту - представляє таблицю projects в базі даних.
    Кожен проект може мати багато задач.
    """
    # Назва таблиці в базі даних
    __tablename__ = 'projects'
    
    # id - первинний ключ, автоматично збільшується
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # name - назва проекту (обов'язкове поле, не може бути NULL)
    name = Column(String(200), nullable=False)
    
    # description - опис проекту (може бути порожнім)
    description = Column(String(1000), default="")
    
    # status - статус проекту (active, completed, archived)
    # За замовчуванням "active"
    status = Column(String(50), default="active")
    
    # created_at - дата та час створення проекту
    # Автоматично встановлюється поточна дата/час
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Зв'язок з задачами - один проект має багато задач
    # cascade="all, delete-orphan" означає що при видаленні проекту видаляються всі його задачі
    # back_populates створює зворотній зв'язок (task.project)
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    
    def to_dict(self):
        """
        Конвертує об'єкт проекту в словник (для JSON API).
        
        Повертає:
            dict: Словник з даними проекту
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "tasks_count": len(self.tasks)  # Кількість задач у проекті
        }


class Task(Base):
    """
    Модель задачі - представляє таблицю tasks в базі даних.
    Кожна задача належить одному проекту.
    """
    # Назва таблиці в базі даних
    __tablename__ = 'tasks'
    
    # id - первинний ключ, автоматично збільшується
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # project_id - зовнішній ключ, посилання на проект
    # ForeignKey означає зв'язок з таблицею projects
    # nullable=False означає що задача обов'язково має належати проекту
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    
    # title - назва задачі (обов'язкове поле)
    title = Column(String(200), nullable=False)
    
    # description - опис задачі (може бути порожнім)
    description = Column(String(1000), default="")
    
    # status - статус задачі для Kanban board
    # todo - нова задача (колонка "To Do")
    # in_progress - задача в роботі (колонка "In Progress")
    # done - завершена задача (колонка "Done")
    status = Column(String(50), default="todo")
    
    # priority - пріоритет задачі (low, medium, high)
    # За замовчуванням "medium"
    priority = Column(String(50), default="medium")
    
    # assigned_to - ID користувача, якому призначена задача
    # Може бути NULL якщо задача не призначена
    assigned_to = Column(Integer, nullable=True, default=None)
    
    # due_date - термін виконання задачі
    # Може бути NULL
    due_date = Column(DateTime, nullable=True, default=None)
    
    # created_at - дата та час створення задачі
    # Автоматично встановлюється поточна дата/час
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Зв'язок з проектом - багато задач належать одному проекту
    # back_populates створює зворотній зв'язок (project.tasks)
    project = relationship("Project", back_populates="tasks")
    
    def to_dict(self):
        """
        Конвертує об'єкт задачі в словник (для JSON API).
        
        Повертає:
            dict: Словник з даними задачі
        """
        return {
            "id": self.id,
            "project_id": self.project_id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "assigned_to": self.assigned_to,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
