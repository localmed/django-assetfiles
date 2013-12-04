import os

from django.contrib.staticfiles.management.commands import collectstatic
from django.contrib.staticfiles import finders
from django.core.management.base import CommandError
from django.utils.datastructures import SortedDict

from assetfiles import filters
from assetfiles.storage import TempFilesStorage


class Command(collectstatic.Command):
    """
    Overrides staticfiles' `collectstatic` command to filter files before
    copying them to the target storage.
    """
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.found_files = SortedDict()
        self.temp_storage = TempFilesStorage()

    def set_options(self, **options):
        super(Command, self).set_options(**options)
        if self.symlink:
            raise CommandError('Symlinking is not supported by Assetfiles.')

    def collect(self):
        if self.clear:
            self.clear_dir('')
        self._collect_files()
        if self.post_process and hasattr(self.storage, 'post_process'):
            self._post_process_files()

        return {
            'modified': self.copied_files,
            'unmodified': self.unmodified_files,
            'post_processed': self.post_processed_files,
        }

    def _collect_files(self):
        for path, prefixed_path, source_storage in self._full_file_list():
            if self._is_copied(prefixed_path):
                self.log("Skipping '%s' (already copied earlier)" % path)
            elif self.delete_file(path, prefixed_path, source_storage):
                path, prefixed_path, source_storage = self._collect_file(
                    path, prefixed_path, source_storage)
            self.found_files[prefixed_path] = (source_storage, path)

    def _post_process_files(self):
        processor = self.storage.post_process(self.found_files,
                                              dry_run=self.dry_run)
        for original_path, processed_path, processed in processor:
            if isinstance(processed, Exception):
                self.stderr.write("Post-processing '%s' failed!" % original_path)
                # Add a blank line before the traceback, otherwise it's
                # too easy to miss the relevant part of the error message.
                self.stderr.write('')
                raise processed
            if processed:
                self.log("Post-processed '%s' as '%s" %
                         (original_path, processed_path), level=1)
                self.post_processed_files.append(original_path)
            else:
                self.log("Skipped post-processing '%s'" % original_path)

    def _collect_file(self, path, prefixed_path, source_storage):
        source_path = source_storage.path(path)
        target_path = prefixed_path
        filter = filters.find_by_input_path(prefixed_path)

        if filter and not filter.is_filterable(prefixed_path):
            self.log("Skipping '%s' (filter dependency)" % path)
        else:
            if filter:
                target_path, source_storage = self._filter_file(
                    filter, prefixed_path, source_path, source_storage)
            self._copy_file(source_path, target_path, source_storage)
            if not prefixed_path in self.copied_files:
                self.copied_files.append(prefixed_path)

        return (source_path, target_path, source_storage)

    def _filter_file(self, filter, prefixed_path, source_path, source_storage):
        target_path = filter.derive_output_path(prefixed_path)
        if self.dry_run:
            self.log("Pretending to process '%s'" % source_path, level=1)
        else:
            self.log("Processing '%s'" % source_path, level=1)
            content = filter.filter(source_path)
            source_storage = self.temp_storage
            source_storage.save(source_path, content)

        return (target_path, source_storage)

    def _copy_file(self, source_path, target_path, source_storage):
        if self.dry_run:
            self.log("Pretending to copy '%s'" % source_path, level=1)
        else:
            self.log("Copying '%s'" % source_path, level=1)
            with source_storage.open(source_path) as source_file:
                self._make_local_dirs(target_path)
                self.storage.save(target_path, source_file)

    def _full_file_list(self):
        for finder in finders.get_finders():
            for path, source_storage in finder.list(self.ignore_patterns):
                prefixed_path = self._get_prefixed_path(path, source_storage)
                yield (path, prefixed_path, source_storage)

    def _get_prefixed_path(self, path, source_storage):
        if getattr(source_storage, 'prefix', None):
            prefixed_path = os.path.join(source_storage.prefix, path)
        else:
            prefixed_path = path
        return prefixed_path

    def _make_local_dirs(self, target_path):
        if self.local:
            full_path = self.storage.path(target_path)
            try:
                os.makedirs(os.path.dirname(full_path))
            except OSError:
                pass

    def _is_copied(self, file):
        return file in self.found_files or file in self.copied_files
