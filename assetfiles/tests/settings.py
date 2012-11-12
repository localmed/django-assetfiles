from os import path

TESTS_ROOT = path.abspath(path.dirname(__file__))

TEST_RUNNER = 'discover_runner.DiscoverRunner'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = (
    'assetfiles',
    'assetfiles.tests.app',
)

ROOT_URLCONF = 'assetfiles.tests.urls'

STATIC_ROOT = path.join(TESTS_ROOT, 'public')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    path.join(TESTS_ROOT, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_DIRS = (
    path.join(TESTS_ROOT, 'templates'),
)
