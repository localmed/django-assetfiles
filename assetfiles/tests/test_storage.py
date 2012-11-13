from django.test import TestCase
from django.utils import six

from assetfiles.storage import TempFilesStorage

class TestTempFilesStorage(TestCase):
    def setUp(self):
        self.storage = TempFilesStorage()

    def test_stores_in_memory(self):
        self.storage.save('path/to/file.txt', 'Hello World!')
        self.assertTrue(self.storage.exists('path/to/file.txt'))

    def test_opens_strings_as_content_files(self):
        self.storage.save('path/to/file.txt', 'Hello World!')
        file = self.storage.open('path/to/file.txt')
        self.assertEquals('Hello World!', ''.join(file.chunks()))

    def test_deletes_storage(self):
        self.storage.save('path/to/file.txt', 'Hello World!')
        self.storage.delete('path/to/file.txt')
        self.assertFalse(self.storage.exists('path/to/file.txt'))
