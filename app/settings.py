import os
import environ
from pathlib import Path

# Configuración para manejar las variables de entorno
env = environ.Env()
environ.Env.read_env()  # Carga el archivo .env

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración de la clave secreta y debug a través del .env
SECRET_KEY = env('SECRET_KEY', default='unsafe-secret-key')
DEBUG = env('DEBUG', default=False)

# Configuración de los hosts permitidos
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',  # Tu aplicación principal
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de URL root
ROOT_URLCONF = 'app.urls'

# Configuración de templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'app/templates'],
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

WSGI_APPLICATION = 'app.wsgi.application'

# Redirección después de logout
LOGOUT_REDIRECT_URL = '/'

# Configuración de la base de datos
DATABASES = {
     'default': env.db(),
}

# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Configuración de internacionalización
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Usar WhiteNoise para servir archivos estáticos
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = [BASE_DIR / 'app/static']

# Configuración del campo primario por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración del backend de correo
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Configuración de sesiones
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
