# -*- coding: utf-8 -*-
"""
Головний файл Flask додатку - REST API для керування проектами та задачами.
Надає HTTP endpoints для створення, читання, оновлення та видалення проектів/задач.
"""

# Імпортуємо Flask та необхідні модулі
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project_manager.models import Base, Project, Task
import os

# Створюємо Flask додаток
# __name__ вказує Flask де шукати templates та static файли
app = Flask(__name__)

# Дозволяємо CORS (Cross-Origin Resource Sharing)
# Це потрібно щоб фронтенд міг викликати API з іншого домену/порту
CORS(app)

# Налаштування бази даних
# Шлях до SQLite файлу бази даних
DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'database.db')

# Створюємо engine - з'єднання з базою даних
# sqlite:/// означає що використовуємо SQLite
# echo=True виводить всі SQL запити в консоль (для відлагодження)
engine = create_engine(f'sqlite:///{DATABASE_PATH}', echo=True)

# Створюємо всі таблиці в базі даних (якщо їх ще немає)
Base.metadata.create_all(engine)

# Створюємо фабрику сесій для роботи з базою даних
# Session - це клас для створення нових сесій
Session = sessionmaker(bind=engine)


# ============================================================================
# ROUTES - Маршрути для веб-інтерфейсу
# ============================================================================

@app.route('/')
def index():
    """
    Головна сторінка - Kanban board інтерфейс.
    Рендерить HTML шаблон з Kanban дошкою.
    """
    return render_template('index.html')


# ============================================================================
# API ENDPOINTS - REST API для роботи з проектами та задачами
# ============================================================================

# ===== PROJECTS API =====

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """
    GET /api/projects - отримати список всіх проектів.
    
    Повертає:
        JSON: Список проектів [{"id": 1, "name": "...", ...}, ...]
    """
    # Створюємо нову сесію для роботи з БД
    session = Session()
    
    try:
        # Виконуємо запит - отримуємо всі проекти
        projects = session.query(Project).all()
        
        # Конвертуємо об'єкти проектів в словники
        result = [project.to_dict() for project in projects]
        
        # Повертаємо JSON відповідь
        return jsonify(result), 200
    
    finally:
        # Завжди закриваємо сесію після роботи
        session.close()


@app.route('/api/projects', methods=['POST'])
def create_project():
    """
    POST /api/projects - створити новий проект.
    
    Тіло запиту (JSON):
        {
            "name": "Назва проекту",
            "description": "Опис проекту" (необов'язково),
            "status": "active" (необов'язково)
        }
    
    Повертає:
        JSON: Створений проект {"id": 1, "name": "...", ...}
    """
    # Отримуємо JSON дані з тіла запиту
    data = request.get_json()
    
    # Перевіряємо чи передано назву проекту
    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400
    
    # Створюємо нову сесію
    session = Session()
    
    try:
        # Створюємо новий об'єкт Project
        project = Project(
            name=data['name'],
            description=data.get('description', ''),  # Якщо description немає, використовуємо порожній рядок
            status=data.get('status', 'active')        # Якщо status немає, використовуємо 'active'
        )
        
        # Додаємо проект до сесії
        session.add(project)
        
        # Зберігаємо зміни в базі даних
        session.commit()
        
        # Повертаємо створений проект
        return jsonify(project.to_dict()), 201
    
    except Exception as e:
        # Якщо сталася помилка, відкатуємо зміни
        session.rollback()
        return jsonify({"error": str(e)}), 500
    
    finally:
        session.close()


@app.route('/api/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    """
    PUT /api/projects/<id> - оновити проект.
    
    Параметри:
        project_id (int): ID проекту для оновлення
    
    Тіло запиту (JSON):
        {
            "name": "Нова назва" (необов'язково),
            "description": "Новий опис" (необов'язково),
            "status": "completed" (необов'язково)
        }
    
    Повертає:
        JSON: Оновлений проект
    """
    data = request.get_json()
    session = Session()
    
    try:
        # Знаходимо проект за ID
        project = session.query(Project).filter(Project.id == project_id).first()
        
        # Якщо проект не знайдено, повертаємо 404
        if not project:
            return jsonify({"error": "Project not found"}), 404
        
        # Оновлюємо поля, які передані в запиті
        if 'name' in data:
            project.name = data['name']
        if 'description' in data:
            project.description = data['description']
        if 'status' in data:
            project.status = data['status']
        
        # Зберігаємо зміни
        session.commit()
        
        return jsonify(project.to_dict()), 200
    
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    
    finally:
        session.close()


@app.route('/api/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    """
    DELETE /api/projects/<id> - видалити проект.
    
    Параметри:
        project_id (int): ID проекту для видалення
    
    Повертає:
        JSON: {"success": true} або помилку
    """
    session = Session()
    
    try:
        # Знаходимо проект за ID
        project = session.query(Project).filter(Project.id == project_id).first()
        
        if not project:
            return jsonify({"error": "Project not found"}), 404
        
        # Видаляємо проект (задачі видаляться автоматично завдяки cascade)
        session.delete(project)
        session.commit()
        
        return jsonify({"success": True}), 200
    
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    
    finally:
        session.close()


# ===== TASKS API =====

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """
    GET /api/tasks - отримати список всіх задач.
    
    Query параметри:
        project_id (необов'язково): Фільтр за ID проекту
        status (необов'язково): Фільтр за статусом (todo, in_progress, done)
    
    Повертає:
        JSON: Список задач
    """
    session = Session()
    
    try:
        # Починаємо запит
        query = session.query(Task)
        
        # Застосовуємо фільтр за project_id якщо він переданий
        project_id = request.args.get('project_id')
        if project_id:
            query = query.filter(Task.project_id == int(project_id))
        
        # Застосовуємо фільтр за status якщо він переданий
        status = request.args.get('status')
        if status:
            query = query.filter(Task.status == status)
        
        # Виконуємо запит
        tasks = query.all()
        
        # Конвертуємо в словники
        result = [task.to_dict() for task in tasks]
        
        return jsonify(result), 200
    
    finally:
        session.close()


@app.route('/api/tasks', methods=['POST'])
def create_task():
    """
    POST /api/tasks - створити нову задачу.
    
    Тіло запиту (JSON):
        {
            "project_id": 1,
            "title": "Назва задачі",
            "description": "Опис" (необов'язково),
            "status": "todo" (необов'язково),
            "priority": "medium" (необов'язково)
        }
    
    Повертає:
        JSON: Створена задача
    """
    data = request.get_json()
    
    # Валідація обов'язкових полів
    if not data or 'project_id' not in data or 'title' not in data:
        return jsonify({"error": "project_id and title are required"}), 400
    
    session = Session()
    
    try:
        # Перевіряємо чи існує проект
        project = session.query(Project).filter(Project.id == data['project_id']).first()
        if not project:
            return jsonify({"error": "Project not found"}), 404
        
        # Створюємо нову задачу
        task = Task(
            project_id=data['project_id'],
            title=data['title'],
            description=data.get('description', ''),
            status=data.get('status', 'todo'),
            priority=data.get('priority', 'medium')
        )
        
        session.add(task)
        session.commit()
        
        return jsonify(task.to_dict()), 201
    
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    
    finally:
        session.close()


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    PUT /api/tasks/<id> - оновити задачу.
    
    Параметри:
        task_id (int): ID задачі для оновлення
    
    Тіло запиту (JSON):
        Будь-які поля задачі для оновлення
    
    Повертає:
        JSON: Оновлена задача
    """
    data = request.get_json()
    session = Session()
    
    try:
        task = session.query(Task).filter(Task.id == task_id).first()
        
        if not task:
            return jsonify({"error": "Task not found"}), 404
        
        # Оновлюємо поля
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'status' in data:
            task.status = data['status']
        if 'priority' in data:
            task.priority = data['priority']
        
        session.commit()
        
        return jsonify(task.to_dict()), 200
    
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    
    finally:
        session.close()


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    DELETE /api/tasks/<id> - видалити задачу.
    
    Параметри:
        task_id (int): ID задачі для видалення
    
    Повертає:
        JSON: {"success": true} або помилку
    """
    session = Session()
    
    try:
        task = session.query(Task).filter(Task.id == task_id).first()
        
        if not task:
            return jsonify({"error": "Task not found"}), 404
        
        session.delete(task)
        session.commit()
        
        return jsonify({"success": True}), 200
    
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    
    finally:
        session.close()


# ============================================================================
# ЗАПУСК ДОДАТКУ
# ============================================================================

if __name__ == '__main__':
    # Запускаємо Flask сервер
    # debug=True - автоматичне перезавантаження при зміні коду
    # host='0.0.0.0' - додаток доступний з усіх мережевих інтерфейсів
    # port=5001 - порт на якому працює сервер
    app.run(debug=True, host='0.0.0.0', port=5001)
