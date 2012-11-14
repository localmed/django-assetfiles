import os, shutil, tempfile

from django.conf import settings
from django.test import TestCase

from assetfiles import find_asset, filter_from_path, filter_to_path
from assetfiles.filters.base import BaseFilter
from assetfiles.tests.base import AssetfilesTestCase
import assetfiles.settings

class Filter1(BaseFilter):
    input_exts = ('in', 'in1')
    output_ext = 'out'

class Filter2(BaseFilter):
    input_exts = ('in2',)
    output_ext = 'out2'

class TestApp(AssetfilesTestCase):
    def setUp(self):
        super(TestApp, self).setUp()
        self.root = self.mkdir()
        self.old_filters = assetfiles.settings.FILTERS
        self.old_staticfiles_dirs = settings.STATICFILES_DIRS
        assetfiles.settings.FILTERS = (
            'tests.test_app.Filter1',
            'tests.test_app.Filter2',
        )
        settings.STATICFILES_DIRS = (self.root,)

    def tearDown(self):
        assetfiles.settings.FILTERS = self.old_filters
        settings.STATICFILES_DIRS = self.old_staticfiles_dirs

    def test_find_asset(self):
        path1 = self.mkfile('some/dir/main.out.in')
        path2 = self.mkfile('another/dir/main.in2')
        asset_path1, filter1 = find_asset('some/dir/main.out')
        asset_path2, filter2 = find_asset('another/dir/main.out2')
        asset_path3, filter3 = find_asset('non/existent/file.out')
        self.assertEquals(path1, asset_path1)
        self.assertIsInstance(filter1, Filter1)
        self.assertEquals(path2, asset_path2)
        self.assertIsInstance(filter2, Filter2)
        self.assertEquals(None, asset_path3)
        self.assertEquals(None, filter3)

    def test_finds_filter_by_input_file(self):
        self.assertIsInstance(filter_from_path('main.in'), Filter1)
        self.assertIsInstance(filter_from_path('main.in1'), Filter1)
        self.assertIsInstance(filter_from_path('main.in2'), Filter2)
        self.assertEquals(None, filter_from_path('main.out'))

    def test_finds_filter_by_output_file(self):
        self.assertIsInstance(filter_to_path('main.out'), Filter1)
        self.assertIsInstance(filter_to_path('main.out2'), Filter2)
        self.assertEquals(None, filter_to_path('main.in'))
