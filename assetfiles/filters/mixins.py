import os
import pipes
import re
from subprocess import Popen, PIPE

from django.utils import six

from assetfiles.exceptions import FilterError


class CommandMixin(object):
    def run_command(self, command, extra_env=None, exception_type=None):
        if not exception_type:
            exception_type = FilterError

        env = dict(os.environ)
        if extra_env:
            env.update(extra_env)

        process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, env=env)
        stdout, stderr = process.communicate()

        if process.returncode:
            raise exception_type(stderr)
        else:
            return stdout

    def format_option_array(self, name, values):
        if values:
            return [self.format_option(name, value) for value in values]
        else:
            return []

    def format_option(self, name, value):
        return '{name} {value}'.format(
            name=self.format_option_name(name),
            value=self.format_option_value(value),
        )

    def format_option_name(self, name):
        return '--{name}'.format(name=name.replace('_', '-'))

    def format_option_value(self, value):
        return pipes.quote(value) if value else ''


class GlobInputMixin(object):
    def __init__(self, input_path_glob, **kwargs):
        self.input_path_glob = input_path_glob

    def matches_input(self, input_path):
        from fnmatch import fnmatch

        return fnmatch(input_path, self.input_path_glob)

    def derive_input_paths(self, output_path):
        input_paths = []
        for root in self._get_staticfiles_roots():
            for path in self._iglob_within(root, self.input_path_glob):
                if path not in input_paths:
                    input_paths.append(path)
        return input_paths

    def _iglob_within(self, root, pathname):
        try:
            from glob2 import iglob
        except ImportError:
            from glob import iglob
        import os

        for path in iglob(os.path.join(root, pathname)):
            yield path.replace(root, '').lstrip('/')

    def _get_staticfiles_roots(self):
        for storages in self._get_staticfiles_storages():
            for root, storage in six.iteritems(storages):
                if hasattr(storage, 'location'):
                    yield storage.location

    def _get_staticfiles_storages(self):
        from django.contrib.staticfiles.finders import get_finders

        for finder in get_finders():
            if hasattr(finder, 'storages'):
                yield finder.storages


class ListInputMixin(object):
    def __init__(self, input_paths):
        self.input_paths = input_paths

    def matches_input(self, input_path):
        return input_path in self.input_paths

    def derive_input_paths(self, output_path):
        return list(self.input_paths)


class MultiInputMixin(object):
    def __init__(self, input_paths=None, *args, **kwargs):
        super(MultiInputMixin, self).__init__(*args, **kwargs)
        if isinstance(input_paths, str):
            self._multi_input_delegate = GlobInputMixin(input_path_glob=input_paths)
        else:
            self._multi_input_delegate = ListInputMixin(input_paths=input_paths)

    def _matches_input(self, input_path):
        return self._multi_input_delegate.matches_input(input_path)

    def _derive_input_paths(self, output_path):
        return self._multi_input_delegate.derive_input_paths(output_path)


class ExtensionMixin(object):
    """
    A mixin for filters that take a file with a certain file extension and
    output another.

    For example, SassFilter generally takes files with the exentions ".scss" and
    ".sass" and output CSS files (".css").

    Attributes:
        input_exts: A tuple of extensions (without the prefixed ".")
        output_ext: A single output extension (again, without the prefixed ".")
    """
    input_exts = None
    output_ext = None

    def __init__(self, input_ext=None, input_exts=None, output_ext=None, *args, **kwargs):
        super(ExtensionMixin, self).__init__(*args, **kwargs)
        if input_ext:
            self.input_ext = input_ext
        if input_exts:
            self.input_exts = input_exts
        if output_ext:
            self.output_ext = output_ext
        if not self.input_exts and self.input_ext:
            self.input_exts = (self.input_ext,)

    def _matches_input(self, intput_path):
        if self.input_exts:
            return re.search(r'\.({0})$'.format('|'.join(self.input_exts)), intput_path)
        return False

    def _matches_output(self, output_path):
        if self.output_ext:
            return re.search(r'\.{0}$'.format(self.output_ext), output_path)
        return False

    def _derive_input_paths(self, output_path):
        paths = []
        if self.input_exts:
            for ext in self.input_exts:
                ext = '.' + ext
                paths.append(output_path + ext)
                paths.append(re.sub(r'\.[^\.]*$', ext, output_path))
        return paths

    def _derive_output_path(self, input_path):
        if self.output_ext:
            path = re.sub(r'\.{0}'.format(self.output_ext), '', input_path)
            ext = '.' + self.output_ext
            return re.sub(r'\.[^\.]*$', ext, path)
        return None

    def set_input_ext(self, value):
        self.input_exts = (value,)
    input_ext = property(fset=set_input_ext)
