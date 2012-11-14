import os

from django.conf import settings
from django.core import management
from django.utils import six

from assetfiles.tests.base import AssetfilesTestCase

def call_command(*args, **kwargs):
    out = six.StringIO()
    kwargs.update({'stdout': out, 'verbosity': 0})
    management.call_command(*args, **kwargs)
    out.seek(0)
    return out

class TestFindStatic(AssetfilesTestCase):
    def test_find_file(self):
        out = call_command('findstatic', 'css/static.css', all=False)
        lines = out.readlines()[1:]
        self.assertEquals(len(lines), 1)
        self.assertIn('project/static/css/static.css', lines[0])

    def test_find_all_files(self):
        out = call_command('findstatic', 'css/static.css')
        lines = out.readlines()[1:]
        self.assertEquals(len(lines), 3)
        self.assertIn('project/static/css/static.css', lines[0])
        self.assertIn('app-1/static/css/static.css', lines[1])
        self.assertIn('app-2/static/css/static.css', lines[2])

class TestCollectStatic(AssetfilesTestCase):
    def setUp(self):
        super(TestCollectStatic, self).setUp()
        self.root = self.mkdir()
        self.old_root = settings.STATIC_ROOT
        settings.STATIC_ROOT = self.root
        call_command('collectstatic', interactive=False, clear=True)

    def tearDown(self):
        settings.STATIC_ROOT = self.old_root

    def test_copies_static_files(self):
        self.assertStaticFileContains('css/static.css',
            'body { color: red; }')

    def test_returns_app_static_files(self):
        self.assertStaticFileContains('css/app_static.css',
            'body { color: blue; }')

    def test_processes_scss_files(self):
        self.assertStaticFileContains('css/simple.css',
            'body {\n  color: red; }')

    def test_processes_app_scss_files(self):
        self.assertStaticFileContains('css/app.css',
            'body {\n  color: yellow; }')

    def test_processes_scss_files_with_deps(self):
        self.assertStaticFileContains('css/with_deps.css',
            'body {\n  color: black; }')

    def test_processes_scss_files_with_app_deps(self):
        self.assertStaticFileContains('css/with_app_deps.css',
            'body {\n  color: white; }')

    def test_integrates_static_url_with_sass(self):
        self.assertStaticFileContains('css/with_url.css',
            'url("/static/img/bg.jpg")')

    def test_skips_sass_dependencies(self):
        self.assertStaticFileNotFound('css/_dep.css')
        self.assertStaticFileNotFound('css/_dep.scss')

    def assertStaticFileNotFound(self, path):
        static_path = os.path.join(settings.STATIC_ROOT, path)
        self.assertFalse(os.path.isfile(static_path),
            "file '{0}' exists".format(path))

    def assertStaticFileExists(self, path):
        static_path = os.path.join(settings.STATIC_ROOT, path)
        self.assertTrue(os.path.isfile(static_path),
            "file '{0}' does not exist".format(path))

    def assertStaticFileContains(self, path, text):
        static_path = os.path.join(settings.STATIC_ROOT, path)

        self.assertStaticFileExists(path)
        with open(static_path, 'r') as file:
            self.assertIn(text, file.read(),
                "'{0}' not in file '{1}'".format(text, path))
