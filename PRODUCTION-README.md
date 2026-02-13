# 🚀 Project Management System - Production Version

Full-featured team collaboration platform with authentication, role-based access, Kanban board, calendar, file attachments, and real-time updates.

---

## 🌟 Features

### Authentication & Security
- ✅ Login/logout system with session management
- ✅ Password hashing (SHA256)
- ✅ Role-based access control (CEO vs Team Member)
- ✅ Session persistence
- ✅ Automatic logout on token expiry

### Role-Based Features

**CEO Account:**
- View all projects and tasks across the organization
- Create and manage projects
- Assign tasks to team members
- Delete projects and tasks
- Add new team members
- View team statistics
- Full system administration

**Team Member Account:**
- View only assigned tasks
- Update task status and details
- Add comments and attachments
- Track personal progress
- View personal statistics

### Project Management
- ✅ Create/Edit/Delete projects
- ✅ Project status tracking (Active, Completed, Archived)
- ✅ Project descriptions and metadata
- ✅ Owner tracking
- ✅ Task count per project

### Task Management
- ✅ Create/Edit/Delete tasks
- ✅ **Drag & Drop between Kanban columns**
- ✅ Task assignment to team members
- ✅ Priority levels (High, Medium, Low) with color coding
- ✅ Status tracking (TO DO, IN PROGRESS, DONE)
- ✅ Due dates with calendar integration
- ✅ Task descriptions
- ✅ **File attachments** (up to 16MB per file)
- ✅ Overdue task detection

### Kanban Board
- ✅ 3-column layout (TO DO → IN PROGRESS → DONE)
- ✅ **Drag and drop tasks between columns**
- ✅ Visual priority indicators (colored borders)
- ✅ Assignee display on cards
- ✅ Due date display with overdue highlighting
- ✅ Real-time counters
- ✅ Edit/delete buttons on cards
- ✅ Smooth animations and hover effects

### Search & Filtering
- ✅ **Real-time search** (searches task titles and descriptions)
- ✅ Filter by project
- ✅ Filter by priority (High/Medium/Low)
- ✅ Filter by assignee
- ✅ Combined filters (all work together)
- ✅ Instant results

### Calendar View
- ✅ Monthly calendar display
- ✅ Tasks shown on due dates
- ✅ Color-coded by priority
- ✅ Click task to edit
- ✅ "Today" highlighting
- ✅ Navigation (previous/next month)
- ✅ Multiple tasks per day support

### Dashboard & Statistics
- ✅ Real-time statistics cards
- ✅ Total projects and tasks
- ✅ Tasks by status breakdown
- ✅ High priority task count
- ✅ Overdue task alerts
- ✅ Team member count (CEO only)
- ✅ Color-coded stat cards

### Team Management (CEO Only)
- ✅ View all team members
- ✅ Add new team members
- ✅ Assign roles (CEO or Team Member)
- ✅ View team member statistics
- ✅ Task counts per member
- ✅ Avatar placeholders

### File Attachments
- ✅ Upload multiple files per task
- ✅ Supported formats: PDF, PNG, JPG, JPEG, GIF, DOC, DOCX, XLS, XLSX, TXT, ZIP
- ✅ 16MB file size limit
- ✅ File download functionality
- ✅ File size display
- ✅ Upload tracking (who uploaded when)
- ✅ Secure file storage

### User Experience
- ✅ **Keyboard shortcuts:**
  - `Ctrl/Cmd + K`: Focus search
  - `N`: New task
  - `P`: New project
  - `Esc`: Close modals
- ✅ Responsive sidebar navigation
- ✅ Beautiful gradient design
- ✅ Smooth animations
- ✅ Loading states
- ✅ Error handling
- ✅ Confirmation dialogs
- ✅ Toast notifications
- ✅ Mobile-friendly layout

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd lab6
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run Production Server

```bash
cd src
python app_production.py
```

Server starts on `http://localhost:5002`

### 3. Login with Demo Accounts

**CEO Account (Full Access):**
```
Username: ceo
Password: ceo123
```

**Team Member Accounts:**
```
Username: john
Password: john123

Username: jane
Password: jane123
```

---

## 📖 How to Use

### For CEO

1. **Login** with `ceo` / `ceo123`
2. **Dashboard Tab:**
   - View system-wide statistics
   - Quick actions (New Project, New Task)
3. **Kanban Board Tab:**
   - See all tasks from all projects
   - **Drag tasks** between columns to update status
   - Filter by project/priority/assignee
   - Search for specific tasks
   - Click ✏️ to edit, 🗑️ to delete
4. **Calendar Tab:**
   - View all tasks with due dates
   - Navigate between months
   - Click task to edit
5. **Team Tab:**
   - View all team members
   - Add new members
   - See each member's task stats

### For Team Members

1. **Login** with your username/password
2. **Dashboard Tab:**
   - View your personal statistics
   - Quick actions for your tasks
3. **Kanban Board Tab:**
   - See only tasks assigned to you
   - **Drag your tasks** between columns
   - Update task details
   - Add attachments
4. **Calendar Tab:**
   - View your tasks with due dates

### Creating a Project

1. Click **"➕ New Project"**
2. Enter project name
3. Add description (optional)
4. Select status (Active/Completed/Archived)
5. Click **"Save"**

### Creating a Task

1. Click **"✓ New Task"**
2. Select project
3. Enter task title
4. Add description (optional)
5. Select priority (Low/Medium/High)
6. Assign to team member
7. Set due date (optional)
8. Select status
9. Click **"Save"**

### Editing a Task

1. Click ✏️ on task card
2. Update any fields
3. **Upload files** (if editing existing task)
4. Click **"Save"**

### Drag & Drop Tasks

1. Navigate to Kanban Board
2. Click and hold a task card
3. Drag to TO DO / IN PROGRESS / DONE column
4. Release to drop
5. Status updates automatically

### Uploading Files

1. Edit an existing task (files only work on saved tasks)
2. Scroll to "📎 Attachments" section
3. Click the upload area
4. Select file(s) (max 16MB each)
5. Files upload automatically
6. Click ⬇️ to download

### Searching Tasks

1. Type in search box at top
2. Results update as you type (300ms delay)
3. Or click 🔍 button
4. Searches task titles and descriptions

### Using Filters

1. Go to Kanban Board
2. Select project from dropdown
3. Select priority filter
4. Select team member
5. All filters combine

---

## 🎨 UI Design

### Color Scheme

**Gradients:**
- Primary: Purple-Blue (`#667eea` → `#764ba2`)

**Task Priorities:**
- 🔴 High: Red (`#f56565`)
- 🟡 Medium: Orange (`#ed8936`)
- 🟢 Low: Green (`#48bb78`)

**Status Colors:**
- Success: Green
- Warning: Orange
- Danger: Red
- Primary: Purple

### Typography

- **Font:** -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto
- **Headings:** 700 weight
- **Body:** 400 weight
- **Labels:** 600 weight

### Layout

- **Sidebar:** 260px fixed left
- **Main Content:** Responsive right area
- **Modals:** Centered overlay with backdrop blur
- **Cards:** Rounded corners, subtle shadows
- **Animations:** 0.3s ease transitions

---

## 🔧 API Endpoints

### Authentication

```
POST   /api/auth/login          # Login
POST   /api/auth/logout         # Logout
GET    /api/auth/me             # Get current user
```

### Projects

```
GET    /api/projects            # List projects
POST   /api/projects            # Create project
PUT    /api/projects/{id}       # Update project
DELETE /api/projects/{id}       # Delete project (CEO only)
```

### Tasks

```
GET    /api/tasks               # List tasks (with filters)
  ?project_id=1                 # Filter by project
  ?status=todo                  # Filter by status
  ?priority=high                # Filter by priority
  ?assigned_to=2                # Filter by assignee
  ?search=backend               # Search text

POST   /api/tasks               # Create task
PUT    /api/tasks/{id}          # Update task
DELETE /api/tasks/{id}          # Delete task (CEO only)
```

### File Attachments

```
POST   /api/tasks/{id}/attachments        # Upload file
GET    /api/tasks/{id}/attachments        # List files
GET    /api/attachments/{id}/download     # Download file
```

### Users (CEO Only)

```
GET    /api/users               # List team members
POST   /api/users               # Create user
```

### Dashboard

```
GET    /api/dashboard/stats     # Get statistics
GET    /api/calendar/tasks      # Get calendar events
  ?start=2026-02-01             # Date range start
  &end=2026-02-28               # Date range end
```

---

## 💾 Database Schema

### Users Table
```sql
- id: INTEGER PRIMARY KEY
- username: VARCHAR(100) UNIQUE
- email: VARCHAR(200) UNIQUE
- password_hash: VARCHAR(200)
- full_name: VARCHAR(200)
- role: VARCHAR(50)  -- 'ceo' or 'team_member'
- is_active: BOOLEAN
- created_at: DATETIME
```

### Projects Table
```sql
- id: INTEGER PRIMARY KEY
- name: VARCHAR(200)
- description: TEXT
- status: VARCHAR(50)  -- 'active', 'completed', 'archived'
- owner_id: INTEGER (FK users.id)
- created_at: DATETIME
- updated_at: DATETIME
```

### Tasks Table
```sql
- id: INTEGER PRIMARY KEY
- project_id: INTEGER (FK projects.id)
- title: VARCHAR(200)
- description: TEXT
- status: VARCHAR(50)  -- 'todo', 'in_progress', 'done'
- priority: VARCHAR(50)  -- 'low', 'medium', 'high'
- assigned_to: INTEGER (FK users.id)
- due_date: DATETIME
- created_at: DATETIME
- updated_at: DATETIME
```

### Task Attachments Table
```sql
- id: INTEGER PRIMARY KEY
- task_id: INTEGER (FK tasks.id)
- filename: VARCHAR(200)
- original_filename: VARCHAR(200)
- file_path: VARCHAR(500)
- file_size: INTEGER
- uploaded_by: INTEGER (FK users.id)
- uploaded_at: DATETIME
```

---

## 🔐 Security Notes

**Current Implementation (Demo):**
- Password hashing: SHA256 (simple for demo)
- Session: Flask session cookies
- File validation: Extension whitelist

**For Production Deployment:**
- Use bcrypt/scrypt for passwords
- Add HTTPS
- Implement JWT tokens
- Add rate limiting
- Sanitize file uploads
- Add CSRF protection
- Environment variables for secrets
- Database backups

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5002
lsof -ti:5002 | xargs kill -9

# Or change port in app_production.py:
app.run(debug=True, host='0.0.0.0', port=5003)
```

### Database Issues
```bash
# Delete and recreate database
rm database_production.db
python app_production.py  # Creates fresh DB with default users
```

### File Upload Fails
- Check uploads/ folder exists
- Verify file size < 16MB
- Check file extension is allowed
- Task must be saved before uploading

### Login Issues
- Clear browser cookies
- Check username/password exactly (case-sensitive)
- Verify server is running
- Check browser console for errors

---

## 📊 Performance

**Backend:**
- SQLite database (suitable for <100 concurrent users)
- SQLAlchemy ORM (lazy loading for efficiency)
- Session management with Flask
- File storage: Local filesystem

**Frontend:**
- Vanilla JavaScript (no framework overhead)
- Real-time search with debouncing (300ms)
- Drag & drop: Native HTML5 API
- Animations: CSS transforms (GPU accelerated)

**Scalability:**
- For production: Switch to PostgreSQL
- Add Redis for session storage
- Use S3 for file storage
- Add Nginx reverse proxy
- Implement caching

---

## 📚 Technologies

**Backend:**
- Python 3.9+
- Flask 3.0 (Web framework)
- SQLAlchemy 2.0 (ORM)
- SQLite (Database)
- Flask-CORS (API access)
- Flask-Login (Session management)
- python-dateutil (Date parsing)

**Frontend:**
- HTML5
- CSS3 (Grid, Flexbox, Animations)
- JavaScript ES6+ (Async/Await, Fetch API)
- Flatpickr (Date picker)

**Infrastructure:**
- Git (Version control)
- GitHub (Code hosting)

---

## 🎯 Future Enhancements

- [ ] Real-time updates (WebSockets)
- [ ] Email notifications
- [ ] Task comments/discussion
- [ ] Activity log/audit trail
- [ ] Export to CSV/PDF
- [ ] Recurring tasks
- [ ] Task dependencies
- [ ] Time tracking
- [ ] Sprint/milestone management
- [ ] Dark mode
- [ ] Mobile app
- [ ] Integrations (Slack, Discord)
- [ ] Two-factor authentication
- [ ] Custom fields
- [ ] Webhooks
- [ ] Public API with OAuth

---

## 📝 License

Educational project for university coursework.

---

## 👨‍💻 Author

Anna Novychann  
University Assignment #28 - Project Management System  
February 2026

---

## 🙏 Acknowledgments

- GitLab reference materials: `okarnaukhov/python_lectures_2025`
- Design inspiration: Trello, Notion, Linear
- Flask documentation
- SQLAlchemy guides

---

## 📞 Support

For issues or questions:
1. Check Troubleshooting section above
2. Review browser console for errors
3. Check server logs (terminal output)
4. Verify all dependencies installed
5. Ensure Python 3.9+ is used

---

**GitHub:** https://github.com/turchmanovich101/project-management-system

**Server:** http://localhost:5002 (when running locally)

**Demo Accounts:** ceo/ceo123, john/john123, jane/jane123
