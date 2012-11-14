import re

class BaseFilter(object):
    input_exts = ()
    output_ext = None

    def matches_input(self, intput_path):
        if self.input_exts:
            return re.search(r'\.({0})$'.format('|'.join(self.input_exts)), intput_path)
        return False

    def matches_output(self, output_path):
        if self.output_ext:
            return re.search(r'\.{0}$'.format(self.output_ext), output_path)
        return False

    def possible_input_paths(self, output_path):
        paths = set()
        if self.input_exts:
            for ext in self.input_exts:
                ext = '.' + ext
                paths.add(output_path + ext)
                paths.add(re.sub(r'\..*$', ext, output_path))
        return paths

    def output_path(self, input_path):
        if self.output_ext:
            ext = '.' + self.output_ext
            return re.sub(r'\..*$', ext, input_path)
        return None

    def skip_output_path(self, output_path):
        return False

    def filter(self, input):
        raise NotImplementedError()
