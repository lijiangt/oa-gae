import os;

DEBUG = False
TEMPLATE_DEBUG = DEBUG


MEDIA_ROOT = ''
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/s'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".


CONTEXT_PATH=''
#print PROJECT_ROOT
#print PROJECT_ROOT
ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'appengine'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
#TIME_ZONE = 'America/Chicago'
TIME_ZONE = 'UTC'

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

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
#    'django.contrib.sessions.middleware.SessionMiddleware',
###    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'django.middleware.doc.XViewMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
        "django.core.context_processors.auth",
        "django.core.context_processors.i18n",
        "django.core.context_processors.request",
        'commons.context_processors.header',
        'commons.context_processors.custom_setting',
)
if DEBUG:
    TEMPLATE_CONTEXT_PROCESSORS += ("django.core.context_processors.debug",)
    

#if DEBUG:
#    MIDDLEWARE_CLASSES += ('commons.middleware.SqlPrintingMiddleware',)


ROOT_URLCONF = 'urls'

ROOT_PATH = os.path.dirname(__file__)
TEMPLATE_DIRS = (
    os.path.join(ROOT_PATH, 'templates')
)


INSTALLED_APPS = (
     'appengine_django',
     'django.contrib.auth',                  
#    'django.contrib.contenttypes',
#    'django.contrib.sessions',
#    'django.contrib.sites',
    'commons',
    'root',
    'work_note',
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
LOGOUT_URL = CONTEXT_PATH+'/accounts/logout'
LOGIN_REDIRECT_URL=CONTEXT_PATH+'/'
LOGOUT_REDIRECT_URL=CONTEXT_PATH+'/'

gettext_noop = lambda s: s

LANGUAGES=(
           ('zh-cn',gettext_noop('Chinese')),
           ('en',gettext_noop('English')),
)

DEFAUTL_PAGE_SIZE = 20
DEFAULT_THEME = 'default'

SITE_NAME='Work Notebook'
MODULE_LIST_HTML = 'module_list.html'
BOTTOM_INCLUDE_HTML = 'bottom_include.html'

FORCE_DOMAIN_VISIT='oa.lijiangt.cn'
