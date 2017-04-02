import random
import collections
import debug_toolkit as debug


@debug.create_transition_matrix
def create_transition_matrix(numbers):
    '''Takes a list of integers (note values) or tuples
    (chords) and returns a dictionary detailing which values
    follow each unique value, and with what probability.
    E.g. if input is [1, 2, 1, 3, 1] the dictionary will show
    {1: [(2, 0.5), (3, 1.0)], 2: [(1, 1.0)], 3: [(1, 1.0)]}'''
    matrix = {}
    mp = lambda a: [sum(a[i] for i in range(j)) for j in range(1, len(a) + 1)]
    pair_counter = collections.Counter(zip(numbers[:-1], numbers[1:]))
    for note in set(numbers):
        subset = [item for item in pair_counter.items() if item[0][0] == note]
        choices = [key[1] for key, value in sorted(subset)]
        total = sum(value for key, value in sorted(subset))
        probs = [value / float(total) for key, value in sorted(subset)]
        matrix[note] = list(zip(choices, mp(probs)))
    return matrix


class Section(object):
    '''A Section can create *length* notes or chords extracted from *generator*,
    converted to their *section* equivalent using *mapping* as reference.'''
    @debug.section_init
    def __init__(self, generator, length, mapping, section):
        self.generator = generator
        self.length = length
        self.map = mapping
        self.section = section

    def _convert_to_section(self, note, section):
        '''Takes a musical unit *element* (note or chord)
        and converts it to its value in *section* as specified
        in *mapping*.'''
        index = self.map['A'].index(note)
        return self.map[section][index]

    def create_section(self):
        '''Builds section *section*, as a list of notes or chords.'''
        for i in range(self.length):
            note = next(self.generator)
            note = Section._convert_to_section(self, note, self.section)
            yield note

    def __iter__(self):
        for i in self.create_section():
            yield i


class Transition(Section):
    '''A Transition can create *length* notes or chords, extracted from
    *generator*. Using *mapping* as a reference, it the notes are converted
    to their *second* equivalent, with increasing probability if
    *first* is lower than *second*, or decreasing probability otherwise.'''
    @debug.transition_init
    def __init__(self, generator, length, mapping, section, next_section):
        Section.__init__(self, generator, length, mapping, section)
        self.next_section = next_section
        self.ascending = section < next_section
        self.probability = 0.0 if self.ascending else 1.0

    def create_transition(self):
        '''Builds the transition between *section*
        and *next_section*, as a list of notes or chords.'''
        if self.ascending:
            lower, higher = self.section, self.next_section
            update_probability = self._increase_probability
        else:
            lower, higher = self.next_section, self.section
            update_probability = self._decrease_probability
        for i in range(self.length):
            note = next(self.generator)
            if random.random() < self.probability:
                note = Section._convert_to_section(self, note, section=higher)
            else:
                note = Section._convert_to_section(self, note, section=lower)
            update_probability()
            yield note

    def _increase_probability(self):
        '''Increases the probability instance variable by a
        fraction proportional to transition length.'''
        self.probability += 1 / float(self.length)

    def _decrease_probability(self):
        '''Decreases the probability instance variable by a
        fraction proportional to transition length.'''
        self.probability -= 1 / float(self.length)

    def __iter__(self):
        for i in self.create_transition():
            yield i
