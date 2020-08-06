from .classes._Number_Struct import _Number_Struct, _Convert
from .classes._Character_Struct import _Character_Struct
from .classes.error_checks._Encrypt_Cases import _verify_sequence_pattern


def _generate_values(string, base, func, *args, **kwargs):
    for step in range(len(string)):
        number = _Number_Struct(func(step, *args, **kwargs), base)._value
        character = _Character_Struct(string[step])._char
        yield character, number


def _assign_values_from_generator(generator):
    return_values = {}
    for i in generator:
        return_values[i[0]] = i[1]
    _verify_sequence_pattern(return_values)
    return return_values


def _assign_values_from_list(a: list, b: list):
    return_values = {}
    for i in range(min([len(a), len(b)])):
        return_values[a[i]] = b[i]
    return return_values


def _extract_prefix(base):
    if type(base) == int:
        return _Convert._supported_types[int](base)
    return _Convert._supported_types[base](base)


def _extract_from_index(pattern: dict, index):
    return f"{list(pattern.values())[index]}"


def default(step: int):
    return step


class _Assignment_Handler:

    def __init__(self, string: str, base: any, func=default, *args, **kwargs):
        generator = _generate_values(string, base, func, *args, **kwargs)
        self.__pattern = _assign_values_from_generator(generator)
        self.__first = _extract_from_index(self.__pattern, 0)
        self.__last = _extract_from_index(self.__pattern, -1)
        self.__prefix = _extract_prefix(base)

    def __repr__(self):
        return f"({self.__first},...,{self.__last})"

    def __len__(self):
        return len(self.__pattern)

    def __add__(self, other):
        temp_keys = self.sequence._keys + other.sequence._keys
        temp_values = self.sequence._values + other.sequence._values
        self.__pattern = _assign_values_from_list(temp_keys, temp_values)
        self.__prefix += f'|{other.__prefix}'
        return self

    @property
    def prefix(self):
        return self.__prefix

    @property
    def sequence(self):
        return self.__Sequence(self.__pattern)

    class __Sequence:

        def __init__(self, sequence: dict):
            self.__sequence = sequence
            self.__keys = list(sequence.keys())
            self.__values = list(sequence.values())

        def __iter__(self):
            return iter(self.__sequence)

        @property
        def _keys(self):
            return self.__keys

        @property
        def _values(self):
            return self.__values
        
        @property
        def _max_length(self):
            return max([len(x) for x in self.__values])
        
        @property
        def _min_length(self):
            return min([len(x) for x in self.__values])

        @property
        def from_keys(self):
            return _assign_values_from_list(self.__keys, self.__values)

        @property
        def from_values(self):
            return _assign_values_from_list(self.__values, self.__keys)
