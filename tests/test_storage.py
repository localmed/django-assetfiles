from __future__ import unicode_literals

from nose.tools import *

from assetfiles.storage import TempFilesStorage


class TestTempFilesStorage(object):

    def test_stores_in_memory(self):
        storage = TempFilesStorage()
        storage.save('path/to/file.txt', 'Hello World!')
        assert_true(storage.exists('path/to/file.txt'))

    def test_opens_strings_as_content_files(self):
        storage = TempFilesStorage()
        storage.save('path/to/file.txt', 'Hello World!')
        file = storage.open('path/to/file.txt')
        assert_equal('Hello World!', ''.join(file.chunks()))

    def test_deletes_storage(self):
        storage = TempFilesStorage()
        storage.save('path/to/file.txt', 'Hello World!')
        storage.delete('path/to/file.txt')
        assert_false(storage.exists('path/to/file.txt'))
