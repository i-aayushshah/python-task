# Secret configuration for Django project
SECRET_KEY = 'django-insecure-change-this-secret-key-in-production-5#$%^&*()_+'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']

# Database Configuration
DATABASE_CONFIG = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sarbottam_cement_db',
        'USER': 'root',
        'PASSWORD': 'Shah.123',  # Change this to your MySQL password
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

# Other settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kathmandu'
