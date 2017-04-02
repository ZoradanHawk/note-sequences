import functools
import types


def sequence_init(function):
    @functools.wraps(function)
    def inner(self, melody, length):
        if not isinstance(melody, list) and not isinstance(melody, tuple):
            raise TypeError('Invalid melody: {}. Must be a list or tuple.'
                            .format(melody))
        for note in melody:
            if not isinstance(note, tuple):
                raise ValueError('Invalid note: {}. Must be a tuple.'
                                .format(note))
        if not isinstance(length, int):
            raise TypeError('Invalid length; {}. Must be an integer.'
                            .format(length))
        if not length > 0:
            raise ValueError('Length must be larger than 0.')
        return function(self, melody, length)
    return inner


def note_sequence_init(function):
    @functools.wraps(function)
    def inner(self, melody, map_filename):
        if not isinstance(map_filename, str):
            raise TypeError('Invalid *map_filename*: {}. Must be a string.'
                            .format(map_filename))
        if map_filename[-4:] != '.txt':
            raise ValueError('Invalid file: {}. Map file must be a .txt map.'
                             'Use create_map_template to generate one.'
                             .format(map_filename))
        return function(self, melody, map_filename)
    return inner


def create_transition_matrix(function):
    @functools.wraps(function)
    def inner(numbers):
        if not isinstance(numbers, list) and not isinstance(numbers, tuple):
            raise TypeError('Invalid argument: {}. Must be a list or tuple.')
        for item in numbers:
            if isinstance(item, tuple):
                continue
            else:
                raise TypeError('Invalid item: {}. Must be int or tuple.'
                               .format(item))
        return function(numbers)
    return inner


def section_init(function):
    @functools.wraps(function)
    def inner(self, generator, length, mapping, section):
        if not isinstance(generator, types.GeneratorType):
            raise TypeError('Invalid arg: {}. Generator must be a generator.'
                            .format(generator))
        if not isinstance(length, int):
            raise TypeError('Invalid arg: {}. Length must be a number.'
                            .format(length))
        if not isinstance(mapping, dict):
            raise TypeError('Invalid arg: {}. Mapping must be a dictionary.'
                            .format(mapping))
        if section not in mapping:
            raise KeyError('Section letter must be an entry in mapping.')
        return function(self, generator, length, mapping, section)
    return inner


def transition_init(function):
    @functools.wraps(function)
    def inner(self, generator, length, mapping, section, next_section):
        if not isinstance(generator, types.GeneratorType):
            raise TypeError('Invalid arg: {}. Generator must be a generator.'
                            .format(generator))
        if not isinstance(length, int):
            raise TypeError('Invalid length: {}. Must be a number.'
                            .format(length))
        if not isinstance(mapping, dict):
            raise TypeError('Invalid mapping: {}. Must be a dictionary.'
                            .format(mapping))
        if section not in mapping:
            raise KeyError('Invalid section letter: {}. Must be in mapping.'
                           .format(section))
        if next_section not in mapping:
            raise KeyError('Invalid section letter: {}. Must be in mapping.'
                           .format(next_section))
        return function(self, generator, length, mapping, section, next_section)
    return inner


def create_map_template(function):
    @functools.wraps(function)
    def inner(output_filename, melody, structure, map_files):
        if output_filename[-4:] != '.txt':
            raise ValueError('Invalid filename: {}. Must be .txt file.'
                             .format(output_filename))
        if not isinstance(melody, list) and not isinstance(melody, tuple):
            raise TypeError('Invalid melody: {}. Must be a list or tuple.'
                            .format(melody))
        if not isinstance(structure, str):
            raise TypeError('Invalid structure: {}. Must be a string.'
                            .format(structure))
        if 'A' not in structure:
            raise ValueError('Structure must contain character "A"!')
        letters = set([chr(i) for i in range(66, 66 + len(map_files))] + ['A'])
        if set(structure) != letters:
            raise ValueError('Invalid structure: {}. Must be based on {}'.
                             format(structure, letters))
        for filename in map_files:
            if filename[-4:] != '.mid':
                raise ValueError('*map_files* must contain midi file names!')
        return function(output_filename, melody, structure, map_files)
    return inner


def read_map_file(structure, mapping, sections, transitions):
    if not isinstance(structure, str):
            raise TypeError('Invalid structure: {}. Must be a string.'
                            .format(structure))
    if 'A' not in structure:
        raise ValueError('Structure must contain character "A"!')
    for value in mapping.values():
        if len(value) != len(mapping.values()[0]):
            raise ValueError('Entries in *mapping* must have same length!')
    for letter in structure:
        if letter not in mapping.keys():
            raise ValueError('Every character in *structure* must be'
                             ' present in *mapping*!')
    if len(sections) != len(structure):
        raise ValueError('*sections* must contain a value for each'
                         ' letter in *structure*.')
    if transitions:
        if len(transitions) != len(sections) - 1:
            raise ValueError('Number of lengths in *transitions* must be '
                             'one less than lengths in *sections*.')
    else:
        transitions = [0] * (len(sections) - 1)
    return structure, mapping, sections, transitions