# Sarbottam Cement Limited - Company Profile Website

A comprehensive Django-based web application showcasing the company profile of Sarbottam Cement Limited (SARBTM), a leading cement manufacturer in Nepal.

## 🏢 About Sarbottam Cement Limited

Sarbottam Cement Limited is an innovator and pioneer of the cement industry of Nepal, being the first and only cement manufacturer to use a completely European production line. The company is publicly listed on the Nepal Stock Exchange (NEPSE) under the symbol SARBTM.

### Key Features:
- **Company Profile**: Comprehensive information about the company
- **News Section**: Latest news and announcements
- **Financial Data**: Stock market information and financial reports
- **Achievements**: Company milestones and recognitions
- **Responsive Design**: Modern, mobile-friendly interface with Tailwind CSS

## 🛠 Technology Stack

- **Backend**: Django 4.2+ (Python)
- **Database**: MySQL
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Icons**: Font Awesome
- **Environment**: Python 3.10+

## 📋 Database Schema

The application includes four main models:

### 1. Company Model
- Basic company information (name, symbol, sector)
- Contact details and location
- Financial information (market price, P/E ratio, etc.)
- Stock information and parent group details

### 2. CompanyNews Model
Fields: `news_title`, `news_date`, `news_image`, `news_body`
- News articles with featured status
- SEO-friendly slugs and meta descriptions
- Author and source attribution

### 3. CompanyFinancial Model
- Quarterly and annual financial data
- Revenue, profit, EPS tracking
- Fiscal year organization

### 4. CompanyAchievement Model
- Company achievements and milestones
- Categorized by type (awards, certifications, etc.)
- Date-based organization

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- MySQL Server
- Git

### 1. Clone the Repository
```bash
git clone <repository-url>
cd "Python Taskk"
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup

#### Option A: Using Django Migrations (Recommended)
1. Update database settings in `secret.py`:
```python
DATABASE_CONFIG = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sarbottam_cement_db',
        'USER': 'your_mysql_username',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

2. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

#### Option B: Using SQL Script
1. Create MySQL database:
```bash
mysql -u root -p < database_setup.sql
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Collect Static Files
```bash
python manage.py collectstatic
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Visit `http://localhost:8000` to view the application.

## 📁 Project Structure

```
Python Taskk/
├── cement_profile_app/          # Main Django project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── sarbottam/                   # Main application
│   ├── models.py               # Database models
│   ├── views.py                # View logic
│   ├── urls.py                 # URL patterns
│   ├── admin.py                # Admin configuration
│   └── migrations/
├── templates/                   # HTML templates
│   ├── base.html               # Base template
│   └── sarbottam/
│       ├── company_profile.html
│       ├── news_list.html
│       └── error.html
├── static/                      # Static files
│   ├── css/
│   ├── js/
│   └── images/
├── media/                       # User uploads
├── requirements.txt            # Python dependencies
├── database_setup.sql          # MySQL schema
├── secret.py                   # Configuration file
└── README.md
```

## 🌐 URLs and Navigation

- `/` - Company Profile (Homepage)
- `/news/` - News Listing
- `/news/<slug>/` - Individual News Detail
- `/financial/` - Financial Data
- `/achievements/` - Company Achievements
- `/admin/` - Django Admin Panel
- `/api/company/` - Company Data API
- `/api/news/` - Latest News API

## 💾 Sample Data

The application includes sample data for Sarbottam Cement Limited:

### Company Information
- **Name**: Sarbottam Cement Limited
- **Symbol**: SARBTM
- **Sector**: Manufacturing and Processing
- **Headquarters**: Sunwal, Nawalparasi, State-5, Nepal
- **Parent Group**: Saurabh Group

### Sample News Articles
1. Strong Q4 Performance Report
2. New CSR Initiative Launch
3. ARCHBUILD EXPO 2024 Participation
4. Career Opportunities Announcement

### Sample Achievements
1. First European Production Line in Nepal
2. ICRANP-IR BBB+ Rating
3. Successful IPO Launch

## 🔧 Configuration

### Environment Variables (secret.py)
```python
SECRET_KEY = 'your-secret-key'
DEBUG = True  # Set to False in production
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASE_CONFIG = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sarbottam_cement_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kathmandu'
```

## 📱 Features

### Company Profile
- Hero section with company overview
- Detailed company information
- Stock market data display
- Industry leadership highlights

### News Management
- Featured news system
- Search functionality
- Pagination support
- Responsive news cards

### Admin Panel
- Full CRUD operations for all models
- Rich admin interface
- Image upload support
- Bulk operations

### Responsive Design
- Mobile-first approach
- Tailwind CSS framework
- Modern card-based layout
- Smooth animations and transitions

## 🔐 Security Features

- CSRF protection
- SQL injection prevention
- XSS protection
- Secure file uploads
- Environment-based configuration

## 🌍 Production Deployment

### Environment Setup
1. Set `DEBUG = False` in settings
2. Configure proper `ALLOWED_HOSTS`
3. Use environment variables for sensitive data
4. Set up proper MySQL database
5. Configure static file serving
6. Enable HTTPS

### Database Configuration
- Use production MySQL server
- Configure database backups
- Set up proper user permissions
- Enable slow query logging

## 📊 API Endpoints

### Company Data API
```
GET /api/company/
Response: JSON with company information
```

### Latest News API
```
GET /api/news/
Response: JSON with latest news articles
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is created for educational and demonstration purposes.

## 📞 Support

For questions or support regarding this application, please refer to the documentation or create an issue in the repository.

---

**Note**: This application was created to demonstrate a modern Django web application with MySQL database integration, showcasing real company data from Nepal's stock market websites including nepalstock.com, sharesansar.com, and merolagani.com.
