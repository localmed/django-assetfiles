import os

from django.contrib.staticfiles.management.commands import collectstatic

class Command(collectstatic.Command):
    def copy_file(self, path, prefixed_path, source_storage):
        """
        Attempt to copy ``path`` with storage.
        """
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
            if source_path.endswith('.scss'):
                _, file_name = os.path.split(source_path)
                if file_name.startswith('_'): return

                self.log("Processing '%s'" % source_path, level=1)
                from assetfiles.processors import SassProcessor
                from assetfiles.storage import TempFilesStorage

                prefixed_path = prefixed_path.replace('.scss', '.css')
                css = SassProcessor(source_path).process()
                source_storage = TempFilesStorage()
                source_storage.save(path, css)

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
