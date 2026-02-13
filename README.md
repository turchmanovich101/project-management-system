# 📋 Система Керування Проектами - Kanban Board

Повноцінна система для керування проектами з Kanban board інтерфейсом (як Trello/Notion).

---

## 📚 Структура Проекту

Проект складається з 6 лабораторних робіт, кожна з яких розширює функціональність системи:

### Lab 1: Базові CRUD операції
- **Функції**: `create_project`, `add_task`, `list_projects`, `list_tasks`
- **Зберігання**: У пам'яті (словники Python)
- **Призначення**: Створення та перегляд проектів і задач

### Lab 2: Розширені CRUD операції
- **Додано**: `update_project`, `update_task`, `delete_project`, `delete_task`
- **Призначення**: Повний цикл CRUD (Create, Read, Update, Delete)

### Lab 3: Файлове зберігання
- **Формат**: JSON файли
- **Функції**: Збереження та завантаження даних з файлів
- **Призначення**: Збереження даних між запусками програми

### Lab 4: SQLite база даних
- **Технологія**: SQLAlchemy ORM + SQLite
- **Моделі**: Project, Task з зв'язками
- **Призначення**: Професійне зберігання даних у БД

### Lab 5: Repository Pattern
- **Архітектура**: Шар абстракції для роботи з даними
- **Класи**: ProjectRepository, TaskRepository
- **Призначення**: Відділення бізнес-логіки від роботи з БД

### Lab 6: Flask REST API + Kanban Board ⭐
- **Backend**: Flask REST API
- **Frontend**: Kanban Board UI (Drag & Drop)
- **База даних**: SQLite через SQLAlchemy
- **Дизайн**: Сучасний інтерфейс як Trello/Notion
- **Фічі**: 
  - 3 колонки: TO DO → IN PROGRESS → DONE
  - Drag & Drop для переміщення задач
  - Пріоритети задач (Низький, Середній, Високий)
  - Модальні вікна для створення проектів та задач
  - Реал-тайм оновлення через REST API

---

## 🚀 Швидкий Старт (Lab 6)

### 1. Встановлення залежностей

```bash
cd lab6
python3 -m venv .venv
source .venv/bin/activate  # На Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Запуск сервера

```bash
cd src
python app.py
```

Сервер запуститься на `http://localhost:5001`

### 3. Відкрити у браузері

Перейдіть на http://localhost:5001 - ви побачите Kanban Board

---

## 💻 Використання API (Lab 6)

### Проекти

#### Отримати всі проекти
```http
GET /api/projects
```

**Відповідь:**
```json
[
  {
    "id": 1,
    "name": "Веб-розробка",
    "description": "Розробка нового сайту",
    "status": "active",
    "created_at": "2026-02-13T10:30:00",
    "tasks_count": 5
  }
]
```

#### Створити проект
```http
POST /api/projects
Content-Type: application/json

{
  "name": "Новий проект",
  "description": "Опис проекту",
  "status": "active"
}
```

#### Оновити проект
```http
PUT /api/projects/1
Content-Type: application/json

{
  "name": "Оновлена назва",
  "status": "completed"
}
```

#### Видалити проект
```http
DELETE /api/projects/1
```

### Задачі

#### Отримати всі задачі
```http
GET /api/tasks
GET /api/tasks?project_id=1  # Фільтр за проектом
GET /api/tasks?status=todo    # Фільтр за статусом
```

**Відповідь:**
```json
[
  {
    "id": 1,
    "project_id": 1,
    "title": "Створити дизайн",
    "description": "Розробити макет у Figma",
    "status": "todo",
    "priority": "high",
    "created_at": "2026-02-13T10:35:00"
  }
]
```

#### Створити задачу
```http
POST /api/tasks
Content-Type: application/json

{
  "project_id": 1,
  "title": "Нова задача",
  "description": "Опис задачі",
  "status": "todo",
  "priority": "medium"
}
```

#### Оновити задачу
```http
PUT /api/tasks/1
Content-Type: application/json

{
  "status": "in_progress",
  "priority": "high"
}
```

#### Видалити задачу
```http
DELETE /api/tasks/1
```

---

## 🎨 Інтерфейс Kanban Board

### Функції:

1. **Створення Проектів**
   - Натисніть "➕ Новий Проект"
   - Введіть назву та опис
   - Проект з'явиться у селекторі

2. **Створення Задач**
   - Виберіть проект зі списку
   - Натисніть "✓ Нова Задача"
   - Введіть назву, опис та пріоритет
   - Задача з'явиться у колонці "TO DO"

3. **Переміщення Задач (Drag & Drop)**
   - Перетягніть задачу з однієї колонки в іншу
   - Статус автоматично оновлюється на сервері
   - Лічильники оновлюються миттєво

4. **Пріоритети Задач**
   - 🔴 Високий (High) - червона смужка зліва
   - 🟡 Середній (Medium) - помаранчева смужка
   - 🟢 Низький (Low) - зелена смужка

5. **Видалення Задач**
   - Натисніть 🗑️ на картці задачі
   - Підтвердіть видалення

### Колонки Kanban:

1. **📝 TO DO** - нові задачі (status: `todo`)
2. **🚀 IN PROGRESS** - задачі в роботі (status: `in_progress`)
3. **✅ DONE** - завершені задачі (status: `done`)

---

## 📖 Пояснення Коду

### Backend (Flask API)

#### `app.py` - Головний файл додатку

```python
# Створення Flask додатку
app = Flask(__name__)
```
- `Flask(__name__)` - створює екземпляр веб-додатку
- `__name__` вказує Flask де шукати templates та static файли

```python
CORS(app)
```
- Дозволяє Cross-Origin Resource Sharing
- Потрібно щоб фронтенд міг викликати API з іншого порту

```python
engine = create_engine(f'sqlite:///{DATABASE_PATH}', echo=True)
```
- `create_engine()` - створює з'єднання з БД
- `sqlite:///` - використовуємо SQLite файл
- `echo=True` - виводить SQL запити в консоль (для відлагодження)

```python
Base.metadata.create_all(engine)
```
- Створює всі таблиці в БД згідно з моделями
- Якщо таблиці вже існують, нічого не робить

```python
Session = sessionmaker(bind=engine)
```
- Створює фабрику сесій для роботи з БД
- Кожна сесія - це транзакція з БД

```python
@app.route('/api/projects', methods=['GET'])
def get_projects():
    session = Session()
    try:
        projects = session.query(Project).all()
        return jsonify([p.to_dict() for p in projects]), 200
    finally:
        session.close()
```
- `@app.route()` - декоратор, який реєструє URL маршрут
- `Session()` - створює нову сесію БД
- `query(Project).all()` - вибирає всі проекти з БД
- `to_dict()` - конвертує об'єкт у словник
- `jsonify()` - конвертує Python об'єкти в JSON
- `finally` - завжди закриває сесію (навіть якщо є помилка)

```python
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    session = Session()
    try:
        task = session.query(Task).filter(Task.id == task_id).first()
        if not task:
            return jsonify({"error": "Task not found"}), 404
        
        if 'status' in data:
            task.status = data['status']
        
        session.commit()
        return jsonify(task.to_dict()), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()
```
- `<int:task_id>` - параметр URL (автоматично конвертується в int)
- `request.get_json()` - отримує JSON дані з тіла запиту
- `filter()` - SQL WHERE умова
- `first()` - повертає перший результат або None
- `commit()` - зберігає зміни в БД
- `rollback()` - відкочує зміни у разі помилки

#### `models.py` - Моделі бази даних

```python
Base = declarative_base()
```
- Базовий клас для всіх моделей SQLAlchemy
- Всі моделі наслідуються від нього

```python
class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    status = Column(String(50), default="active")
    
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
```
- `__tablename__` - назва таблиці в БД
- `Column()` - визначає стовпець таблиці
- `primary_key=True` - це первинний ключ
- `nullable=False` - поле обов'язкове
- `default="active"` - значення за замовчуванням
- `relationship()` - зв'язок з іншою таблицею (один-до-багатьох)
- `cascade="all, delete-orphan"` - при видаленні проекту видаляються його задачі
- `back_populates` - створює зворотній зв'язок (task.project)

```python
class Task(Base):
    __tablename__ = 'tasks'
    
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    
    project = relationship("Project", back_populates="tasks")
```
- `ForeignKey()` - зовнішній ключ (посилання на іншу таблицю)
- Це створює зв'язок багато-до-одного (багато задач → один проект)

```python
def to_dict(self):
    return {
        "id": self.id,
        "name": self.name,
        "status": self.status
    }
```
- Метод конвертації об'єкта в словник
- Використовується для створення JSON відповідей

### Frontend (Kanban Board)

#### HTML Структура

```html
<div class="kanban-column" data-status="todo">
    <div class="task-list" id="tasks-todo" 
         ondrop="drop(event)" 
         ondragover="allowDrop(event)">
    </div>
</div>
```
- `data-status` - атрибут для зберігання статусу колонки
- `ondrop` - обробник події "відпустили об'єкт"
- `ondragover` - обробник події "тягнуть над елементом"

#### JavaScript Drag & Drop

```javascript
function drag(event) {
    event.dataTransfer.setData('taskId', event.target.dataset.taskId);
    event.target.classList.add('dragging');
}
```
- `event.dataTransfer.setData()` - зберігає дані про об'єкт, що тягнеться
- `dataset.taskId` - отримує значення атрибуту `data-task-id`
- `classList.add()` - додає CSS клас для візуального ефекту

```javascript
async function drop(event) {
    event.preventDefault();
    const taskId = event.dataTransfer.getData('taskId');
    const newStatus = event.currentTarget.id.replace('tasks-', '');
    
    await fetch(`${API_URL}/tasks/${taskId}`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ status: newStatus })
    });
    
    loadTasks();
}
```
- `event.preventDefault()` - запобігає стандартній поведінці браузера
- `getData()` - отримує збережені дані
- `currentTarget.id` - ID елемента, на який відпустили
- `fetch()` - робить HTTP запит до API
- `async/await` - асинхронний код (очікує відповіді від сервера)
- `JSON.stringify()` - конвертує JavaScript об'єкт в JSON рядок

#### Створення Задачі

```javascript
async function createTask() {
    const projectId = document.getElementById('projectSelect').value;
    const title = document.getElementById('taskTitle').value.trim();
    
    if (!title) {
        alert('Введіть назву задачі!');
        return;
    }

    await fetch(`${API_URL}/tasks`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            project_id: parseInt(projectId),
            title: title,
            description: document.getElementById('taskDescription').value,
            priority: document.getElementById('taskPriority').value,
            status: 'todo'
        })
    });
    
    closeTaskModal();
    loadTasks();
}
```
- `document.getElementById()` - знаходить елемент за ID
- `.value` - отримує значення input/select елемента
- `.trim()` - видаляє пробіли на початку та кінці
- `parseInt()` - конвертує рядок в число
- `method: 'POST'` - HTTP метод для створення нового ресурсу
- `headers` - HTTP заголовки (вказуємо що відправляємо JSON)
- Після створення закриваємо модалку і перезавантажуємо задачі

---

## 🧪 Тестування (Labs 1-2)

```bash
cd lab1  # або lab2
source .venv/bin/activate
pytest tests/
```

### Приклад тестів:

```python
def test_create_project():
    """Тестуємо створення проекту"""
    project_id = manager.create_project("Тест", "Опис", "active")
    assert project_id == 1  # Перевіряємо що ID = 1
    assert project_id in manager.projects  # Перевіряємо що проект збережено
    
    project = manager.projects[project_id]
    assert project["name"] == "Тест"  # Перевіряємо назву
```

- `assert` - перевірка умови (тест падає якщо False)
- Кожен тест запускається з чистою пам'яттю (фікстура `reset_data`)

---

## 📁 Структура Файлів

```
project-management/
├── lab1/                      # Базові CRUD операції
│   ├── src/
│   │   ├── project_manager/
│   │   │   ├── __init__.py
│   │   │   └── manager.py     # Логіка CRUD
│   │   └── main.py            # Демонстрація
│   ├── tests/
│   │   └── test_project_manager.py
│   ├── requirements.txt
│   ├── setup.py
│   ├── pytest.ini
│   └── tox.ini
│
├── lab2/                      # Розширені CRUD операції
│   └── ...                    # Аналогічна структура
│
├── lab6/                      # Flask REST API + Kanban Board
│   ├── src/
│   │   ├── project_manager/
│   │   │   ├── __init__.py
│   │   │   └── models.py      # SQLAlchemy моделі
│   │   ├── templates/
│   │   │   └── index.html     # Kanban Board UI
│   │   └── app.py             # Flask додаток
│   ├── database.db            # SQLite база даних
│   ├── requirements.txt
│   └── setup.py
│
└── README.md                  # Ця документація
```

---

## 🛠️ Технології

- **Python 3.8+** - Мова програмування
- **Flask 3.0** - Веб-фреймворк
- **SQLAlchemy 2.0** - ORM для роботи з БД
- **SQLite** - Легка файлова база даних
- **Flask-CORS** - CORS підтримка для API
- **Pytest** - Тестування
- **HTML5 + CSS3 + JavaScript (ES6+)** - Фронтенд

---

## 🎯 Можливості для Розвитку

1. **Аутентифікація користувачів**
   - Додати логін/реєстрацію
   - Кожен користувач бачить тільки свої проекти

2. **Деталі задач**
   - Додати дедлайни
   - Прикріплення файлів
   - Коментарі до задач
   - Призначення виконавців

3. **Фільтрація та пошук**
   - Пошук задач за назвою
   - Фільтр за пріоритетом
   - Сортування

4. **Статистика**
   - Кількість завершених задач
   - Середній час виконання
   - Графіки прогресу

5. **Кастомізація**
   - Налаштування кольорів
   - Додавання власних колонок
   - Налаштування пріоритетів

---

## 📝 Ліцензія

Навчальний проект для університету.

---

## 👤 Автор

Student - Університетська лабораторна робота №28 (Система керування проектами)

---

## 🙏 Подяки

- Instructor: okarnaukhov (GitLab)
- Лекційні матеріали: https://gitlab.com/okarnaukhov/python_lectures_2025
