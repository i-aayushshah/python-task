# Sarbottam Cement Limited - Company Profile System

A Django web application for managing company profile and news for Sarbottam Cement Limited (SARBTM).

## Features

- Company profile management
- News section with CRUD operations
- Responsive design using Tailwind CSS
- MySQL database integration

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Database Setup**
   - Create a MySQL database named `sarbottam_cement_db`
   - Run the MySQL script: `mysql -u your_username -p sarbottam_cement_db < database_setup.sql`

3. **Django Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

4. **Access the Application**
   - Main page: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Technology Stack

- **Backend**: Django 4.2.7
- **Database**: MySQL
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Image Processing**: Pillow

## Project Structure

```
sarbottam_cement/
├── sarbottam_cement/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── company/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
└── static/
```
