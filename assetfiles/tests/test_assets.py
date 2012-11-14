import os, shutil, tempfile

from django.conf import settings
from django.test import TestCase

from assetfiles import assets
from assetfiles.tests.base import AssetfilesTestCase, Filter1, Filter2
import assetfiles.settings

class TestAssets(AssetfilesTestCase):
    def setUp(self):
        super(TestAssets, self).setUp()
        self.root = self.mkdir()
        self.old_filters = assetfiles.settings.FILTERS
        self.old_staticfiles_dirs = settings.STATICFILES_DIRS
        assetfiles.settings.FILTERS = (
            'assetfiles.tests.base.Filter1',
            'assetfiles.tests.base.Filter2',
        )
        settings.STATICFILES_DIRS = (self.root,)

    def tearDown(self):
        assetfiles.settings.FILTERS = self.old_filters
        settings.STATICFILES_DIRS = self.old_staticfiles_dirs

    def test_find_asset(self):
        path1 = self.mkfile('some/dir/main.out.in')
        path2 = self.mkfile('another/dir/main.in2')
        asset_path1, filter1 = assets.find('some/dir/main.out')
        asset_path2, filter2 = assets.find('another/dir/main.out2')
        asset_path3, filter3 = assets.find('non/existent/file.out')
        self.assertEquals(path1, asset_path1)
        self.assertIsInstance(filter1, Filter1)
        self.assertEquals(path2, asset_path2)
        self.assertIsInstance(filter2, Filter2)
        self.assertEquals(None, asset_path3)
        self.assertEquals(None, filter3)
