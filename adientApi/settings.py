import os
from datetime import  timedelta
import datetime
from app.helper.config.ConfigsDatabase import ConfigsDatabase

# project base folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(__file__)

SECRET_KEY = '+cpms8jch^4oi&m4@!rd@dooz46r9tqlbc9e-1m^ykb(0vt!(1'

DEBUG = True

ALLOWED_HOSTS = ['*']

MEDIA_URL =  '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# allow client into server
CORS_ORIGIN_ALLOW_ALL = True


INSTALLED_APPS = [
    'accounts',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djoser',
    'events',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    # part master
    'order.apps.OrderConfig',
    # master data
    'master_data.apps.MasterDataConfig',
    # truck plan management 
    'truck_plan_management.apps.TruckPlanManagementConfig',
    # pdf html5lib
    'pdf.apps.PdfConfig',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
     # CORS ORIGINE
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'adientApi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'adientApi.wsgi.application'


# Database access
configsDatabase = ConfigsDatabase()
DATABASES = {
    'default': {
        'ENGINE': configsDatabase.configs.get("DB_ENGINE").data,
        'NAME': configsDatabase.configs.get("DB_NAME").data,
        'USER': configsDatabase.configs.get("DB_USER").data,
        'PASSWORD': configsDatabase.configs.get("DB_PASSWORD").data,
        'HOST': configsDatabase.configs.get("DB_HOST").data,
        'PORT': configsDatabase.configs.get("DB_PORT").data,
    }
}



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



STATIC_URL = '/statica/'
STATICFILES_DIRS =(
    os.path.join(BASE_DIR, 'staticas'),
    '/statica',
)

REST_FRAMEWORK = {
    "DATE_INPUT_FORMATS": ["%d-%m-%Y"],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}


JWT_AUTH = {
 
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': False,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=3000),
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
 
}

