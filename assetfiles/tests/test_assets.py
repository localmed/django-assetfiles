from django.conf import settings

from assetfiles import assets
from assetfiles.filters import BaseFilter, ExtensionMixin
from assetfiles.tests.base import AssetfilesTestCase
import assetfiles.settings


class Filter1(ExtensionMixin, BaseFilter):
    input_exts = ('in', 'in1')
    output_ext = 'out'


class Filter2(ExtensionMixin, BaseFilter):
    input_ext = 'in2'
    output_ext = 'out2'


class TestAssets(AssetfilesTestCase):
    def setUp(self):
        super(TestAssets, self).setUp()
        self.old_filters = assetfiles.settings.FILTERS
        assetfiles.settings.FILTERS = (
            'assetfiles.tests.test_assets.Filter1',
            'assetfiles.tests.test_assets.Filter2',
        )

    def tearDown(self):
        assetfiles.settings.FILTERS = self.old_filters

    def test_find_asset(self):
        path1 = self.mkfile('static/some/dir/main.out.in')
        path2 = self.mkfile('static/another/dir/main.in2')
        asset_path1, filter1 = assets.find('some/dir/main.out')
        asset_path2, filter2 = assets.find('another/dir/main.out2')
        asset_path3, filter3 = assets.find('non/existent/file.out')
        self.assertEqual(path1, asset_path1)
        self.assertIsInstance(filter1, Filter1)
        self.assertEqual(path2, asset_path2)
        self.assertIsInstance(filter2, Filter2)
        self.assertEqual(None, asset_path3)
        self.assertEqual(None, filter3)
