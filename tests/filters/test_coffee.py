from __future__ import unicode_literals

from nose.tools import *

from assetfiles import settings
from assetfiles.filters.coffee import CoffeeScriptFilterError

from tests.base import AssetfilesTestCase, filter


class TestCoffeeScriptFilter(AssetfilesTestCase):

    def setUp(self):
        super(TestCoffeeScriptFilter, self).setUp()
        self.original_coffee_options = settings.COFFEE_SCRIPT_OPTIONS

    def tearDown(self):
        super(TestCoffeeScriptFilter, self).tearDown()
        settings.COFFEE_SCRIPT_OPTIONS = self.original_coffee_options

    def test_processes_coffee_files(self):
        self.mkfile('static/js/simple.coffee', 'a = foo: "1#{2}3"')
        assert_in(b'foo: "1" + 2 + "3"', filter('js/simple.js'))

    def test_uses_coffee_script_options(self):
        settings.COFFEE_SCRIPT_OPTIONS = {'bare': True}
        self.mkfile('static/js/simple.coffee', 'a = foo: "1#{2}3"')
        assert_not_in(b'(function() {', filter('js/simple.js'))

    def test_raises_syntax_error(self):
        with assert_raises(CoffeeScriptFilterError):
            self.mkfile('static/js/simple.coffee', '\n\n\n\na = foo: "1#{2}3')
            filter('js/simple.js')
