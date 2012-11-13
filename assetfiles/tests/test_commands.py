from os import environ, path
import shutil, tempfile

from django.conf import settings
from django.core import management
from django.test import TestCase
from django.utils import six

def call_command(*args, **kwargs):
    out = six.StringIO()
    kwargs.update({'stdout': out, 'verbosity': 0})
    management.call_command(*args, **kwargs)
    out.seek(0)
    return out

class TestFindStatic(TestCase):
    def test_find_file(self):
        out = call_command('findstatic', 'css/static.css', all=False)
        lines = [l.strip() for l in out.readlines()][1:]
        self.assertEquals(len(lines), 1)
        self.assertIn('project/static/css/static.css', lines[0])

    def test_find_all_files(self):
        out = call_command('findstatic', 'css/static.css')
        lines = [l.strip() for l in out.readlines()][1:]
        self.assertEquals(len(lines), 3)
        self.assertIn('project/static/css/static.css', lines[0])
        self.assertIn('app-1/static/css/static.css', lines[1])
        self.assertIn('app-2/static/css/static.css', lines[2])

class TestCollectStatic(TestCase):
    def setUp(self):
        self.old_root = settings.STATIC_ROOT
        self.root = settings.STATIC_ROOT = tempfile.mkdtemp(dir=settings.TEMP_DIR)
        self.addCleanup(shutil.rmtree, settings.STATIC_ROOT, ignore_errors=True)
        pass

    def tearDown(self):
        settings.STATIC_ROOT = self.old_root
        pass

    def test_copies_static_files(self):
        call_command('collectstatic', interactive=False)
        self.assertTrue(path.exists(path.join(self.root, 'css/static.css')))
