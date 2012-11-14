from django.test import TestCase
from django.test.client import Client

class TestServe(TestCase):
    def test_returns_not_found_without_an_asset(self):
        response = Client().get('/static/non/existent/file.css')
        self.assertEquals(response.status_code, 404)

    def test_returns_static_files(self):
        response = Client().get('/static/css/static.css')
        self.assertEquals(response.content.strip(), 'body { color: red; }')
        self.assertEquals(response.get('content-type'), 'text/css')

    def test_returns_static_files_with_correct_content_type(self):
        response = Client().get('/static/css/static.css')
        self.assertEquals(response.get('content-type'), 'text/css')

    def test_returns_app_static_files(self):
        response = Client().get('/static/css/app_static.css')
        self.assertEquals(response.content.strip(), 'body { color: blue; }')

    def test_processes_scss_files(self):
        response = Client().get('/static/css/simple.css')
        self.assertEquals(response.content.strip(), 'body {\n  color: red; }')

    def test_processes_app_scss_files(self):
        response = Client().get('/static/css/app.css')
        self.assertEquals(response.content.strip(), 'body {\n  color: yellow; }')

    def test_returns_processed_scss_files_with_correct_content_type(self):
        response = Client().get('/static/css/simple.css')
        self.assertEquals(response.get('content-type'), 'text/css')

    def test_processes_scss_files_with_deps(self):
        response = Client().get('/static/css/with_deps.css')
        self.assertEquals(response.content.strip(), 'body {\n  color: black; }')

    def test_processes_scss_files_with_app_deps(self):
        response = Client().get('/static/css/with_app_deps.css')
        self.assertEquals(response.content.strip(), 'body {\n  color: white; }')

    def test_integrates_static_url_with_sass(self):
        response = Client().get('/static/css/with_url.css')
        self.assertEquals(response.content.strip(),
            'body {\n  background: url("/static/img/bg.jpg"); }')
