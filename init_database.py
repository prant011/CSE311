#!/usr/bin/env python
"""
Initialize database if it doesn't exist
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
db_path = BASE_DIR / 'db.sqlite3'

# Check if database exists and has tables
if not db_path.exists():
    print("Database not found. Creating...")
    exec(open('create_database.py').read())
else:
    # Check if tables exist
    import sqlite3
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='library_book'")
    if not cursor.fetchone():
        print("Database exists but no tables found. Creating...")
        conn.close()
        exec(open('create_database.py').read())
    else:
        print("Database and tables already exist.")
    conn.close()
