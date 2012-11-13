from os import environ, path, popen
from subprocess import Popen, PIPE

from django.conf import settings
from django.contrib.staticfiles.finders import find

class SassError(Exception):
    def __init__(self, stacktrace):
        self.stacktrace = stacktrace.split('\n')
        self.message    = self._message()

    def __str__(self):
        return repr(self.message)

    def _message(self):
        trace = [line.strip() for line in self.stacktrace]
        return ' '.join(trace[:2])


class SassProcessor(object):
    sass_functions = path.abspath(path.join(path.dirname(__file__), 'scripts/sass_functions.rb'))
    sass_load_path_dirs = ('css', 'style', 'styles', 'stylesheets')

    def __init__(self, file):
        self.file = file

    def process(self):
        env = dict(environ)
        env.update({
            'SASSPATH': ':'.join(self.get_load_paths()),
            'DJANGO_STATIC_URL': settings.STATIC_URL,
        })

        command = 'scss --require {0} {1}'.format(
            sh_quote(self.sass_functions),
            sh_quote(self.file),
        )

        process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, env=env)
        result = process.communicate()
        if process.returncode:
            raise SassError(result[1])
        else:
            return result[0]

    def get_load_paths(self):
        load_paths = []
        for dir in self.sass_load_path_dirs:
            load_paths += find(dir, all=True) or []
        return load_paths

def sh_quote(s):
    return "'{0}'".format(s.replace("'", "'\\''"))
