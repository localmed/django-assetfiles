import os

from django.contrib.staticfiles.management.commands import collectstatic

from assetfiles import filters


class Command(collectstatic.Command):
    """
    Overrides staticfiles' `collectstatic` command to filter files before
    copying them to the target storage.
    """

    def copy_file(self, path, prefixed_path, source_storage):
        # Skip this file if it was already copied earlier
        if prefixed_path in self.copied_files:
            return self.log("Skipping '%s' (already copied earlier)" % path)
        # Delete the target file if needed or break
        if not self.delete_file(path, prefixed_path, source_storage):
            return
        # The full path of the source file
        source_path = source_storage.path(path)
        # Finally start copying
        if self.dry_run:
            self.log("Pretending to copy '%s'" % source_path, level=1)
        else:
            filter = filters.find_by_input_path(source_path)
            if filter:
                if filter.skip_output_path(prefixed_path): return

                self.log("Processing '%s'" % source_path, level=1)
                from assetfiles.storage import TempFilesStorage

                prefixed_path = filter.output_path(prefixed_path)
                content = filter.filter(source_path)
                source_storage = TempFilesStorage()
                source_storage.save(path, content)

            self.log("Copying '%s'" % source_path, level=1)
            if self.local:
                full_path = self.storage.path(prefixed_path)
                try:
                    os.makedirs(os.path.dirname(full_path))
                except OSError:
                    pass
            with source_storage.open(path) as source_file:
                self.storage.save(prefixed_path, source_file)
        if not prefixed_path in self.copied_files:
            self.copied_files.append(prefixed_path)
