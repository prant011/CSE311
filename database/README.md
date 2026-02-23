# Database Schema and Setup

This directory contains the MySQL database schema and setup files for the Library Management System.

## Files

- `library_management_schema.sql` - Complete database schema export containing all tables, indexes, and relationships

## Database Structure

The database consists of the following main tables:

### Django System Tables
- `django_*` - Django framework tables (migrations, sessions, admin log, etc.)
- `auth_*` - Django authentication system tables (users, groups, permissions)

### Library Application Tables
- `library_admin` - Admin users
- `library_student` - Student users
- `library_author` - Book authors
- `library_book` - Book catalog
- `library_issuerequest` - Book borrowing requests/issues
- `library_fine` - Fine records for overdue books
- `library_notification` - User notifications

## Setup Instructions

### 1. Create Database
```sql
CREATE DATABASE library_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Import Schema
```bash
mysql -u root -p library_management < database/library_management_schema.sql
```

### 3. Configure Environment
Update your `.env` file with database credentials:
```
DB_NAME=library_management
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

### 4. Run Django Migrations
```bash
python manage.py migrate
```

## Database Export

To export the database schema yourself:
```bash
python manage.py export_schema
```

This will generate a fresh `database/library_management_schema.sql` file with the current database structure.

## Notes

- The schema includes all table structures, indexes, and foreign key relationships
- Default data is not included in the schema export
- The export uses MySQL-specific syntax and features
- All tables use InnoDB engine with utf8mb4 character set for Unicode support
