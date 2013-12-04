from django.conf import settings

from nose.tools import *

from assetfiles import assets
from assetfiles.filters import BaseFilter, ExtensionMixin
import assetfiles.settings

from tests.base import AssetfilesTestCase


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
            'tests.test_assets.Filter1',
            'tests.test_assets.Filter2',
        )

    def tearDown(self):
        assetfiles.settings.FILTERS = self.old_filters

    def test_find_asset(self):
        path1 = self.mkfile('static/some/dir/main.out.in')
        path2 = self.mkfile('static/another/dir/main.in2')
        asset_path1, filter1 = assets.find('some/dir/main.out')
        asset_path2, filter2 = assets.find('another/dir/main.out2')
        asset_path3, filter3 = assets.find('non/existent/file.out')
        assert_equal(path1, asset_path1)
        assert_is_instance(filter1, Filter1)
        assert_equal(path2, asset_path2)
        assert_is_instance(filter2, Filter2)
        assert_equal(None, asset_path3)
        assert_equal(None, filter3)
