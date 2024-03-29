from pathlib import Path
import os
import environ 
from dotenv import load_dotenv
import dj_database_url


load_dotenv()
env = environ.Env()
environ.Env.read_env()

ENVIRONMENT = env

#para una vaariable de entorno en windows solo se puede marcar el camino no un comando
# NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"

NODE_ENV='production tailwindcss --postcss -i ./src/styles.css -o ../static/css/dist/styles.css --minify'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-k)my4t*zx^!bc6seaeja79v*b(uelj!f#7+5)+9y%&p$shn2&+'


ALLOWED_HOSTS = [
    #Acceder a cualquier sitio con el url de la app
    '*',    
]

RENDER_EXTERNAL_HOSTSNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTSNAME:  
     ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTSNAME) 
# Application definition

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'





INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'social',
    'tailwind',
    'compressor',
    'theme',
    'bootstrap4',
    'django_browser_reload',
    'django.contrib.sites',
    #las fechas se veran en vez de 2022-01-01 12:00:00 a 56 minutos atras
    'django.contrib.humanize',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    #para que se pueda logear con google
    'allauth.socialaccount.providers.google',
    'crispy_forms',
    "crispy_tailwind",
    'accounts',

]

SITE_ID = 1
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
TAILWIND_APP_NAME = 'theme'

CRISPY_TEMPLATE_PACK = 'tailwind'
# CRISPY_TEMPLATE_PACK = 'bootstrap4'
NTERNAL_IPS =[
    "127.0.0.1",
]

# ================ ALLAUTH ==================== #
AUTHORIZED_EMAILS = env.list("AUTHORIZED_EMAILS")
AUTHORIZED_PASSWORDS = env.list("AUTHORIZED_PASSWORDS")
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_UNIQUE = True
AUTH_USER_MODEL="accounts.User"
#nos redirige a la pagina de login si no estamos logeados
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 3
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT =300
#nos dirige a la pagina de inicio una vez se logea
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "account_login"



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    #render
    "whitenoise.middleware.WhiteNoiseMiddleware",


]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

#si no se coloca el backends no se podra logear con el correo y dara error
AUTHENTICATION_BACKENDS = [
    
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
    
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": env.db("DATABASE_URL", default="postgres:///social"),
}
# DATABASES["default"]["ATOMIC_REQUESTS"] = True
DATABASES["default"]=dj_database_url.parse("postgres://admin:K5TIOnSc8twIxQw8Vw86ogQtuCw3SHlL@dpg-cnffd0qcn0vc73e7i8qg-a.oregon-postgres.render.com/social_suqs")

PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
    "django.contrib.auth.hashers.SHA1PasswordHasher",

]

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

#render
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

MEDIA_URL = 'media/'
#render
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATIC_ROOT = os.path.join(BASE_DIR, 'templates')
STATIC_TMP= os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media') 

COMPRESS_ENABLED = False

STATICFILES_FINDERS = (
    # 'compressor.finders.CompressorFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',)


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
#Confirmacion Correo Consola
# EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'

#Confirmacion Correo Gmail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = 'hcffkznmzajwdsna'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = [
    
     'wwww.acm5pts.com',
    'acm5pts.com',

]
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 3600
ACCOUNT_RATE_LIMITS = {
    'login_failed': {
        'LIMIT': 5,  # Número máximo de intentos de inicio de sesión fallidos permitidos
        'WINDOW': 3600,  # Ventana de tiempo (en segundos) para el límite de intentos de inicio de sesión fallidos
    }
}

RENDER_EXTERNAL_HOSTSNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTSNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTSNAME)


if not DEBUG:
    EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'redsocialconfirmacion@gmail.com'
    EMAIL_HOST_USER = env('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 415300
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    PUBLIC_MEDIA_LOCATION = 'media'
    # DEFAULT_FILE_STORAGE = 'core.storage_backends.MediaStore'

    STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
