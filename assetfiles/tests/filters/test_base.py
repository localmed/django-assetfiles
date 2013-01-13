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
        self.assertEquals(None, filters.find_by_input_path('main.out'))

    def test_find_by_output_path(self):
        self.assertIsInstance(filters.find_by_output_path('main.out'), Filter1)
        self.assertIsInstance(filters.find_by_output_path('main.out2'), Filter2)
        self.assertEquals(None, filters.find_by_output_path('main.in'))


class ReplaceFilter(BaseFilter):
    def __init__(self, pattern, replacement):
        self.pattern = pattern
        self.replacement = replacement

    def filter(self, input):
        with open(input, 'r') as file:
            return file.read().replace(self.pattern, self.replacement)


class TestBaseFilter(AssetfilesTestCase):
    def test_filters_a_single_input_file(self):
        filter = ReplaceFilter('Hello', 'World')
        filter.pattern
        path = self.mkfile('main.css', 'Hello')
        result = filter.filter(path)
        self.assertEquals('World', result)
