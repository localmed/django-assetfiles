from assetfiles.filters.coffee import CoffeeScriptFilterError
from assetfiles.tests.base import AssetfilesTestCase, filter


class TestCoffeeScriptFilter(AssetfilesTestCase):
    def test_processes_coffee_files(self):
        self.mkfile('static/js/simple.coffee', 'a = foo: "1#{2}3"')
        self.assertIn('foo: "1" + 2 + "3"', filter('js/simple.js'))

    def test_raises_syntax_error(self):
        with self.assertRaisesRegexp(
                CoffeeScriptFilterError,
                r'.*?SyntaxError.*?static/js/simple\.coffee.*?line 5'):
            self.mkfile('static/js/simple.coffee', '\n\n\n\na = foo: "1#{2}3')
            filter('js/simple.js')
