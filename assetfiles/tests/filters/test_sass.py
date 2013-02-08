from __future__ import unicode_literals

import re

from assetfiles.filters.sass import SassFilterError
from assetfiles.tests.base import assertRaisesRegex, AssetfilesTestCase, filter


class TestSassFilter(AssetfilesTestCase):
    def test_processes_scss_files(self):
        self.mkfile(
            'static/css/simple.scss',
            '$c: red; body { color: $c; }')
        self.assertEqual(filter('css/simple.css'), b'body {\n  color: red; }')

    def test_processes_app_scss_files(self):
        self.mkfile(
            'app-1/static/css/app.scss',
            '$c: yellow; body { color: $c; }')
        self.assertEqual(filter('css/app.css'), b'body {\n  color: yellow; }')

    def test_processes_scss_files_with_deps(self):
        self.mkfile('static/css/folder/_dep.scss', '$c: black;')
        self.mkfile(
            'static/css/with_deps.scss',
            '@import "folder/dep"; body { color: $c; }')
        self.assertEqual(
            filter('css/with_deps.css'),
            b'body {\n  color: black; }')

    def test_processes_scss_files_with_app_deps(self):
        self.mkfile('app-1/static/css/folder/_dep.scss', '$c: white;')
        self.mkfile(
            'static/css/with_app_deps.scss',
            '@import "folder/dep"; body { color: $c; }')
        self.assertEqual(
            filter('css/with_app_deps.css'),
            b'body {\n  color: white; }')

    def test_integrates_static_url_with_sass(self):
        self.mkfile(
            'static/css/with_url.scss',
            'body { background: static-url("img/bg.jpg"); }')
        self.assertEqual(
            filter('css/with_url.css'),
            b'body {\n  background: url("/static/img/bg.jpg"); }')

    def test_integrates_with_compass(self):
        self.mkfile(
            'static/css/with_compass.scss',
            '@import "compass"; .btn { @include border-radius(5px); }')
        self.assertIn(b'border-radius: 5px;', filter('css/with_compass.css'))

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
            b'body {\n  background: url("/static/img/bg.jpg"); }')
        self.assertEqual(
            filter('css/only_path.css'),
            b'body {\n  background: url("/static/img/bg.jpg"); }')
        self.assertEqual(
            filter('css/cache_buster.css'),
            b'body {\n  background: url("/static/img/bg.jpg"); }')

    def test_integrates_with_compass_font_url(self):
        self.mkfile(
            'static/css/font_url.scss',
            '@font-face { src: font-url("fonts/font.ttf"); }')
        self.mkfile(
            'static/css/only_path.scss',
            '@font-face { src: url(font-url("fonts/font.ttf", true)); }')
        self.assertEqual(
            filter('css/font_url.css'),
            b'@font-face {\n  src: url("/static/fonts/font.ttf"); }')
        self.assertEqual(
            filter('css/only_path.css'),
            b'@font-face {\n  src: url("/static/fonts/font.ttf"); }')

    def test_raises_syntax_error(self):
        message = re.compile(
            r'.*?Syntax error.*?line 5.*?static/css/syntax_error\.scss',
            re.DOTALL)
        with assertRaisesRegex(self, SassFilterError, message):
            self.mkfile('static/css/syntax_error.scss', '\n\n\n\nbody {')
            filter('css/syntax_error.css')
