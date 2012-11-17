from django.test import TestCase
from django.utils import six

from assetfiles.storage import TempFilesStorage


class TestTempFilesStorage(TestCase):
    def test_stores_in_memory(self):
        storage = TempFilesStorage()
        storage.save('path/to/file.txt', 'Hello World!')
        self.assertTrue(storage.exists('path/to/file.txt'))

    def test_opens_strings_as_content_files(self):
        storage = TempFilesStorage()
        storage.save('path/to/file.txt', 'Hello World!')
        file = storage.open('path/to/file.txt')
        self.assertEquals('Hello World!', ''.join(file.chunks()))

    def test_deletes_storage(self):
        storage = TempFilesStorage()
        storage.save('path/to/file.txt', 'Hello World!')
        storage.delete('path/to/file.txt')
        self.assertFalse(storage.exists('path/to/file.txt'))
