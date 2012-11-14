import os, shutil, tempfile

from assetfiles import settings
from assetfiles import filters
from assetfiles.filters.base import BaseFilter
from assetfiles.filters.sass import SassFilter
from assetfiles.tests.base import AssetfilesTestCase, ReplaceFilter, Filter1, Filter2

class TestBaseFilter(AssetfilesTestCase):
    def setUp(self):
        super(TestBaseFilter, self).setUp()
        self.root = self.mkdir()

    def test_filters_a_single_input_file(self):
        filter = ReplaceFilter('Hello', 'World')
        path = self.mkfile('main.css', 'Hello')
        result = filter.filter(path)
        self.assertEquals('World', result)

    def test_matches_input_file_by_ext(self):
        filter = ReplaceFilter()
        path1 = os.path.join(self.root, 'main.foo')
        path2 = os.path.join(self.root, 'main.baz')
        path3 = os.path.join(self.root, 'main.css')
        self.assertTrue(filter.matches_input(path1))
        self.assertTrue(filter.matches_input(path2))
        self.assertFalse(filter.matches_input(path3))

    def test_does_not_match_input_file_without_input_exts(self):
        filter = ReplaceFilter()
        filter.input_exts = ()
        path1 = os.path.join(self.root, 'main.foo')
        path2 = os.path.join(self.root, 'main.baz')
        self.assertFalse(filter.matches_input(path1))
        self.assertFalse(filter.matches_input(path2))

    def test_matches_input_file_by_ext(self):
        filter = ReplaceFilter()
        path1 = os.path.join(self.root, 'main.bar')
        path2 = os.path.join(self.root, 'main.foo')
        self.assertTrue(filter.matches_output(path1))
        self.assertFalse(filter.matches_output(path2))

    def test_does_not_match_output_file_without_output_ext(self):
        filter = ReplaceFilter()
        filter.output_ext = None
        path1 = os.path.join(self.root, 'main.bar')
        self.assertFalse(filter.matches_output(path1))

    def test_returns_possible_input_paths(self):
        filter = ReplaceFilter()
        self.assertEquals(set([
            'dir/main.bar.foo',
            'dir/main.foo',
            'dir/main.bar.baz',
            'dir/main.baz',
        ]), filter.possible_input_paths('dir/main.bar'))

    def test_returns_output_path(self):
        filter = ReplaceFilter()
        self.assertEquals('dir/main.bar', filter.output_path('dir/main.bar.foo'))
        self.assertEquals('dir/main.bar', filter.output_path('dir/main.foo'))

class TestFilters(AssetfilesTestCase):
    def setUp(self):
        super(TestFilters, self).setUp()
        self.old_filters = settings.FILTERS
        settings.FILTERS = (
            'assetfiles.tests.base.Filter1',
            'assetfiles.tests.base.Filter2',
        )

    def tearDown(self):
        settings.FILTERS = self.old_filters

    def test_filter_from_path(self):
        self.assertIsInstance(filters.find_by_input_path('main.in'), Filter1)
        self.assertIsInstance(filters.find_by_input_path('main.in1'), Filter1)
        self.assertIsInstance(filters.find_by_input_path('main.in2'), Filter2)
        self.assertEquals(None, filters.find_by_input_path('main.out'))

    def test_filter_to_path(self):
        self.assertIsInstance(filters.find_by_output_path('main.out'), Filter1)
        self.assertIsInstance(filters.find_by_output_path('main.out2'), Filter2)
        self.assertEquals(None, filters.find_by_output_path('main.in'))
