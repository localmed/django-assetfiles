# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django_nose.tools import *

from tests.base import AssetfilesTestCase


class TestServe(AssetfilesTestCase):

    def test_returns_not_found_without_an_asset(self):
        response = self.client.get('/static/non/existent/file.css')
        assert_equal(response.status_code, 404)

    def test_returns_static_files(self):
        self.mkfile('static/css/static.css', 'body { color: red; }')
        response = self.client.get('/static/css/static.css')
        assert_contains(response, 'body { color: red; }')

    def test_returns_static_files_with_correct_content_type(self):
        self.mkfile('static/css/static.css')
        response = self.client.get('/static/css/static.css')
        assert_equal(response.get('content-type'), 'text/css')

    def test_returns_static_files_with_extra_extensions(self):
        self.mkfile('app-1/static/js/jquery.plugin.js', '$.fn.plugin = {};')
        response = self.client.get('/static/js/jquery.plugin.js')
        assert_contains(response, '$.fn.plugin = {};')

    def test_returns_app_static_files(self):
        self.mkfile('app-1/static/css/app_static.css', 'body { color: blue; }')
        response = self.client.get('/static/css/app_static.css')
        assert_contains(response, 'body { color: blue; }')

    def test_processes_scss_files(self):
        self.mkfile('static/css/simple.scss',
            '$c: red; body { color: $c; }')
        response = self.client.get('/static/css/simple.css')
        assert_contains(response, 'body {\n  color: red; }')

    def test_returns_processed_scss_files_with_correct_content_type(self):
        self.mkfile('static/css/simple.scss',
            '$c: red; body { color: $c; }')
        response = self.client.get('/static/css/simple.css')
        assert_equal(response.get('content-type'), 'text/css')

    def test_processes_app_scss_files(self):
        self.mkfile('app-1/static/css/app.scss',
            '$c: yellow; body { color: $c; }')
        response = self.client.get('/static/css/app.css')
        assert_contains(response, 'body {\n  color: yellow; }')

    def test_processes_scss_files_with_deps(self):
        self.mkfile('static/css/folder/_dep.scss', '$c: black;')
        self.mkfile('static/css/with_deps.scss',
            '@import "folder/dep"; body { color: $c; }')
        response = self.client.get('/static/css/with_deps.css')
        assert_contains(response, 'body {\n  color: black; }')

    def test_processes_scss_files_with_app_deps(self):
        self.mkfile('app-1/static/css/folder/_dep.scss', '$c: white;')
        self.mkfile('static/css/with_app_deps.scss',
            '@import "folder/dep"; body { color: $c; }')
        response = self.client.get('/static/css/with_app_deps.css')
        assert_contains(response, 'body {\n  color: white; }')

    def test_processes_asset_files_with_unicode_chars(self):
        self.mkfile('static/css/simple.scss',
            '$c: "é"; a::before { content: $c; }')
        self.mkfile('static/js/simple.coffee', 'a = foo: "é#{2}3"')
        response = self.client.get('/static/css/simple.css')
        assert_contains(response, 'a::before {\n  content: "é"; }')
        response = self.client.get('/static/js/simple.js')
        assert_contains(response, 'foo: "é" + 2 + "3"')
