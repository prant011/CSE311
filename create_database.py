#!/usr/bin/env python
"""
Create SQLite database with all required tables for Library Management System
"""
import os
import sqlite3
from pathlib import Path

# Get the database path
BASE_DIR = Path(__file__).resolve().parent
db_path = BASE_DIR / 'db.sqlite3'

# Remove existing database if it exists
if db_path.exists():
    os.remove(db_path)
    print(f"Removed existing database: {db_path}")

# Create new database connection
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

print("Creating SQLite database tables...")

# Create Django's built-in tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS django_migrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    app VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    applied DATETIME NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS django_content_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    UNIQUE(app_label, model)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS auth_permission (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    content_type_id INTEGER NOT NULL REFERENCES django_content_type(id),
    codename VARCHAR(100) NOT NULL,
    UNIQUE(content_type_id, codename)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS auth_group (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(150) NOT NULL UNIQUE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS auth_group_permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id INTEGER NOT NULL REFERENCES auth_group(id),
    permission_id INTEGER NOT NULL REFERENCES auth_permission(id),
    UNIQUE(group_id, permission_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS auth_user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME,
    is_superuser BOOL NOT NULL,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    is_staff BOOL NOT NULL,
    is_active BOOL NOT NULL,
    date_joined DATETIME NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS auth_user_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES auth_user(id),
    group_id INTEGER NOT NULL REFERENCES auth_group(id),
    UNIQUE(user_id, group_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS auth_user_user_permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES auth_user(id),
    permission_id INTEGER NOT NULL REFERENCES auth_permission(id),
    UNIQUE(user_id, permission_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS django_session (
    session_key VARCHAR(40) NOT NULL PRIMARY KEY,
    session_data TEXT NOT NULL,
    expire_date DATETIME NOT NULL
)
''')

# Create library_author table
cursor.execute('''
CREATE TABLE IF NOT EXISTS library_author (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    bio TEXT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
)
''')

# Create library_book table
cursor.execute('''
CREATE TABLE IF NOT EXISTS library_book (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(300) NOT NULL,
    author_id INTEGER NOT NULL REFERENCES library_author(id),
    isbn VARCHAR(20) UNIQUE,
    category VARCHAR(100),
    quantity INTEGER NOT NULL DEFAULT 1,
    available INTEGER NOT NULL DEFAULT 1,
    cover_image VARCHAR(200),
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
)
''')

# Create library_student table
cursor.execute('''
CREATE TABLE IF NOT EXISTS library_student (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    department VARCHAR(100) NOT NULL,
    student_id VARCHAR(50) NOT NULL UNIQUE,
    phone VARCHAR(20),
    status VARCHAR(20) DEFAULT 'active',
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
)
''')

# Create library_issuerequest table
cursor.execute('''
CREATE TABLE IF NOT EXISTS library_issuerequest (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL REFERENCES library_student(id),
    book_id INTEGER NOT NULL REFERENCES library_book(id),
    status VARCHAR(20) DEFAULT 'requested',
    issue_date DATE,
    return_date DATE,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
)
''')

# Create library_fine table
cursor.execute('''
CREATE TABLE IF NOT EXISTS library_fine (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    issue_id INTEGER NOT NULL REFERENCES library_issuerequest(id),
    amount DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    status VARCHAR(20) DEFAULT 'unpaid',
    payment_date DATETIME,
    bkash_trxid VARCHAR(100),
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
)
''')

# Create library_notification table
cursor.execute('''
CREATE TABLE IF NOT EXISTS library_notification (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER REFERENCES library_student(id),
    message TEXT NOT NULL,
    is_read BOOL DEFAULT FALSE,
    created_at DATETIME NOT NULL
)
''')

# Create library_admin table
cursor.execute('''
CREATE TABLE IF NOT EXISTS library_admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
    email VARCHAR(254) NOT NULL,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    is_active BOOL DEFAULT TRUE,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
)
''')

# Insert sample data
print("Inserting sample data...")

# Insert sample authors
authors_data = [
    ('J.K. Rowling', 'British author, best known for Harry Potter series'),
    ('Stephen King', 'American author of horror, supernatural fiction, suspense, and fantasy novels'),
    ('Agatha Christie', 'English writer known for her detective novels and short story collections'),
    ('George Orwell', 'English novelist and essayist, journalist and critic'),
    ('Jane Austen', 'English novelist known primarily for her social commentary')
]

cursor.executemany('''
INSERT INTO library_author (name, bio, created_at, updated_at) 
VALUES (?, ?, datetime('now'), datetime('now'))
''', authors_data)

# Insert sample books
books_data = [
    ('Harry Potter and the Sorcerer\'s Stone', 1, '978-0439708180', 'Fantasy', 5, 5),
    ('Harry Potter and the Chamber of Secrets', 1, '978-0439064866', 'Fantasy', 3, 3),
    ('The Shining', 2, '978-0307743657', 'Horror', 2, 2),
    ('It', 2, '978-1501142970', 'Horror', 4, 4),
    ('Murder on the Orient Express', 3, '978-0007119318', 'Mystery', 3, 3),
    ('And Then There Were None', 3, '978-0007122783', 'Mystery', 2, 2),
    ('1984', 4, '978-0451524935', 'Dystopian', 6, 6),
    ('Animal Farm', 4, '978-0451526342', 'Political Satire', 4, 4),
    ('Pride and Prejudice', 5, '978-0141439518', 'Romance', 3, 3),
    ('Sense and Sensibility', 5, '978-0141439662', 'Romance', 2, 2)
]

cursor.executemany('''
INSERT INTO library_book (title, author_id, isbn, category, quantity, available, created_at, updated_at) 
VALUES (?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
''', books_data)

# Insert sample admin
cursor.execute('''
INSERT INTO library_admin (username, password, email, first_name, last_name, created_at, updated_at) 
VALUES (?, ?, ?, ?, ?, datetime('now'), datetime('now'))
''', ('admin', 'pbkdf2_sha256$600000$hashed_password_here', 'admin@library.com', 'Admin', 'User'))

# Insert sample student
cursor.execute('''
INSERT INTO library_student (department, student_id, phone, status, created_at, updated_at) 
VALUES (?, ?, ?, ?, datetime('now'), datetime('now'))
''', ('Computer Science', 'CS2024001', '+8801234567890', 'active'))

# Commit changes and close connection
conn.commit()
conn.close()

print(f"✅ SQLite database created successfully at: {db_path}")
print("📚 Sample data inserted:")
print("   - 5 authors")
print("   - 10 books") 
print("   - 1 admin user")
print("   - 1 student")
print("\n🚀 Your library management system is ready!")
