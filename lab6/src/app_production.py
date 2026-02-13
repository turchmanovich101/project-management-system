# -*- coding: utf-8 -*-
"""
Production Flask App - Complete Project Management System
Features: Authentication, Team Management, Dashboard, File Uploads, Calendar
"""

from flask import Flask, request, jsonify, render_template, send_from_directory, session
from flask_cors import CORS
from sqlalchemy import create_engine, or_, func
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from dateutil import parser as date_parser
import os
import json

# Import enhanced models
from project_manager.models_enhanced import Base, User, Project, Task, TaskAttachment

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), '..', 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx', 'txt', 'zip'}

CORS(app)

# Create uploads folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database setup
DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'database_production.db')
engine = create_engine(f'sqlite:///{DATABASE_PATH}', echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Create default users if database is empty
def init_default_users():
    """Create CEO and team member accounts"""
    db_session = Session()
    try:
        if db_session.query(User).count() == 0:
            # Create CEO account
            ceo = User(
                username='ceo',
                email='ceo@company.com',
                full_name='CEO Admin',
                role='ceo',
                is_active=True
            )
            ceo.set_password('ceo123')
            
            # Create team member account
            team1 = User(
                username='john',
                email='john@company.com',
                full_name='John Doe',
                role='team_member',
                is_active=True
            )
            team1.set_password('john123')
            
            team2 = User(
                username='jane',
                email='jane@company.com',
                full_name='Jane Smith',
                role='team_member',
                is_active=True
            )
            team2.set_password('jane123')
            
            db_session.add_all([ceo, team1, team2])
            db_session.commit()
            print("✓ Default users created: ceo/ceo123, john/john123, jane/jane123")
    finally:
        db_session.close()

init_default_users()


# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_current_user():
    """Get current logged in user from session"""
    user_id = session.get('user_id')
    if not user_id:
        return None
    db_session = Session()
    try:
        return db_session.query(User).filter(User.id == user_id).first()
    finally:
        db_session.close()


# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@app.route('/')
def index():
    """Main page - redirect to login or dashboard"""
    if 'user_id' in session:
        return render_template('dashboard.html')
    return render_template('login.html')


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login endpoint"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    
    db_session = Session()
    try:
        user = db_session.query(User).filter(User.username == username).first()
        
        if not user or not user.check_password(password):
            return jsonify({"error": "Invalid credentials"}), 401
        
        if not user.is_active:
            return jsonify({"error": "Account is disabled"}), 403
        
        # Set session
        session['user_id'] = user.id
        session['username'] = user.username
        session['role'] = user.role
        
        return jsonify({
            "success": True,
            "user": user.to_dict()
        }), 200
    
    finally:
        db_session.close()


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Logout endpoint"""
    session.clear()
    return jsonify({"success": True}), 200


@app.route('/api/auth/me', methods=['GET'])
def get_current_user_info():
    """Get current user info"""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not authenticated"}), 401
    return jsonify(user.to_dict()), 200


# ============================================================================
# USER MANAGEMENT (CEO only)
# ============================================================================

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users (for assignment dropdown)"""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not authenticated"}), 401
    
    db_session = Session()
    try:
        users = db_session.query(User).filter(User.is_active == True).all()
        return jsonify([u.to_dict() for u in users]), 200
    finally:
        db_session.close()


@app.route('/api/users', methods=['POST'])
def create_user():
    """Create new user (CEO only)"""
    user = get_current_user()
    if not user or not user.is_ceo():
        return jsonify({"error": "Unauthorized"}), 403
    
    data = request.get_json()
    db_session = Session()
    try:
        new_user = User(
            username=data['username'],
            email=data['email'],
            full_name=data.get('full_name'),
            role=data.get('role', 'team_member')
        )
        new_user.set_password(data['password'])
        
        db_session.add(new_user)
        db_session.commit()
        
        return jsonify(new_user.to_dict()), 201
    
    except Exception as e:
        db_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()


# ============================================================================
# PROJECTS API
# ============================================================================

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """Get all projects (CEO sees all, team members see projects with assigned tasks)"""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not authenticated"}), 401
    
    db_session = Session()
    try:
        if user.is_ceo():
            # CEO sees all projects
            projects = db_session.query(Project).all()
        else:
            # Team member sees projects where they have assigned tasks
            projects = db_session.query(Project).join(Task).filter(
                Task.assigned_to == user.id
            ).distinct().all()
        
        return jsonify([p.to_dict() for p in projects]), 200
    
    finally:
        db_session.close()


@app.route('/api/projects', methods=['POST'])
def create_project():
    """Create new project"""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not authenticated"}), 401
    
    data = request.get_json()
    db_session = Session()
    try:
        project = Project(
            name=data['name'],
            description=data.get('description', ''),
            status=data.get('status', 'active'),
            owner_id=user.id
        )
        
        db_session.add(project)
        db_session.commit()
        
        return jsonify(project.to_dict()), 201
    
    except Exception as e:
        db_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()


@app.route('/api/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    """Update project"""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not authenticated"}), 401
    
    data = request.get_json()
    db_session = Session()
    try:
        project = db_session.query(Project).filter(Project.id == project_id).first()
        
        if not project:
            return jsonify({"error": "Project not found"}), 404
        
        # Only CEO or project owner can update
        if not user.is_ceo() and project.owner_id != user.id:
            return jsonify({"error": "Unauthorized"}), 403
        
        if 'name' in data:
            project.name = data['name']
        if 'description' in data:
            project.description = data['description']
        if 'status' in data:
            project.status = data['status']
        
        project.updated_at = datetime.utcnow()
        db_session.commit()
        
        return jsonify(project.to_dict()), 200
    
    except Exception as e:
        db_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()


@app.route('/api/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    """Delete project (CEO only)"""
    user = get_current_user()
    if not user or not user.is_ceo():
        return jsonify({"error": "Unauthorized"}), 403
    
    db_session = Session()
    try:
        project = db_session.query(Project).filter(Project.id == project_id).first()
        
        if not project:
            return jsonify({"error": "Project not found"}), 404
        
        db_session.delete(project)
        db_session.commit()
        
        return jsonify({"success": True}), 200
    
    except Exception as e:
        db_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()


# ============================================================================
# TASKS API
# ============================================================================

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get tasks with filters and search"""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not authenticated"}), 401
    
    # Get query parameters
    project_id = request.args.get('project_id')
    status = request.args.get('status')
    priority = request.args.get('priority')
    search = request.args.get('search')
    assigned_to = request.args.get('assigned_to')
    
    db_session = Session()
    try:
        query = db_session.query(Task)
        
        # Role-based filtering
        if not user.is_ceo():
            # Team member sees only assigned tasks
            query = query.filter(Task.assigned_to == user.id)
        
        # Apply filters
        if project_id:
            query = query.filter(Task.project_id == int(project_id))
        
        if status:
            query = query.filter(Task.status == status)
        
        if priority:
            query = query.filter(Task.priority == priority)
        
        if assigned_to:
            query = query.filter(Task.assigned_to == int(assigned_to))
        
        # Search in title and description
        if search:
            query = query.filter(
                or_(
                    Task.title.contains(search),
                    Task.description.contains(search)
                )
            )
        
        tasks = query.all()
        return jsonify([t.to_dict(include_assignee=True) for t in tasks]), 200
    
    finally:
        db_session.close()


@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create new task"""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not authenticated"}), 401
    
    data = request.get_json()
    db_session = Session()
    try:
        # Parse due date if provided
        due_date = None
        if data.get('due_date'):
            try:
                due_date = date_parser.parse(data['due_date'])
            except:
                pass
        
        task = Task(
            project_id=data['project_id'],
            title=data['title'],
            description=data.get('description', ''),
            status=data.get('status', 'todo'),
            priority=data.get('priority', 'medium'),
            assigned_to=data.get('assigned_to'),
            due_date=due_date
        )
        
        db_session.add(task)
        db_session.commit()
        
        return jsonify(task.to_dict(include_assignee=True)), 201
    
    except Exception as e:
        db_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update task"""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not authenticated"}), 401
    
    data = request.get_json()
    db_session = Session()
    try:
        task = db_session.query(Task).filter(Task.id == task_id).first()
        
        if not task:
            return jsonify({"error": "Task not found"}), 404
        
        # Check permissions
        if not user.is_ceo() and task.assigned_to != user.id:
            return jsonify({"error": "Unauthorized"}), 403
        
        # Update fields
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'status' in data:
            task.status = data['status']
        if 'priority' in data:
            task.priority = data['priority']
        if 'assigned_to' in data and user.is_ceo():
            task.assigned_to = data['assigned_to']
        if 'due_date' in data:
            try:
                task.due_date = date_parser.parse(data['due_date']) if data['due_date'] else None
            except:
                pass
        
        task.updated_at = datetime.utcnow()
        db_session.commit()
        
        return jsonify(task.to_dict(include_assignee=True)), 200
    
    except Exception as e:
        db_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete task"""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not authenticated"}), 401
    
    db_session = Session()
    try:
        task = db_session.query(Task).filter(Task.id == task_id).first()
        
        if not task:
            return jsonify({"error": "Task not found"}), 404
        
        # Only CEO can delete
        if not user.is_ceo():
            return jsonify({"error": "Unauthorized"}), 403
        
        db_session.delete(task)
        db_session.commit()
        
        return jsonify({"success": True}), 200
    
    except Exception as e:
        db_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()


# ============================================================================
# FILE ATTACHMENTS
# ============================================================================

@app.route('/api/tasks/<int:task_id>/attachments', methods=['POST'])
def upload_attachment(task_id):
    """Upload file attachment to task"""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not authenticated"}), 401
    
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400
    
    db_session = Session()
    try:
        task = db_session.query(Task).filter(Task.id == task_id).first()
        if not task:
            return jsonify({"error": "Task not found"}), 404
        
        # Generate unique filename
        original_filename = secure_filename(file.filename)
        filename = f"{datetime.now().timestamp()}_{original_filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save file
        file.save(filepath)
        file_size = os.path.getsize(filepath)
        
        # Create attachment record
        attachment = TaskAttachment(
            task_id=task_id,
            filename=filename,
            original_filename=original_filename,
            file_path=filepath,
            file_size=file_size,
            uploaded_by=user.id
        )
        
        db_session.add(attachment)
        db_session.commit()
        
        return jsonify(attachment.to_dict()), 201
    
    except Exception as e:
        db_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()


@app.route('/api/tasks/<int:task_id>/attachments', methods=['GET'])
def get_attachments(task_id):
    """Get all attachments for a task"""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not authenticated"}), 401
    
    db_session = Session()
    try:
        attachments = db_session.query(TaskAttachment).filter(
            TaskAttachment.task_id == task_id
        ).all()
        
        return jsonify([a.to_dict() for a in attachments]), 200
    
    finally:
        db_session.close()


@app.route('/api/attachments/<int:attachment_id>/download', methods=['GET'])
def download_attachment(attachment_id):
    """Download file attachment"""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not authenticated"}), 401
    
    db_session = Session()
    try:
        attachment = db_session.query(TaskAttachment).filter(
            TaskAttachment.id == attachment_id
        ).first()
        
        if not attachment:
            return jsonify({"error": "Attachment not found"}), 404
        
        return send_from_directory(
            app.config['UPLOAD_FOLDER'],
            attachment.filename,
            as_attachment=True,
            download_name=attachment.original_filename
        )
    
    finally:
        db_session.close()


# ============================================================================
# DASHBOARD & STATISTICS
# ============================================================================

@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics"""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not authenticated"}), 401
    
    db_session = Session()
    try:
        if user.is_ceo():
            # CEO sees all stats
            total_projects = db_session.query(Project).count()
            total_tasks = db_session.query(Task).count()
            
            # Tasks by status
            todo_count = db_session.query(Task).filter(Task.status == 'todo').count()
            in_progress_count = db_session.query(Task).filter(Task.status == 'in_progress').count()
            done_count = db_session.query(Task).filter(Task.status == 'done').count()
            
            # Tasks by priority
            high_priority = db_session.query(Task).filter(Task.priority == 'high').count()
            
            # Overdue tasks
            overdue_tasks = db_session.query(Task).filter(
                Task.due_date < datetime.utcnow(),
                Task.status != 'done'
            ).count()
            
            # Team stats
            total_team_members = db_session.query(User).filter(User.role == 'team_member').count()
            
        else:
            # Team member sees only their stats
            total_projects = db_session.query(Project).join(Task).filter(
                Task.assigned_to == user.id
            ).distinct().count()
            
            total_tasks = db_session.query(Task).filter(Task.assigned_to == user.id).count()
            
            todo_count = db_session.query(Task).filter(
                Task.assigned_to == user.id,
                Task.status == 'todo'
            ).count()
            
            in_progress_count = db_session.query(Task).filter(
                Task.assigned_to == user.id,
                Task.status == 'in_progress'
            ).count()
            
            done_count = db_session.query(Task).filter(
                Task.assigned_to == user.id,
                Task.status == 'done'
            ).count()
            
            high_priority = db_session.query(Task).filter(
                Task.assigned_to == user.id,
                Task.priority == 'high'
            ).count()
            
            overdue_tasks = db_session.query(Task).filter(
                Task.assigned_to == user.id,
                Task.due_date < datetime.utcnow(),
                Task.status != 'done'
            ).count()
            
            total_team_members = 0
        
        return jsonify({
            "total_projects": total_projects,
            "total_tasks": total_tasks,
            "todo_count": todo_count,
            "in_progress_count": in_progress_count,
            "done_count": done_count,
            "high_priority_count": high_priority,
            "overdue_count": overdue_tasks,
            "total_team_members": total_team_members,
            "role": user.role
        }), 200
    
    finally:
        db_session.close()


@app.route('/api/calendar/tasks', methods=['GET'])
def get_calendar_tasks():
    """Get tasks with due dates for calendar view"""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not authenticated"}), 401
    
    # Get date range from query params
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    
    db_session = Session()
    try:
        query = db_session.query(Task).filter(Task.due_date.isnot(None))
        
        # Role-based filtering
        if not user.is_ceo():
            query = query.filter(Task.assigned_to == user.id)
        
        # Date range filter
        if start_date:
            query = query.filter(Task.due_date >= date_parser.parse(start_date))
        if end_date:
            query = query.filter(Task.due_date <= date_parser.parse(end_date))
        
        tasks = query.all()
        
        # Format for calendar
        events = []
        for task in tasks:
            events.append({
                "id": task.id,
                "title": task.title,
                "start": task.due_date.isoformat(),
                "color": {
                    "high": "#f56565",
                    "medium": "#ed8936",
                    "low": "#48bb78"
                }.get(task.priority, "#667eea"),
                "extendedProps": task.to_dict(include_assignee=True)
            })
        
        return jsonify(events), 200
    
    finally:
        db_session.close()


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 PRODUCTION PROJECT MANAGEMENT SYSTEM")
    print("=" * 60)
    print("\n📝 Default Accounts:")
    print("   CEO:          username: ceo,  password: ceo123")
    print("   Team Member:  username: john, password: john123")
    print("   Team Member:  username: jane, password: jane123")
    print("\n🌐 Server: http://localhost:5001")
    print("=" * 60)
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5002)
