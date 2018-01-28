'''Contains sequence classes, which take lists of note values
and re-elaborate them in various ways.'''

import random
import sequence_toolkit as toolkit
import debug_toolkit as debug
from mapping_toolkit import read_map_file as read_map


class Sequence(object):

    @debug.sequence_init
    def __init__(self, melody, length):
        '''Main class. Takes a list of note values and builds a
        new one with the same probability of transitioning from
        one note to the next.'''
        self.melody = melody
        self.total_length = length
        self.data = self.create_sequence()

    @staticmethod
    def note_generator(melody, length):
        '''Builds a transition matrix of note values
        within *melody* and generates *length* values.'''
        note = random.choice(melody)
        matrix = toolkit.create_transition_matrix(melody)
        for i in range(length):
            if not matrix[note]:
                note = max(matrix, key=lambda x: len(matrix[x]))
            rand = random.random()
            for possible_note, probability in matrix[note]:
                if rand < probability:
                    note = possible_note
                    break
            yield note

    def create_sequence(self):
        '''Calls note_generator. Returns the output list of note values.'''
        generator = self.note_generator(self.melody, self.total_length)
        return [next(generator) for _ in range(self.total_length)]

    def __iter__(self):
        for note in self.data:
            yield note

    def __str__(self):
        return str(self.data)

    def __len__(self):
        return self.total_length

    def __getitem__(self, number):
        return self.data[number]


class NoteSequence(Sequence):

    @debug.note_sequence_init
    def __init__(self, melody, map_filename):
        '''A Sequence with specific sections and optional transitions
        between sections. Allows for variation in harmony throughout
        the sequence. Requires a .txt map file (see mapping_toolkit.py)
        to specify a structure, mapping and section/transition lengths.'''
        self.structure, self.sections, self.transitions, self.map = read_map(
            map_filename)
        Sequence.__init__(self, melody, sum(self.sections + self.transitions))

    def create_sequence(self):
        '''Builds Section and Transition objects based on the order in
        *structure* and the lengths in *sections* and *transitions*.
        Returns a list of note values.'''
        sequence = []
        generator = Sequence.note_generator(self.melody, self.total_length)
        section_lengths = (length for length in self.sections)
        transition_lengths = (length for length in self.transitions)
        for i, letter in enumerate(self.structure):
            section = toolkit.Section(generator=generator,
                                      length=next(section_lengths),
                                      mapping=self.map,
                                      section=letter)
            for note in section:
                sequence.append(note)
            try:
                next_section = self.structure[i + 1]
                transition = toolkit.Transition(generator=generator,
                                             length=next(transition_lengths),
                                             mapping=self.map,
                                             section=letter,
                                             next_section=next_section)
                for note in transition:
                    sequence.append(note)
            except IndexError:
                pass
        return sequence


class SparseSequence(Sequence):

    def __init__(self, melody, length, increasing=True):
        '''A Sequence with a flag value to be turned into pauses within
        Sibelius or MuseScore. Pause value is prevalent early in the
        sequence, nonexistent towards the end.'''
        self.increasing = increasing
        Sequence.__init__(self, melody, length)

    def create_sequence(self):
        '''Calls the note generator to build the output sequence.'''
        sequence = []
        generator = Sequence.note_generator(self.melody, self.total_length)
        for i in range(self.total_length):
            prob = self._update_probability(i)
            if random.random() < prob:
                sequence.append(next(generator))
            else:
                sequence.append((5,))
        return sequence

    def _update_probability(self, i):
        if self.increasing:
            return i / float(self.total_length)
        else:
            return 1 - (i / float(self.total_length))


class ChordSequence(NoteSequence):
    @debug.chord_sequence_init
    def __init__(self, melody, map_filename, chord_increase=1):
        '''A NoteSequence that allows for gradual building of
        chords within the sequence. Adds notes from the same
        section values based on random chance.'''
        self.chord_increase = chord_increase
        NoteSequence.__init__(self, melody, map_filename)

    def _update(self, note_value, prob, note_set):
        '''A NoteSequence that allows for gradual building of
        chords within the sequence. Adds notes from the same
        section values based on random chance. Argument chord_
        _increase determines the maximum number of notes added.'''
        for _ in range(self.chord_increase):
            if random.random() < prob:
                note_set = [n for n in note_set if n[0] not in note_value]
                note_value += random.choice(note_set) if note_set else ()
        return note_value

    def create_sequence(self):
        '''Calls the note generator to build the sequence, has an
        ever increasing change of updating each note to a longer chord.
        Returns the new list of values.'''
        sequence = []
        generator = Sequence.note_generator(self.melody, self.total_length)
        section_lengths = (length for length in self.sections)
        transition_lengths = (length for length in self.transitions)
        prob = 0.0
        for i, letter in enumerate(self.structure):
            note_set = self.map[letter]
            section = toolkit.Section(generator=generator,
                                      length=next(section_lengths),
                                      mapping=self.map,
                                      section=letter)
            for note in section:
                sequence.append(self._update(note, prob, note_set))
                prob += 1 / float(self.total_length)
            try:
                next_section = self.structure[i + 1]
                note_set = self.map[letter] + self.map[self.structure[i + 1]]
                transition = toolkit.Transition(generator=generator,
                                             length=next(transition_lengths),
                                             mapping=self.map,
                                             section=letter,
                                             next_section=next_section)
                for note in transition:
                    sequence.append(self._update(note, prob, note_set))
                    prob += 1 / float(self.total_length)
            except IndexError:
                pass
        return sequence


class GroupedSequence(Sequence):

    def __init__(self, melody, length):
        Sequence.__init__(self, toolkit.group_by_pitch(melody), length)
        self.grouped_by_pitch = toolkit.flatten_sequence(self.data)
        Sequence.__init__(self, toolkit.group_by_pauses(melody), length)
        self.grouped_by_pauses = toolkit.flatten_sequence(self.data)

