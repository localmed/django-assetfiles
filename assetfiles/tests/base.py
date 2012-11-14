import os, shutil, tempfile

from django.contrib.staticfiles import finders, storage
from django.test import TestCase
from django.utils.functional import empty

from assetfiles import filters
from assetfiles.filters.base import BaseFilter

class AssetfilesTestCase(TestCase):
    def setUp(self):
        # Clear the cached staticfiles_storage out, this is because when it first
        # gets accessed (by some other test), it evaluates settings.STATIC_ROOT,
        # since we're planning on changing that we need to clear out the cache.
        storage.staticfiles_storage._wrapped = empty
        # Clear the cached staticfile finders, so they are reinitialized every
        # run and pick up changes in settings.STATICFILES_DIRS.
        finders._finders.clear()
        # Clear the cached assetfile filters, so they are reinitialized every
        # run and pick up changes in settings.ASSETFILES_FILTERS.
        filters._filters.clear()

    def mkdir(self):
        path = tempfile.mkdtemp(prefix='assetfiles-')
        self.addCleanup(shutil.rmtree, path, ignore_errors=True)
        return path

    def mkfile(self, relative_path, content=None, root=None):
        if root is None and self.root: root = self.root

        abspath = os.path.join(root, relative_path)
        dirname = os.path.dirname(abspath)

        if not os.path.isdir(dirname): os.makedirs(dirname)

        with open(abspath, 'w') as file:
            if content: file.write(content)

        return abspath

class ReplaceFilter(BaseFilter):
    input_exts = ('foo', 'baz')
    output_ext = 'bar'

    def __init__(self, pattern='a', replacement='b'):
        self.pattern = pattern
        self.replacement = replacement

    def filter(self, input):
        with open(input, 'r') as file:
            return file.read().replace(self.pattern, self.replacement)

class Filter1(BaseFilter):
    input_exts = ('in', 'in1')
    output_ext = 'out'

class Filter2(BaseFilter):
    input_exts = ('in2',)
    output_ext = 'out2'
