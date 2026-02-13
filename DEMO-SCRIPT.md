# 📹 Demo Video Script - Kanban Board Project Management System

## Duration: ~5 minutes

---

## Introduction (30 seconds)

**Show:** Open README.md in VS Code

**Say:** "Це система керування проектами з Kanban board інтерфейсом. Проект складається з 6 лабораторних робіт, кожна додає нову функціональність."

**Show:** Scroll through the 6 labs in file explorer:
- Lab1: Basic CRUD
- Lab2: Extended CRUD
- Lab3: File Storage
- Lab4: SQLite Database
- Lab5: Repository Pattern
- Lab6: Flask REST API + Kanban Board

---

## Lab1 Demo - Basic CRUD (30 seconds)

**Terminal:**
```bash
cd lab1/src
python3 main.py
```

**Say:** "Lab1 - базові CRUD операції. Створюємо проекти та задачі в пам'яті."

**Show:** Output showing projects and tasks being created

---

## Lab3 Demo - File Storage (30 seconds)

**Terminal:**
```bash
cd ../../lab3/src
python3 main.py
```

**Say:** "Lab3 - зберігання даних у JSON файлах. Дані зберігаються між запусками."

**Show:** 
1. Program output
2. Open `data.json` file to show saved data
3. Run program again to show data loading

---

## Lab6 Demo - Kanban Board (3 minutes)

**Browser:** Open http://localhost:5001

### 1. Show Empty State (15 seconds)

**Show:** Clean interface with 3 columns (TO DO, IN PROGRESS, DONE)

**Say:** "Lab6 - веб-інтерфейс з Kanban дошкою. Схожий на Trello або Notion."

### 2. Create First Project (30 seconds)

**Actions:**
1. Click "➕ Новий Проект"
2. Enter name: "Веб-розробка"
3. Enter description: "Розробка сайту для компанії"
4. Click "Створити"

**Show:** Project appears in selector dropdown

**Say:** "Створюємо проект через модальне вікно."

### 3. Create Tasks (45 seconds)

**Select the project from dropdown**

**Create 3 tasks:**

**Task 1:**
- Title: "Дизайн головної сторінки"
- Description: "Створити макет у Figma"
- Priority: Високий 🔴
- Click "Створити"

**Task 2:**
- Title: "Backend API"
- Description: "REST endpoints"
- Priority: Високий 🔴

**Task 3:**
- Title: "Написати тести"
- Description: "Unit тести"
- Priority: Середній 🟡

**Say:** "Додаємо задачі з різними пріоритетами. Червона смужка = високий пріоритет."

**Show:** All 3 tasks appear in TO DO column

### 4. Drag & Drop Demo (45 seconds)

**Actions:**
1. Drag "Backend API" from TO DO → IN PROGRESS
2. Show counter updates (TO DO: 2, IN PROGRESS: 1)
3. Drag "Дизайн головної сторінки" from TO DO → DONE
4. Show counter updates
5. Drag task back to IN PROGRESS

**Say:** "Просто перетягуємо задачі між колонками. Статус оновлюється автоматично в базі даних."

### 5. Show Multiple Projects (30 seconds)

**Actions:**
1. Click "➕ Новий Проект"
2. Create "Мобільний додаток"
3. Switch to new project in dropdown
4. Add 2 tasks to the new project
5. Switch back to first project

**Say:** "Кожен проект має свої задачі. Можна легко перемикатися між проектами."

### 6. Show Priority Colors (15 seconds)

**Show:** Zoom in on tasks to highlight colored borders:
- 🔴 Red border = High priority
- 🟡 Orange border = Medium priority
- 🟢 Green border = Low priority

**Say:** "Колір смужки показує пріоритет задачі."

### 7. Delete Task Demo (15 seconds)

**Actions:**
1. Click 🗑️ icon on one task
2. Confirm deletion
3. Show task disappears and counter updates

**Say:** "Видалення задач працює миттєво."

---

## Code Explanation (30 seconds)

**Show:** Open `lab6/src/app.py` in VS Code

**Scroll through and highlight:**
1. Flask routes (`@app.route`)
2. SQLAlchemy queries (`session.query(Project).all()`)
3. JSON responses (`jsonify()`)

**Say:** "Весь код детально прокоментовано українською мовою. README містить пояснення кожного рядка."

---

## README Demo (30 seconds)

**Show:** README.md in VS Code

**Scroll through sections:**
1. Quick Start
2. API Documentation
3. Code Explanations with comments
4. Technologies Used

**Say:** "Повна документація з інструкціями по встановленню та поясненнями коду."

---

## Conclusion (15 seconds)

**Terminal:**
```bash
git log --oneline
```

**Show:** Commit history

**Say:** "Весь код на GitHub: github.com/turchmanovich101/project-management-system. 6 лабораторних робіт виконано. Дякую за перегляд!"

**End with browser showing the working Kanban board**

---

## Recording Tips

1. **Resolution:** 1920x1080 minimum
2. **Frame Rate:** 30fps
3. **Audio:** Clear microphone, no background noise
4. **Cursor:** Make sure cursor is visible
5. **Pace:** Speak slowly and clearly
6. **Zoom:** Zoom in on important details (priority colors, drag & drop)
7. **Transitions:** Smooth transitions between demos

## Tools

- **macOS:** QuickTime Player (File → New Screen Recording)
- **Windows:** OBS Studio or Xbox Game Bar
- **Linux:** SimpleScreenRecorder or OBS Studio

## Upload

- YouTube (Unlisted or Public)
- Google Drive
- Or send the .mp4 file directly
