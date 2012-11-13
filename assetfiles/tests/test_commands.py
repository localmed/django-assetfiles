from django.core.management import call_command
from django.test import TestCase
from django.utils import six

class TestFindStatic(TestCase):
    def test_find_file(self):
        out = six.StringIO()
        call_command('findstatic', 'css/static.css', all=False, verbosity=0, stdout=out)
        out.seek(0)
        lines = [l.strip() for l in out.readlines()][1:]
        self.assertEquals(len(lines), 1)
        self.assertIn('tests/static/css/static.css', lines[0])

    def test_find_all_files(self):
        out = six.StringIO()
        call_command('findstatic', 'css/static.css', verbosity=0, stdout=out)
        out.seek(0)
        lines = [l.strip() for l in out.readlines()][1:]
        self.assertEquals(len(lines), 2)
        self.assertIn('tests/static/css/static.css', lines[0])
        self.assertIn('tests/app/static/css/static.css', lines[1])
