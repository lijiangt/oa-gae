# Django settings for oa project.
import os;

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_ROOT = os.path.dirname(__file__)
#PROJECT_ROOT='/home/lijt/workspace-core/oa'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT ='%s/s' % PROJECT_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/s'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/s_admin/'


CONTEXT_PATH=''
#print PROJECT_ROOT
#print PROJECT_ROOT
ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'oa_django'             # Or path to database file if using sqlite3.
DATABASE_USER = 'root'             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
#TIME_ZONE = 'America/Chicago'
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-cn'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True


APPEND_SLASH=False
# Make this unique, and don't share it with anybody.
SECRET_KEY = 'rriwdv=t(po#-r149=gpg03)%nzc(7z3^si%s4sej(ci7owdj!'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
        "django.core.context_processors.auth",
        "django.core.context_processors.i18n",
        "django.core.context_processors.request",
        'oa.commons.context_processors.header',
        'oa.commons.context_processors.custom_setting',
)
if DEBUG:
    TEMPLATE_CONTEXT_PROCESSORS += ("django.core.context_processors.debug",)
    
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)
if DEBUG:
    MIDDLEWARE_CLASSES += ('oa.commons.middleware.SqlPrintingMiddleware',)


ROOT_URLCONF = 'oa.urls'

TEMPLATE_DIRS = (
 #   '%s/templates' % PROJECT_ROOT,
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'oa',
    'oa.work_note',
    'oa.site_improve',
)

DATE_FORMAT='%Y-%m-%d'
DATETIME_FORMAT='%Y-%m-%d %H:%M:%S'
TIME_FORMAT='%H:%M:%S'
DEFAULT_FROM_EMAIL='admin@bupticet.com'
EMAIL_HOST='localhost'
EMAIL_HOST_PASSWORD=''
EMAIL_HOST_USER=''

EXTEND_HTTP_METHOD='__http_method'
LOGIN_URL = CONTEXT_PATH+'/accounts/login'
LOGIN_REDIRECT_URL=CONTEXT_PATH+'/'
LOGOUT_REDIRECT_URL=CONTEXT_PATH+'/'

gettext_noop = lambda s: s

LANGUAGES=(
           ('zh-cn',gettext_noop('Chinese')),
           ('en',gettext_noop('English')),
)

DEFAUTL_PAGE_SIZE = 20
DEFAULT_THEME = 'default'