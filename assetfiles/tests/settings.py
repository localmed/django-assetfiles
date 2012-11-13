from os import path

PROJECT_ROOT = path.abspath(path.join(path.dirname(__file__), 'project'))

TEST_RUNNER = 'discover_runner.DiscoverRunner'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = (
    'assetfiles',
    'assetfiles.tests.apps.app-1',
    'assetfiles.tests.apps.app-2',
)

ROOT_URLCONF = 'assetfiles.tests.urls'

STATIC_ROOT = path.join(PROJECT_ROOT, 'public')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    path.join(PROJECT_ROOT, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_DIRS = (
    path.join(PROJECT_ROOT, 'templates'),
)
