# -*- coding: utf-8 -*-
"""
Authentication models - User system with CEO/Team Member roles.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from .models import Base


class User(Base):
    """
    User model for authentication.
    Supports two roles: 'ceo' and 'team_member'.
    """
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)  # In production: use bcrypt hash
    email = Column(String(200), unique=True, nullable=False)
    role = Column(String(50), default='team_member')  # 'ceo' or 'team_member'
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    def check_password(self, password):
        """Simple password check (use bcrypt in production)"""
        return self.password == password


class TaskAssignment(Base):
    """
    Track which team members are assigned to which tasks.
    """
    __tablename__ = 'task_assignments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    assigned_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "task_id": self.task_id,
            "user_id": self.user_id,
            "assigned_at": self.assigned_at.isoformat() if self.assigned_at else None
        }
