# -*- coding: utf-8 -*-
"""
Файл setup.py для Lab6 - Flask REST API та Kanban Board.
"""

from setuptools import setup, find_packages

setup(
    name="project_manager_lab6",
    version="6.0.0",
    description="Система керування проектами - Lab6 (Flask REST API + Kanban Board)",
    author="Student",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "Flask>=3.0.0",
        "Flask-CORS>=4.0.0",
        "SQLAlchemy>=2.0.0",
        "Flask-SQLAlchemy>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
)
