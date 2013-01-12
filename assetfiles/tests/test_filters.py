import os
import shutil
import tempfile

from assetfiles import assets, filters, settings
from assetfiles.filters.base import BaseFilter, SingleOutputMixin, SingleInputMixin
from assetfiles.filters.coffee import CoffeeScriptFilterError
from assetfiles.filters.sass import SassFilterError
from assetfiles.tests.base import (AssetfilesTestCase,
                                   ReplaceFilter, Filter1, Filter2)

def assertRaisesRegex(self, *args, **kwargs):
    '''
    Python 2/3 compatibility not offered by Django 1.4's version of six.
    '''
    method = 'assertRaisesRegex'
    if not hasattr(self, method):
        method = 'assertRaisesRegexp'
    return getattr(self, method)(*args, **kwargs)


def filter(path):
    asset_path, filter = assets.find(path)
    return filter.filter(asset_path).strip()


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

    def test_find_by_input_path(self):
        self.assertIsInstance(filters.find_by_input_path('main.in'), Filter1)
        self.assertIsInstance(filters.find_by_input_path('main.in1'), Filter1)
        self.assertIsInstance(filters.find_by_input_path('main.in2'), Filter2)
        self.assertEquals(None, filters.find_by_input_path('main.out'))

    def test_find_by_output_path(self):
        self.assertIsInstance(filters.find_by_output_path('main.out'), Filter1)
        self.assertIsInstance(filters.find_by_output_path('main.out2'), Filter2)
        self.assertEquals(None, filters.find_by_output_path('main.in'))


class TestBaseFilter(AssetfilesTestCase):
    def test_filters_a_single_input_file(self):
        filter = ReplaceFilter('Hello', 'World')
        path = self.mkfile('main.css', 'Hello')
        result = filter.filter(path)
        self.assertEqual('World', result)

    def test_matches_input_file_by_ext(self):
        filter = ReplaceFilter()
        path1 = os.path.join(self.root, 'main.foo')
        path2 = os.path.join(self.root, 'main.baz')
        path3 = os.path.join(self.root, 'main.plugin.foo')
        path4 = os.path.join(self.root, 'main.css')
        self.assertTrue(filter.matches_input(path1))
        self.assertTrue(filter.matches_input(path2))
        self.assertTrue(filter.matches_input(path3))
        self.assertFalse(filter.matches_input(path4))

    def test_does_not_match_input_file_without_input_exts(self):
        filter = ReplaceFilter()
        filter.input_exts = ()
        path1 = os.path.join(self.root, 'main.foo')
        path2 = os.path.join(self.root, 'main.baz')
        self.assertFalse(filter.matches_input(path1))
        self.assertFalse(filter.matches_input(path2))

    def test_set_single_input_ext(self):
        filter = ReplaceFilter()
        filter.input_ext = 'foo'
        self.assertEqual(('foo',), filter.input_exts)

    def test_matches_output_file_by_ext(self):
        filter = ReplaceFilter()
        self.assertTrue(filter.matches_output('main.bar'))
        self.assertTrue(filter.matches_output('main.plugin.bar'))
        self.assertFalse(filter.matches_output('main.foo'))

    def test_does_not_match_output_file_without_output_ext(self):
        filter = ReplaceFilter()
        filter.output_ext = None
        self.assertFalse(filter.matches_output('main.bar'))

    def test_derive_input_paths(self):
        filter = ReplaceFilter()
        self.assertEqual(set([
            'dir/main.bar.foo',
            'dir/main.foo',
            'dir/main.bar.baz',
            'dir/main.baz',
        ]), filter.derive_input_paths('dir/main.bar'))
        self.assertEquals(set([
            'dir/main.plugin.bar.foo',
            'dir/main.plugin.foo',
            'dir/main.plugin.bar.baz',
            'dir/main.plugin.baz',
        ]), filter.derive_input_paths('dir/main.plugin.bar'))

    def test_derive_output_path(self):
        filter = ReplaceFilter()
        self.assertEquals('dir/main.bar',
            filter.derive_output_path('dir/main.foo'))
        self.assertEquals('dir/main.bar',
            filter.derive_output_path('dir/main.bar.foo'))
        self.assertEquals('dir/main.plugin.bar',
            filter.derive_output_path('dir/main.plugin.foo'))


class TestSingleOutputMixin(AssetfilesTestCase):
    class SingleOutputFilter(SingleOutputMixin, BaseFilter):
        pass

    def test_matches_set_output_path(self):
        filter = self.SingleOutputFilter(output_path='dir/main.out')
        self.assertFalse(filter.matches_output('main.out'))
        self.assertFalse(filter.matches_output('dir/main.in'))
        self.assertFalse(filter.matches_output('dir/main'))
        self.assertFalse(filter.matches_output('dir/dir/main.out'))
        self.assertTrue(filter.matches_output('dir/main.out'))

    def test_derive_output_path(self):
        filter = self.SingleOutputFilter(output_path='dir/main.out')
        self.assertEquals(filter.derive_output_path('main.in'), 'dir/main.out')
        self.assertEquals(filter.derive_output_path('dir/main.in'), 'dir/main.out')


class TestSingleInputMixin(AssetfilesTestCase):
    class SingleInputFilter(SingleInputMixin, BaseFilter):
        pass

    def test_matches_set_input_path(self):
        filter = self.SingleInputFilter(input_path='dir/main.in')
        self.assertFalse(filter.matches_input('main.in'))
        self.assertFalse(filter.matches_input('dir/main.out'))
        self.assertFalse(filter.matches_input('dir/main'))
        self.assertFalse(filter.matches_input('dir/dir/main.in'))
        self.assertTrue(filter.matches_input('dir/main.in'))

    def test_derive_input_paths(self):
        filter = self.SingleInputFilter(input_path='dir/main.in')
        self.assertEquals(filter.derive_input_paths('main.in'),
            set(['dir/main.in']))
        self.assertEquals(filter.derive_input_paths('dir/main.in'),
            set(['dir/main.in']))


class TestSassFilter(AssetfilesTestCase):
    def test_processes_scss_files(self):
        self.mkfile(
            'static/css/simple.scss',
            '$c: red; body { color: $c; }')
        self.assertEqual(filter('css/simple.css'), 'body {\n  color: red; }')

    def test_processes_app_scss_files(self):
        self.mkfile(
            'app-1/static/css/app.scss',
            '$c: yellow; body { color: $c; }')
        self.assertEqual(filter('css/app.css'), 'body {\n  color: yellow; }')

    def test_processes_scss_files_with_deps(self):
        self.mkfile('static/css/folder/_dep.scss', '$c: black;')
        self.mkfile(
            'static/css/with_deps.scss',
            '@import "folder/dep"; body { color: $c; }')
        self.assertEqual(
            filter('css/with_deps.css'),
            'body {\n  color: black; }')

    def test_processes_scss_files_with_app_deps(self):
        self.mkfile('app-1/static/css/folder/_dep.scss', '$c: white;')
        self.mkfile(
            'static/css/with_app_deps.scss',
            '@import "folder/dep"; body { color: $c; }')
        self.assertEqual(
            filter('css/with_app_deps.css'),
            'body {\n  color: white; }')

    def test_integrates_static_url_with_sass(self):
        self.mkfile(
            'static/css/with_url.scss',
            'body { background: static-url("img/bg.jpg"); }')
        self.assertEqual(
            filter('css/with_url.css'),
            'body {\n  background: url("/static/img/bg.jpg"); }')

    def test_integrates_with_compass(self):
        self.mkfile(
            'static/css/with_compass.scss',
            '@import "compass"; .btn { @include border-radius(5px); }')
        self.assertIn('border-radius: 5px;', filter('css/with_compass.css'))

    def test_integrates_with_compass_image_url(self):
        self.mkfile(
            'static/css/image_url.scss',
            'body { background: image-url("img/bg.jpg"); }')
        self.mkfile(
            'static/css/only_path.scss',
            'body { background: url(image-url("img/bg.jpg", true)); }')
        self.mkfile(
            'static/css/cache_buster.scss',
            'body { background: image-url("img/bg.jpg", false, true); }')
        self.assertEqual(
            filter('css/image_url.css'),
            'body {\n  background: url("/static/img/bg.jpg"); }')
        self.assertEqual(
            filter('css/only_path.css'),
            'body {\n  background: url("/static/img/bg.jpg"); }')
        self.assertEqual(
            filter('css/cache_buster.css'),
            'body {\n  background: url("/static/img/bg.jpg"); }')

    def test_integrates_with_compass_font_url(self):
        self.mkfile(
            'static/css/font_url.scss',
            '@font-face { src: font-url("fonts/font.ttf"); }')
        self.mkfile(
            'static/css/only_path.scss',
            '@font-face { src: url(font-url("fonts/font.ttf", true)); }')
        self.assertEqual(
            filter('css/font_url.css'),
            '@font-face {\n  src: url("/static/fonts/font.ttf"); }')
        self.assertEqual(
            filter('css/only_path.css'),
            '@font-face {\n  src: url("/static/fonts/font.ttf"); }')

    def test_raises_syntax_error(self):
        with assertRaisesRegex(self,
                SassFilterError,
                r'.*?Syntax error.*?\n.*?line 5.*?static/css/syntax_error\.scss'):
            self.mkfile('static/css/syntax_error.scss', '\n\n\n\nbody {')
            filter('css/syntax_error.css')


class TestCoffeeScriptFilter(AssetfilesTestCase):
    def test_processes_coffee_files(self):
        self.mkfile('static/js/simple.coffee', 'a = foo: "1#{2}3"')
        self.assertIn('foo: "1" + 2 + "3"', filter('js/simple.js'))

    def test_raises_syntax_error(self):
        with assertRaisesRegex(self,
                CoffeeScriptFilterError,
                r'.*?SyntaxError.*?static/js/simple\.coffee.*?line 5'):
            self.mkfile('static/js/simple.coffee', '\n\n\n\na = foo: "1#{2}3')
            filter('js/simple.js')
