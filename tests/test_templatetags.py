from django.template import loader, Context
from django.test.utils import override_settings
from django.utils import six
from nose.tools import *

from tests.base import AssetfilesTestCase


def assert_static_renders(path, result, asvar=False, **kwargs):
    template = _static_template_snippet(path, asvar)
    assert_equal(_render_template(template, **kwargs), result)


def _render_template(template, **kwargs):
    if isinstance(template, six.string_types):
        template = loader.get_template_from_string(template)
    return template.render(Context(kwargs)).strip()


def _static_template_snippet(path, asvar=False):
    return "{%% load static from staticfiles %%}{%% static '%s' %%}" % path


class TestTemplateTag(AssetfilesTestCase):

    def test_template_tag(self):
        assert_static_renders('does/not/exist.png',
                              '/static/does/not/exist.png')
        assert_static_renders('testfile.txt', '/static/testfile.txt')
        assert_static_renders('testfile.txt', '/static/testfile.txt')


@override_settings(
    STATICFILES_STORAGE='django.contrib.staticfiles.storage.CachedStaticFilesStorage',
    DEBUG=False,
)
class TestStaticTagWithCachedStorage(AssetfilesTestCase):

    def test_raises_error_without_a_file(self):
        assert_raises(ValueError,
                      assert_static_renders,
                      'does/not/exist.png',
                      '/static/does/not/exist.png')

    def test_does_not_change_folder_names(self):
        assert_static_renders('path/',
                              '/static/path/')
        assert_static_renders('path/?query',
                              '/static/path/?query')

    def test_returns_file_with_hash_name(self):
        self.mkfile('public/test/file.txt', 'Some Content')
        assert_static_renders('test/file.txt',
                              '/static/test/file.78138d2003f1.txt')
        assert_static_renders('test/file.txt',
                              '/static/test/file.78138d2003f1.txt')
