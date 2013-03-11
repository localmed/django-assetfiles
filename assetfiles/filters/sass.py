from __future__ import unicode_literals

import os

from django.conf import settings
from django.contrib.staticfiles.finders import find

from assetfiles.filters import BaseFilter, CommandMixin, ExtensionMixin
import assetfiles.settings
from assetfiles.exceptions import SassFilterError


class SassFilter(ExtensionMixin, CommandMixin, BaseFilter):
    """
    Filters Sass files into CSS.

    Attributes:
        sass_path: The full path to the Sass command. This defaults to a
            customized binstub that allows for better Bundler integration.
        functions_path: The full path to the Sass extension functions for
            Django integration. Set to None or False to bypass adding
            these functions.
    """
    SCRIPTS_PATH = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../scripts'))

    input_exts = ('sass', 'scss')
    output_ext = 'css'
    sass_path = 'sass'
    sass_env_path = os.path.join(SCRIPTS_PATH, 'sass_env.rb')
    sass_functions_path = os.path.join(SCRIPTS_PATH, 'sass_functions.rb')

    def __init__(self, options=None, *args, **kwargs):
        super(SassFilter, self).__init__(*args, **kwargs)
        if options is None:
            options = {}

        sass_options = assetfiles.settings.SASS_OPTIONS

        self.sass_path = options.get(
            'sass_path',
            sass_options.get('sass_path', self.sass_path)
        )
        self.sass_env_path = options.get(
            'sass_env_path',
            sass_options.get('sass_env_path', self.sass_env_path)
        )
        self.sass_functions_path = options.get(
            'sass_functions_path',
            sass_options.get('sass_functions_path', self.sass_functions_path)
        )
        options['compass'] = options.get(
            'compass',
            sass_options.get('compass', self._detect_compass())
        )

        for option in ('style', 'precision', 'quiet', 'debug_info',
                       'line_numbers', 'cache_location', 'no_cache'):
            if option not in options:
                options[option] = sass_options.get(option)

        options['require'] = (
            sass_options.get('require', []) +
            options.get('require', [])
        )
        if self.sass_functions_path:
            options['require'].insert(0, self.sass_functions_path)
        if self.sass_env_path:
            options['require'].insert(0, self.sass_env_path)

        options['load_paths'] = (
            sass_load_paths +
            sass_options.get('load_paths', []) +
            options.get('load_paths', [])
        )

        self.options = options

    def filter(self, input):
        command = '{command} {args} {input}'.format(
            command=self.sass_path,
            args=self._build_args(),
            input=self.format_option_value(input),
        )

        return self.run_command(
            command,
            extra_env={'DJANGO_STATIC_URL': settings.STATIC_URL},
            exception_type=SassFilterError
        )

    def is_filterable(self, output_path):
        """
        Skips files prefixed with a '_'. These are Sass dependencies.
        """
        _, file_name = os.path.split(output_path)
        return not file_name.startswith('_')

    def _build_args(self):
        """
        Returns a list of arguments for the Sass command.
        """
        args = []

        args += self.format_option_array('require', self.options['require'])
        args += self.format_option_array('load_path', self.options['load_paths'])

        value_options = ('style', 'precision', 'cache_location')
        for option in value_options:
            if self.options[option]:
                args.append(self.format_option(option, self.options[option]))

        bool_options = ('quiet', 'compass', 'debug_info',
                        'line_numbers', 'no_cache')
        for option in bool_options:
            if self.options[option]:
                args.append(self.format_option_name(option))

        return ' '.join(args)

    def _detect_compass(self):
        """
        Returns true if Compass integration is available.
        """
        return os.system('which compass > /dev/null') is 0


def get_static_sass_dirs(dirs=None):
    """
    Returns the directories with Sass files within the static directories.

    Args:
        dirs: A list or tuple of directory names that contain Sass files.
            Can be configured with the ASSETFILES_SASS_DIRS setting, which by
            default is `('css',)`

    Returns:
        A list of directory paths containing Sass files.
    """
    if not dirs:
        dirs = assetfiles.settings.SASS_DIRS

    load_paths = []
    for dir in dirs:
        load_paths += find(dir, all=True) or []
    return load_paths


"""
Directories that will be added to the Sass load path.

By default, these are 'css' directories within the static directories.
"""
sass_load_paths = get_static_sass_dirs()
