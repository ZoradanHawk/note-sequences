'''Contains wrapper functions to check the arguments of several
functions in other modules (type checking etc.). Names of the wrappers
correspond to the function they are protecting.'''

import functools
import types


def sequence_init(function):
    @functools.wraps(function)
    def inner(self, melody, length):
        for note_value in melody:
            if not isinstance(note_value, tuple):
                raise ValueError('Invalid note: {}. Must be a tuple.'
                                .format(note_value))
        if not isinstance(length, int):
            raise TypeError('Invalid length: {}. Must be an integer.'
                            .format(length))
        if not length > 0:
            raise ValueError('Length must be larger than 0.')
        return function(self, melody, length)
    return inner


def note_sequence_init(function):
    @functools.wraps(function)
    def inner(self, melody, map_filename):
        if not isinstance(map_filename, str):
            raise TypeError('Invalid file name: {}. Must be a string.'
                            .format(map_filename))
        if map_filename[-4:] != '.txt':
            raise ValueError('Invalid file: {}. Map file must be a .txt map.'
                             .format(map_filename))
        return function(self, melody, map_filename)
    return inner


def chord_sequence_init(function):
    @functools.wraps(function)
    def inner(self, melody, map_filename, chord_increase=1):
        if not isinstance(chord_increase, int):
            raise TypeError('Invalid chord increase: {}. Must be an int.'
                            .format(chord_increase))
        if not chord_increase > 0:
            raise ValueError('Chord increase must be larger than 0.')
        return function(self, melody, map_filename, chord_increase)
    return inner


def check_note_value(note_value):
    if isinstance(note_value, int):
        return True
    elif isinstance(note_value, tuple):
        for note in note_value:
            check_note_value(note)
    else:
        raise TypeError('Invalid note value: {}. Must be tuple of integer/s.'
                        .format(note_value))


def create_transition_matrix(function):
    @functools.wraps(function)
    def inner(numbers):
        for note_value in numbers:
            check_note_value(note_value)
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


def create_map_file(function):
    @functools.wraps(function)
    def inner(map_files, structure, output_file):
        for filename in map_files:
            if filename[-4:] != '.mid':
                raise ValueError('*map_files* must contain midi file names!')
        if 'A' not in structure:
            raise ValueError('Structure must contain character "A".')
        letters = set([chr(i) for i in range(65, 65 + len(map_files))])
        if set(structure) != letters:
            raise ValueError('Invalid structure: {}. Must be based on {}'.
                             format(structure, letters))
        if output_file[-4:] != '.txt':
            raise ValueError('Invalid filename: {}. Must be .txt file.'
                             .format(output_file))
        return function(map_files, structure, output_file)
    return inner


def read_map_file(structure, sections, transitions, mapping):
    if not isinstance(structure, str):
            raise TypeError('Invalid structure: {}. Must be a string.'
                            .format(structure))
    if 'A' not in structure:
        raise ValueError('Structure must contain character "A"!')
    for value in mapping.values():
        if len(value) != len(list(mapping.values())[0]):
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
    return structure, sections, transitions, mapping
