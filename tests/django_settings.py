from os import path
import shutil


TESTS_ROOT = path.abspath(path.dirname(__file__))
PROJECT_ROOT = path.join(TESTS_ROOT, 'project')

# We'll use am empty project for each test and create the files we need.
# But, we need actual app directories to have them installed so we copy
# the template beforehand.
if not path.exists(PROJECT_ROOT):
    shutil.copytree(path.join(TESTS_ROOT, 'project-template'), PROJECT_ROOT)

TEST_RUNNER = 'django_nose.run_tests'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = (
    'django_nose',
    'assetfiles',
    'tests.project.app-1',
    'tests.project.app-2',
)

ROOT_URLCONF = 'tests.urls'

STATIC_ROOT = path.join(PROJECT_ROOT, 'public')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    path.join(PROJECT_ROOT, 'static'),
    ('prefix', path.join(PROJECT_ROOT, 'static-prefix'))
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_DIRS = (
    path.join(PROJECT_ROOT, 'templates'),
)

SECRET_KEY = 'ev2pj15ucf^d84l216^@-mv)pl4$^@9g4)9_)7xi@0j0xop94f'
DEFAULT_CHARSET = 'utf-8'
