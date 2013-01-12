import os

from django.contrib.staticfiles.management.commands import collectstatic

from assetfiles import filters


class Command(collectstatic.Command):
    """
    Overrides staticfiles' `collectstatic` command to filter files before
    copying them to the target storage.
    """

    def copy_file(self, path, prefixed_path, source_storage):
        if prefixed_path in self.copied_files:
            return self.log("Skipping '%s' (already copied earlier)" % path)
        if not self.delete_file(path, prefixed_path, source_storage):
            return

        source_path = source_storage.path(path)
        target_path = prefixed_path

        filter = filters.find_by_input_path(prefixed_path)
        if filter:
            if not filter.is_filterable(prefixed_path):
                return self.log("Skipping '%s' (filter dependency)" % path)
            target_path, source_storage = self._filter_file(filter, path, prefixed_path, source_path, source_storage)

        self._copy_file(path, target_path, source_path, source_storage)
        if not prefixed_path in self.copied_files:
            self.copied_files.append(prefixed_path)

    def _filter_file(self, filter, path, prefixed_path, source_path, source_storage):
        from assetfiles.storage import TempFilesStorage
        target_path = filter.derive_output_path(prefixed_path)
        if self.dry_run:
            self.log("Pretending to process '%s'" % source_path, level=1)
        else:
            self.log("Processing '%s'" % source_path, level=1)
            content = filter.filter(source_path)
            source_storage = TempFilesStorage()
            source_storage.save(path, content)
        return (target_path, source_storage)

    def _copy_file(self, path, target_path, source_path, source_storage):
        if self.dry_run:
            self.log("Pretending to copy '%s'" % source_path, level=1)
        else:
            self.log("Copying '%s'" % source_path, level=1)
            with source_storage.open(path) as source_file:
                self._make_local_dirs(target_path)
                self.storage.save(target_path, source_file)

    def _make_local_dirs(self, target_path):
        if self.local:
            full_path = self.storage.path(target_path)
            try:
                os.makedirs(os.path.dirname(full_path))
            except OSError:
                pass
