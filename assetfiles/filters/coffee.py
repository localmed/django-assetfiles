from assetfiles import settings
from assetfiles.filters import BaseFilter, CommandMixin, ExtensionMixin
from assetfiles.exceptions import CoffeeScriptFilterError


class CoffeeScriptFilter(ExtensionMixin, CommandMixin, BaseFilter):
    """
    Filters CoffeeScript files into JS.
    """
    input_ext = 'coffee'
    output_ext = 'js'
    coffee_path = 'coffee'

    def __init__(self, options=None, *args, **kwargs):
        super(CoffeeScriptFilter, self).__init__(*args, **kwargs)
        if options is None:
            options = {}

        coffee_options = settings.COFFEE_SCRIPT_OPTIONS

        self.coffee_path = options.get(
            'coffee_path',
            coffee_options.get('coffee_path', self.coffee_path)
        )
        if 'bare' not in options:
            options['bare'] = coffee_options.get('bare')

        self.options = options

    def filter(self, input):
        command = '{command} {args} {input}'.format(
            command=self.coffee_path,
            args=self._build_args(),
            input=self.format_option('print', input),
        )

        return self.run_command(command,
                                exception_type=CoffeeScriptFilterError)

    def _build_args(self):
        args = []

        if self.options['bare']:
            args.append(self.format_option_name('bare'))
        args.append(self.format_option_name('compile'))

        return ' '.join(args)
