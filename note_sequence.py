import random
import sequence_toolkit as toolkit
import debug_toolkit as debug
import mapping_toolkit as mappings


class Sequence(object):

    @debug.sequence_init
    def __init__(self, melody, length):
        self.melody = melody
        self.total_length = length
        self.data = self.create_sequence()

    @staticmethod
    def note_generator(melody, length):
        '''Starting from *initial_note*, generates *length*
        notes based on the choices and probabilities
        specified in *matrix*. '''
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
        generator = self.note_generator(self.melody, self.total_length)
        return [next(generator) for _ in range(self.total_length)]

    def __iter__(self):
        for note in self.data:
            yield note

    def __str__(self):
        return str(list(self.data))

    def __len__(self):
        return self.total_length

    def __getitem__(self, number):
        return self.data[number]


class NoteSequence(Sequence):

    @debug.note_sequence_init
    def __init__(self, melody, map_filename):
        self.structure, self.map, self.sections,
        self.transitions = mappings.read_map_file(map_filename)
        Sequence.__init__(self, melody, sum(self.sections + self.transitions))

    def create_sequence(self):
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
    def __init__(self, melody, length, pause_value=61):
        self.pause_value = pause_value
        Sequence.__init__(self, melody, length)

    def create_sequence(self):
        sequence = []
        generator = Sequence.note_generator(self.melody, self.total_length)
        for i in range(self.total_length):
            prob = i / float(self.total_length)
            if random.random() < prob:
                sequence.append(next(generator))
            else:
                sequence.append((self.pause_value,))
        return sequence


class ChordSequence(NoteSequence):
    def __init__(self, melody, map_filename, chord_increase=1):
        self.chord_increase = chord_increase
        NoteSequence.__init__(self, melody, map_filename)

    def _update(self, note, prob, note_set):
        for _ in range(self.chord_increase):
            if random.random() < prob:
                note_set = [o for o in note_set if o[0] not in note]
                note += random.choice(note_set) if note_set else ()
        return note

    def create_sequence(self):
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
