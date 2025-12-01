# 📚 Library Management System

A comprehensive library management system with bKash payment integration.

## ✨ Features

### For Everyone:
- View all books on homepage
- Search by title, author, category
- Sort books alphabetically
- NSU-style modern interface

### For Students:
- Signup/Login with validation
- Request books
- View issues (requested, issued, returned)
- Check fines and payment history
- Pay fines online with bKash

### For Admin:
- Complete dashboard with statistics
- Manage books and authors
- Manage students by department
- Accept/reject issue requests
- Process returns with automatic fine calculation
- Manage fines
- Change user passwords

## 🚀 Installation

### Prerequisites:
- Python 3.8+
- MySQL Server
- bKash Merchant Account (for payment)

### Steps:

1. **Clone/Download Project**
```bash
git clone <repository-url>
cd library_management_system
```

2. **Create Virtual Environment**
```bash
python -m venv venv
# Activate:
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup MySQL Database**
```sql
CREATE DATABASE library_management;
-- Run all table creation queries
```

5. **Configure Environment**
```bash
# Copy .env.example to .env
# Update with your credentials
```

6. **Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Create Superuser**
```bash
python manage.py createsuperuser
```

8. **Run Server**
```bash
python manage.py runserver
```

9. **Access Application**
- Main: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## 📱 URLs

| Page | URL |
|------|-----|
| Home | / |
| Login | /login/ |
| Signup | /signup/ |
| Student Dashboard | /student/dashboard/ |
| Student Issues | /student/issues/ |
| Student Fines | /student/fines/ |
| Admin Dashboard | /admin/dashboard/ |
| Manage Books | /admin/books/ |
| Manage Students | /admin/students/ |
| Manage Fines | /admin/fines/ |

## 🔧 Configuration

### bKash Setup:
1. Register at https://developer.bka.sh/
2. Create an app
3. Get credentials (App Key, Secret, Username, Password)
4. Add to .env file

### Database:
- Default: MySQL
- Database name: library_management
- Update credentials in .env

## 📊 Database Schema

- **Author** - Author information
- **Book** - Books with author relationship
- **Student** - Student profiles (linked to User)
- **IssueRequest** - Borrowing requests
- **Fine** - Fine records with bKash integration

## 👨‍💻 Developer

**Farhin Ahmed Pranto**
- ID: 2312734
- Section: 09

## 📄 License

This project is created for academic purposes.

## 🆘 Support

For issues or questions, contact: farhinahmed71@gmail.com