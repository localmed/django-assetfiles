# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import codecs
import os

from django.conf import settings
from django.contrib.staticfiles import storage
from django.core import management
from django.core.management.base import CommandError
from django.utils import six
from nose.tools import *

from tests.base import is_at_least_django_15, AssetfilesTestCase


def call_command(*args, **kwargs):
    stdout = six.StringIO()
    kwargs.update({'stdout': stdout, 'stderr': six.StringIO(), 'verbosity': 1})
    management.call_command(*args, **kwargs)
    stdout.seek(0)
    return stdout


def assert_static_file_not_found(path):
    static_path = os.path.join(settings.STATIC_ROOT, path)
    assert_false(os.path.isfile(static_path),
        "file '{0}' exists".format(path))


def assert_static_file_exists(path):
    static_path = os.path.join(settings.STATIC_ROOT, path)
    assert_true(os.path.isfile(static_path),
        "file '{0}' does not exist".format(path))


def assert_static_file_contains(path, text):
    static_path = os.path.join(settings.STATIC_ROOT, path)

    assert_static_file_exists(path)
    with codecs.open(static_path, 'r', encoding='utf-8') as file:
        file_data = file.read()
        assert_in(text, file_data,
            "'{0}' not in file '{1}'.".format(text, path))


class TestFindStatic(AssetfilesTestCase):

    def setUp(self):
        super(TestFindStatic, self).setUp()
        self.mkfile('static/css/main.css')
        self.mkfile('app-1/static/css/main.css')
        self.mkfile('app-2/static/css/main.css')

    def test_find_file(self):
        out = call_command('findstatic', 'css/main.css', all=False)
        lines = out.readlines()[1:]
        assert_equal(len(lines), 1)
        assert_in('project/static/css/main.css', lines[0])

    def test_find_all_files(self):
        out = call_command('findstatic', 'css/main.css')
        lines = out.readlines()[1:]
        assert_equal(len(lines), 3)
        assert_in('project/static/css/main.css', lines[0])
        assert_in('app-1/static/css/main.css', lines[1])
        assert_in('app-2/static/css/main.css', lines[2])


class CustomStorage(storage.StaticFilesStorage):

    def post_process(self, paths, dry_run=False, **options):
        path_level = lambda name: len(name.split(os.sep))
        for name in sorted(paths.keys(), key=path_level, reverse=True):
            storage, path = paths[name]
            with storage.open(path) as original_file:
                new_name = name.replace('simple', 'complex')
                self._save(new_name, original_file)
                yield name, new_name, True


class TestCollectStatic(AssetfilesTestCase):

    def setUp(self):
        super(TestCollectStatic, self).setUp()
        self.old_staticfiles_storage = storage.staticfiles_storage

    def tearDown(self):
        super(TestCollectStatic, self).tearDown()
        storage.staticfiles_storage = self.old_staticfiles_storage

    def collectstatic(self, *args, **kwargs):
        kwargs.update({'interactive': False, 'clear': True})
        return call_command('collectstatic', *args, **kwargs)

    def test_copies_static_files(self):
        self.mkfile('static/css/static.css',
            'body { color: red; }')
        self.collectstatic()
        assert_static_file_contains('css/static.css',
            'body { color: red; }')

    def test_copies_unicode_static_files(self):
        self.mkfile('static/css/static.css',
            'a::before { content: "é"; }')
        self.collectstatic()
        assert_static_file_contains('css/static.css',
            'a::before { content: "é"; }')

    def test_copies_static_files_with_prefix(self):
        self.mkfile('static-prefix/css/static.css',
            'body { color: red; }')
        self.collectstatic()
        assert_static_file_contains('prefix/css/static.css',
            'body { color: red; }')

    def test_post_processes_static_files(self):
        storage.staticfiles_storage = CustomStorage()
        self.mkfile('static-prefix/css/simple.css',
            'body { color: red; }')
        self.collectstatic()
        assert_static_file_contains('prefix/css/complex.css',
            'body { color: red; }')

    def test_copies_app_static_files(self):
        self.mkfile('app-1/static/css/app_static.css',
            'body { color: blue; }')
        self.collectstatic()
        assert_static_file_contains('css/app_static.css',
            'body { color: blue; }')

    def test_processes_scss_files(self):
        self.mkfile('static/css/simple.scss',
            '$c: red; body { color: $c; }')
        self.collectstatic()
        assert_static_file_contains('css/simple.css',
            'body {\n  color: red; }')

    def test_processes_unicode_asset_files(self):
        self.mkfile('static/css/simple.scss',
            '$content: "é"; a::before { content: $content; }')
        self.mkfile('static/js/simple.coffee', 'a = foo: "é#{2}3"')
        self.collectstatic()
        assert_static_file_contains('css/simple.css',
            'a::before {\n  content: "é"; }')
        assert_static_file_contains('js/simple.js', 'foo: "é" + 2 + "3"')

    def test_processes_scss_files_with_prefix(self):
        self.mkfile('static-prefix/css/simple.scss',
            '$c: red; body { color: $c; }')
        self.collectstatic()
        assert_static_file_contains('prefix/css/simple.css',
            'body {\n  color: red; }')

    def test_processes_app_scss_files(self):
        self.mkfile('app-1/static/css/app.scss',
            '$c: yellow; body { color: $c; }')
        self.collectstatic()
        assert_static_file_contains('css/app.css',
            'body {\n  color: yellow; }')

    def test_processes_scss_files_with_deps(self):
        self.mkfile('static/css/folder/_dep.scss', '$c: black;')
        self.mkfile('static/css/with_deps.scss',
            '@import "folder/dep"; body { color: $c; }')
        self.collectstatic()
        assert_static_file_contains('css/with_deps.css',
            'body {\n  color: black; }')

    def test_processes_scss_files_with_app_deps(self):
        self.mkfile('app-1/static/css/folder/_dep.scss', '$c: white;')
        self.mkfile('static/css/with_app_deps.scss',
            '@import "folder/dep"; body { color: $c; }')
        self.collectstatic()
        assert_static_file_contains('css/with_app_deps.css',
            'body {\n  color: white; }')

    def test_skips_sass_dependencies(self):
        self.mkfile('static/css/_dep.scss', '$c: black;')
        self.mkfile('static/css/with_deps.scss',
            '@import "dep"; body { color: $c; }')
        self.collectstatic()
        assert_static_file_not_found('css/_dep.css')
        assert_static_file_not_found('css/_dep.scss')

    def test_processes_coffee_files(self):
        self.mkfile('static/js/simple.coffee', 'a = foo: "1#{2}3"')
        self.collectstatic()
        assert_static_file_contains('js/simple.js', 'foo: "1" + 2 + "3"')

    def test_post_processes_asset_files(self):
        storage.staticfiles_storage = CustomStorage()
        self.mkfile('static/css/simple.scss',
            '$c: red; body { color: $c; }')
        self.collectstatic()
        assert_static_file_contains('css/complex.css',
            'body {\n  color: red; }')

    def test_post_processes_asset_files_with_prefix(self):
        storage.staticfiles_storage = CustomStorage()
        self.mkfile('static-prefix/css/simple.scss',
            '$c: red; body { color: $c; }')
        self.collectstatic()
        assert_static_file_contains('prefix/css/complex.css',
            'body {\n  color: red; }')

    def test_does_not_allow_symlinking(self):
        error = CommandError if is_at_least_django_15() else SystemExit
        with assert_raises(error):
            self.collectstatic(link=True)
