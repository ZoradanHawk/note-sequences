import random
import collections
import debug_toolkit as debug


@debug.create_transition_matrix
def create_transition_matrix(melody):
    '''Takes a list of note values and returns a dictionary detailing
    which values follow each unique value, and with what probability.
    Probabilities ar formatted in a cumulative way, for example four
    note values with probabilities [0.2, 0.4, 0.2, 0.2] will be shown
    as [(n1, 0.2), (n2, 0.6), (n3, 0.8), (n4, 1.0)]. This allows to
    choose one of the values by cycling through the list.'''
    matrix = {}
    mp = lambda a: [sum(a[i] for i in range(j)) for j in range(1, len(a) + 1)]
    pair_counter = collections.Counter(zip(melody[:-1], melody[1:]))
    for note in set(melody):
        subset = [item for item in pair_counter.items() if item[0][0] == note]
        choices = [pair[1] for pair, count in sorted(subset)]
        total_count = sum(count for pair, count in sorted(subset))
        probs = [count / float(total_count) for pair, count in sorted(subset)]
        matrix[note] = list(zip(choices, mp(probs)))
    return matrix


class Section(object):
    '''A Section consists of note values extracted from *generator*,
    converted to their *section* equivalent.'''
    @debug.section_init
    def __init__(self, generator, length, mapping, section):
        self.generator = generator
        self.length = length
        self.map = mapping
        self.section = section
        self.data = self.create_section()

    def _convert_to_section(self, note_value, section):
        '''Takes a note value and converts it to its value within
         *section* as specified in *mapping*.'''
        index = self.map['A'].index(note_value)
        return self.map[section][index]

    def create_section(self):
        '''Builds the section by calling the instance generator
        and converting the note values to the correct section
         (entry within the instance map).'''
        for i in range(self.length):
            note = next(self.generator)
            note = Section._convert_to_section(self, note, self.section)
            yield note

    def __iter__(self):
        for note in self.data:
            yield note


class Transition(Section):
    '''A Transition consists of note values extracted from *generator*,
    converted either to their *section* or *next_section* equivalent.'''
    @debug.transition_init
    def __init__(self, generator, length, mapping, section, next_section):
        self.next_section = next_section
        self.ascending = section < next_section
        self.probability = 0.0 if self.ascending else 1.0
        Section.__init__(self, generator, length, mapping, section)

    def create_section(self):
        '''Builds the transition between *section* and *next_section*.
        The probability of turning to next_section notes increases if
        *first_section* is lower than *next_section*, decreases otherwise.'''
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
        '''Increases the instance probability by a
        fraction proportional to instance length.'''
        self.probability += 1 / float(self.length)

    def _decrease_probability(self):
        '''Decreases the instance probability by a
        fraction proportional to instance length.'''
        self.probability -= 1 / float(self.length)


def flatten_sequence(sequence):
    final = []
    for group in sequence:
        final.extend(group)
    return final


def group_by_pitch(sequence):
    final = []
    group = []
    for i, note in enumerate(sequence[:-1]):
        next_note = sequence[i + 1]
        if note == next_note:
            group.append(note)
        else:
            final.append(tuple(group + [note]))
            group = []
    group.append(sequence[-1])
    final.append(tuple(group))
    return final


def group_by_pauses(sequence):
    final = []
    group = []
    for i, note in enumerate(sequence[:-1]):
        next_note = sequence[i + 1]
        if note == (5,):
            group.append(note)
        elif next_note == (5,):
            final.append(tuple(group) + (note,))
            group = []
        else:
            group.append(note)
    group.append(sequence[-1])
    final.append(tuple(group))
    return final
