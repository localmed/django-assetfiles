from django.test.client import Client

from assetfiles.tests.base import AssetfilesTestCase


class TestServe(AssetfilesTestCase):
    def test_returns_not_found_without_an_asset(self):
        response = Client().get('/static/non/existent/file.css')
        self.assertEquals(response.status_code, 404)

    def test_returns_static_files(self):
        self.mkfile('static/css/static.css', 'body { color: red; }')
        response = Client().get('/static/css/static.css')
        self.assertEquals(response.content.strip(), 'body { color: red; }')
        self.assertEquals(response.get('content-type'), 'text/css')

    def test_returns_static_files_with_correct_content_type(self):
        self.mkfile('static/css/static.css')
        response = Client().get('/static/css/static.css')
        self.assertEquals(response.get('content-type'), 'text/css')

    def test_returns_app_static_files(self):
        self.mkfile('app-1/static/css/app_static.css', 'body { color: blue; }')
        response = Client().get('/static/css/app_static.css')
        self.assertEquals(response.content.strip(), 'body { color: blue; }')

    def test_processes_scss_files(self):
        self.mkfile('static/css/simple.scss',
            '$c: red; body { color: $c; }')
        response = Client().get('/static/css/simple.css')
        self.assertEquals(response.content.strip(), 'body {\n  color: red; }')

    def test_returns_processed_scss_files_with_correct_content_type(self):
        self.mkfile('static/css/simple.scss',
            '$c: red; body { color: $c; }')
        response = Client().get('/static/css/simple.css')
        self.assertEquals(response.get('content-type'), 'text/css')

    def test_processes_app_scss_files(self):
        self.mkfile('app-1/static/css/app.scss',
            '$c: yellow; body { color: $c; }')
        response = Client().get('/static/css/app.css')
        self.assertEquals(response.content.strip(), 'body {\n  color: yellow; }')

    def test_processes_scss_files_with_deps(self):
        self.mkfile('static/css/folder/_dep.scss', '$c: black;')
        self.mkfile('static/css/with_deps.scss',
            '@import "folder/dep"; body { color: $c; }')
        response = Client().get('/static/css/with_deps.css')
        self.assertEquals(response.content.strip(), 'body {\n  color: black; }')

    def test_processes_scss_files_with_app_deps(self):
        self.mkfile('app-1/static/css/folder/_dep.scss', '$c: white;')
        self.mkfile('static/css/with_app_deps.scss',
            '@import "folder/dep"; body { color: $c; }')
        response = Client().get('/static/css/with_app_deps.css')
        self.assertEquals(response.content.strip(), 'body {\n  color: white; }')
