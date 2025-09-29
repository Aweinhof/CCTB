from enum import Enum


class Filter(Enum):
    CONTAIN = ''
    EXACT = '='
    REGEX = '~'
    NOT_CONTAIN = '!'
    NOT_EXACT = '!='
    NOT_REGEX = '!~'

    def __call__(self, message: str):
        return FilterValue(self, message)


class FilterValue:
    def __init__(self, filter: Filter, value: str):
        self.type = filter
        self.value = value
        self.text = f'filter={filter.value}{value}'
