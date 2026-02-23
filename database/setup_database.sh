#!/bin/bash

# Library Management System - Database Setup Script
# This script sets up the MySQL database for the Library Management System

echo "Library Management System - Database Setup"
echo "=========================================="

# Check if MySQL is installed
if ! command -v mysql &> /dev/null; then
    echo "❌ MySQL client is not installed. Please install MySQL first."
    exit 1
fi

# Default database configuration
DB_NAME="library_management"
DB_USER="root"
DB_HOST="localhost"
DB_PORT="3306"

echo "Database Configuration:"
echo "  Name: $DB_NAME"
echo "  Host: $DB_HOST"
echo "  Port: $DB_PORT"

# Get MySQL root password
echo -n "Enter MySQL root password: "
read -s MYSQL_PASSWORD
echo ""

# Test MySQL connection
echo "Testing MySQL connection..."
if ! mysql -u"$DB_USER" -p"$MYSQL_PASSWORD" -h"$DB_HOST" -P"$DB_PORT" -e "SELECT 1;" &> /dev/null; then
    echo "❌ Failed to connect to MySQL. Please check your credentials."
    exit 1
fi

echo "✅ MySQL connection successful"

# Check if database exists
DB_EXISTS=$(mysql -u"$DB_USER" -p"$MYSQL_PASSWORD" -h"$DB_HOST" -P"$DB_PORT" -e "SHOW DATABASES LIKE '$DB_NAME';" | grep "$DB_NAME" | wc -l)

if [ "$DB_EXISTS" -gt 0 ]; then
    echo "⚠️  Database '$DB_NAME' already exists."
    echo -n "Do you want to drop and recreate it? (y/N): "
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo "Dropping existing database..."
        mysql -u"$DB_USER" -p"$MYSQL_PASSWORD" -h"$DB_HOST" -P"$DB_PORT" -e "DROP DATABASE $DB_NAME;"
        echo "Creating new database..."
        mysql -u"$DB_USER" -p"$MYSQL_PASSWORD" -h"$DB_HOST" -P"$DB_PORT" -e "CREATE DATABASE $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    else
        echo "Using existing database..."
    fi
else
    echo "Creating database '$DB_NAME'..."
    mysql -u"$DB_USER" -p"$MYSQL_PASSWORD" -h"$DB_HOST" -P"$DB_PORT" -e "CREATE DATABASE $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
fi

# Import schema
echo "Importing database schema..."
if mysql -u"$DB_USER" -p"$MYSQL_PASSWORD" -h"$DB_HOST" -P"$DB_PORT" "$DB_NAME" < "database/library_management_schema.sql"; then
    echo "✅ Database schema imported successfully"
else
    echo "❌ Failed to import database schema"
    exit 1
fi

echo ""
echo "🎉 Database setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Update your .env file with database credentials:"
echo "   DB_NAME=$DB_NAME"
echo "   DB_USER=$DB_USER"
echo "   DB_PASSWORD=$MYSQL_PASSWORD"
echo "   DB_HOST=$DB_HOST"
echo "   DB_PORT=$DB_PORT"
echo ""
echo "2. Run Django migrations:"
echo "   python manage.py migrate"
echo ""
echo "3. Create a superuser (optional):"
echo "   python manage.py createsuperuser"
echo ""
echo "4. Start the development server:"
echo "   python manage.py runserver"
