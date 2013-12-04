from django.conf import settings
from django.core.files.base import File, ContentFile
from django.core.files.storage import Storage
from django.utils.encoding import filepath_to_uri, force_text
from django.utils import six


class TempFilesStorage(Storage):
    """
    TempFilesStorage is an in-memory storage of files and file-like strings.

    This is used to temporarily hold processed files before they're copied
    to a new storage during `collectstatic`
    """

    def __init__(self):
        self.files = {}

    def _open(self, name, mode='rb'):
        if not self.exists(name):
            raise IOError('No such file in TempFilesStorage: {0}'.format(name))
        file = self.files[name]

        if isinstance(file, six.string_types) or isinstance(file, six.binary_type):
            file = ContentFile(file, name)
        elif not isinstance(file, File):
            file = File(file)

        return file

    def save(self, name, content):
        name = self.get_available_name(name)
        self.files[name] = content

        # Store filenames with forward slashes, even on Windows
        return force_text(name.replace('\\', '/'))

    def delete(self, name):
        del self.files[name]

    def exists(self, name):
        return name in self.files
