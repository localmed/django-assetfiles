from __future__ import unicode_literals

import os
import re

from nose.tools import *

from assetfiles import settings
from assetfiles.filters.sass import SassFilterError

from tests.base import AssetfilesTestCase, filter


class TestSassFilter(AssetfilesTestCase):

    def setUp(self):
        super(TestSassFilter, self).setUp()
        self.original_sass_options = settings.SASS_OPTIONS

    def tearDown(self):
        super(TestSassFilter, self).tearDown()
        settings.SASS_OPTIONS = self.original_sass_options

    def test_processes_scss_files(self):
        self.mkfile(
            'static/css/simple.scss',
            '$c: red; body { color: $c; }')
        assert_equal(filter('css/simple.css'), b'body {\n  color: red; }')

    def test_processes_app_scss_files(self):
        self.mkfile(
            'app-1/static/css/app.scss',
            '$c: yellow; body { color: $c; }')
        assert_equal(filter('css/app.css'), b'body {\n  color: yellow; }')

    def test_processes_scss_files_with_deps(self):
        self.mkfile('static/css/folder/_dep.scss', '$c: black;')
        self.mkfile(
            'static/css/with_deps.scss',
            '@import "folder/dep"; body { color: $c; }')
        assert_equal(
            filter('css/with_deps.css'),
            b'body {\n  color: black; }')

    def test_processes_scss_files_with_app_deps(self):
        self.mkfile('app-1/static/css/folder/_dep.scss', '$c: white;')
        self.mkfile(
            'static/css/with_app_deps.scss',
            '@import "folder/dep"; body { color: $c; }')
        assert_equal(
            filter('css/with_app_deps.css'),
            b'body {\n  color: white; }')

    def test_integrates_static_url_with_sass(self):
        self.mkfile(
            'static/css/with_url.scss',
            'body { background: static-url("img/bg.jpg"); }')
        assert_equal(
            filter('css/with_url.css'),
            b'body {\n  background: url("/static/img/bg.jpg"); }')

    def test_uses_sass_options(self):
        settings.SASS_OPTIONS = {
            'load_paths': [os.path.join(self.root, 'additional/load/path')],
            'style': 'compressed'
        }
        self.mkfile('additional/load/path/folder/_dep.scss', '$c: white;')
        self.mkfile(
            'static/css/with_load_path_deps.scss',
            '@import "folder/dep"; body { color: $c; }')
        assert_equal(
            filter('css/with_load_path_deps.css'),
            b'body{color:#fff}')

    def test_integrates_with_compass(self):
        self.mkfile(
            'static/css/with_compass.scss',
            '@import "compass"; .btn { @include border-radius(5px); }')
        assert_in(b'border-radius: 5px;', filter('css/with_compass.css'))

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
        assert_equal(
            filter('css/image_url.css'),
            b'body {\n  background: url("/static/img/bg.jpg"); }')
        assert_equal(
            filter('css/only_path.css'),
            b'body {\n  background: url("/static/img/bg.jpg"); }')
        assert_equal(
            filter('css/cache_buster.css'),
            b'body {\n  background: url("/static/img/bg.jpg"); }')

    def test_integrates_with_compass_font_url(self):
        self.mkfile(
            'static/css/font_url.scss',
            '@font-face { src: font-url("fonts/font.ttf"); }')
        self.mkfile(
            'static/css/only_path.scss',
            '@font-face { src: url(font-url("fonts/font.ttf", true)); }')
        assert_equal(
            filter('css/font_url.css'),
            b'@font-face {\n  src: url("/static/fonts/font.ttf"); }')
        assert_equal(
            filter('css/only_path.css'),
            b'@font-face {\n  src: url("/static/fonts/font.ttf"); }')

    def test_raises_syntax_error(self):
        with assert_raises(SassFilterError):
            self.mkfile('static/css/syntax_error.scss', '\n\n\n\nbody {')
            filter('css/syntax_error.css')
