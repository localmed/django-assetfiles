class FilterError(Exception):
    pass


class SassFilterError(FilterError):
    pass


class CoffeeScriptFilterError(FilterError):
    pass
