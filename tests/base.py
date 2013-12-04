import os
import shutil
import tempfile

import django
from django.conf import settings
from django.contrib.staticfiles import finders, storage
from django.test import TestCase
from django.utils import six
from django.utils.functional import empty

from assetfiles import assets, filters
import assetfiles.settings


def filter(path):
    asset_path, filter = assets.find(path)
    return filter.filter(asset_path).strip()


def is_at_least_django_15():
    return django.VERSION[0] >= 1 and django.VERSION[1] >= 5


def is_glob2_available():
    try:
        import glob2
        return True
    except ImportError:
        return False


class AssetfilesTestCase(TestCase):

    def setUp(self):
        # Clear the cached staticfiles_storage out, this is because when it first
        # gets accessed (by some other test), it evaluates settings.STATIC_ROOT,
        # since we're planning on changing that we need to clear out the cache.
        storage.staticfiles_storage._wrapped = empty
        # Clear the cached staticfile finders, so they are reinitialized every
        # run and pick up changes in settings.STATICFILES_DIRS.
        finders._finders.clear()
        # Clear the cached assetfile filters, so they are reinitialized every
        # run and pick up changes in settings.ASSETFILES_FILTERS.
        filters._filters.clear()

        if not os.path.exists(settings.PROJECT_ROOT):
            shutil.copytree(
                os.path.join(settings.TESTS_ROOT, 'project-template'),
                settings.PROJECT_ROOT
            )
        self.addCleanup(shutil.rmtree, settings.PROJECT_ROOT, ignore_errors=True)
        self.root = settings.PROJECT_ROOT

    def mkfile(self, path, content=None):
        abspath = os.path.join(self.root, path)
        dirname = os.path.dirname(abspath)

        if not os.path.isdir(dirname):
            os.makedirs(dirname)

        with open(abspath, 'w') as file:
            if content:
                if not six.PY3:
                    content = content.encode('utf-8')
                file.write(content)

        return abspath
