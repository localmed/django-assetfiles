from assetfiles import filters, settings
from assetfiles.filters import BaseFilter, ExtensionMixin
from assetfiles.tests.base import AssetfilesTestCase


class Filter1(ExtensionMixin, BaseFilter):
    input_exts = ('in', 'in1')
    output_ext = 'out'


class Filter2(ExtensionMixin, BaseFilter):
    input_ext = 'in2'
    output_ext = 'out2'


class TestFilters(AssetfilesTestCase):
    def setUp(self):
        super(TestFilters, self).setUp()
        self.old_filters = settings.FILTERS
        settings.FILTERS = (
            'assetfiles.tests.filters.test_base.Filter1',
            'assetfiles.tests.filters.test_base.Filter2',
        )

    def tearDown(self):
        settings.FILTERS = self.old_filters

    def test_find_by_input_path(self):
        self.assertIsInstance(filters.find_by_input_path('main.in'), Filter1)
        self.assertIsInstance(filters.find_by_input_path('main.in1'), Filter1)
        self.assertIsInstance(filters.find_by_input_path('main.in2'), Filter2)
        self.assertEqual(None, filters.find_by_input_path('main.out'))

    def test_find_by_output_path(self):
        self.assertIsInstance(filters.find_by_output_path('main.out'), Filter1)
        self.assertIsInstance(filters.find_by_output_path('main.out2'), Filter2)
        self.assertEqual(None, filters.find_by_output_path('main.in'))


class ReplaceFilter(BaseFilter):
    def __init__(self, pattern, replacement, **kwargs):
        super(ReplaceFilter, self).__init__(**kwargs)
        self.pattern = pattern
        self.replacement = replacement

    def filter(self, input):
        with open(input, 'r') as file:
            return file.read().replace(self.pattern, self.replacement)


class TestBaseFilter(AssetfilesTestCase):
    def test_matches_set_input_path(self):
        filter = BaseFilter(input_path='dir/main.in')
        self.assertFalse(filter.matches_input('main.in'))
        self.assertFalse(filter.matches_input('dir/main.out'))
        self.assertFalse(filter.matches_input('dir/main'))
        self.assertFalse(filter.matches_input('dir/dir/main.in'))
        self.assertTrue(filter.matches_input('dir/main.in'))

    def test_derives_set_input_path(self):
        filter = BaseFilter(input_path='dir/main.in')
        self.assertEqual(filter.derive_input_paths('dir/main.in'),
            ['dir/main.in'])

    def test_matches_set_output_path(self):
        filter = BaseFilter(output_path='dir/main.out')
        self.assertFalse(filter.matches_output('main.out'))
        self.assertFalse(filter.matches_output('dir/main.in'))
        self.assertFalse(filter.matches_output('dir/main'))
        self.assertFalse(filter.matches_output('dir/dir/main.out'))
        self.assertTrue(filter.matches_output('dir/main.out'))

    def test_derives_set_output_path(self):
        filter = BaseFilter(output_path='dir/main.out')
        self.assertEqual(filter.derive_output_path('main.in'), 'dir/main.out')
        self.assertEqual(filter.derive_output_path('dir/main.in'), 'dir/main.out')

    def test_filters_a_single_input_file(self):
        filter = ReplaceFilter(pattern='Hello', replacement='World')
        path = self.mkfile('main.css', 'Hello')
        result = filter.filter(path)
        self.assertEqual('World', result)
