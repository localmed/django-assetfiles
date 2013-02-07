from django.template import loader, Context
from django.test.utils import override_settings
from django.utils import six

from assetfiles.tests.base import AssetfilesTestCase


class BaseTemplateTagsTestCase(AssetfilesTestCase):
    def render_template(self, template, **kwargs):
        if isinstance(template, six.string_types):
            template = loader.get_template_from_string(template)
        return template.render(Context(kwargs)).strip()

    def static_template_snippet(self, path, asvar=False):
        return "{%% load static from staticfiles %%}{%% static '%s' %%}" % path

    def assertStaticRenders(self, path, result, asvar=False, **kwargs):
        template = self.static_template_snippet(path, asvar)
        self.assertEqual(self.render_template(template, **kwargs), result)


class TestTemplateTag(BaseTemplateTagsTestCase):
    def test_template_tag(self):
        self.assertStaticRenders('does/not/exist.png',
                                 '/static/does/not/exist.png')
        self.assertStaticRenders('testfile.txt', '/static/testfile.txt')
        self.assertStaticRenders('testfile.txt', '/static/testfile.txt')


@override_settings(
    STATICFILES_STORAGE='django.contrib.staticfiles.storage.CachedStaticFilesStorage',
    DEBUG=False,
)
class TestStaticTagWithCachedStorage(BaseTemplateTagsTestCase):
    def test_raises_error_without_a_file(self):
        self.assertRaises(ValueError,
                          self.assertStaticRenders,
                          'does/not/exist.png',
                          '/static/does/not/exist.png')

    def test_does_not_change_folder_names(self):
        self.assertStaticRenders('path/',
                                 '/static/path/')
        self.assertStaticRenders('path/?query',
                                 '/static/path/?query')

    def test_returns_file_with_hash_name(self):
        self.mkfile('public/test/file.txt', 'Some Content')
        self.assertStaticRenders('test/file.txt',
                                 '/static/test/file.78138d2003f1.txt')
        self.assertStaticRenders('test/file.txt',
                                 '/static/test/file.78138d2003f1.txt')
