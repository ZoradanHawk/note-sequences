author = 'Thomas Grossi'
version = '0.3'

import random

from midi_IO import input_midi_chords
from transitions import TransitionMatrix
from sections import Section, TransitionSection


class NoteSequence(object):
    def __init__(self, notes, structure, mapping, section, transition):
        self.matrix = TransitionMatrix(numbers=notes)
        self.total_length = ((section * len(structure)) +
                            (transition * (len(structure) - 1)))
        self.get_note = self.note_generator(initial_note=random.choice(notes),
                                            length=self.total_length,
                                            matrix=self.matrix)
        self.data = self.create_sequence(structure, mapping, section,
                                             transition)

    @staticmethod
    def note_generator(initial_note, matrix, length):
        '''Starting from *initial_note*, generates *length*
        notes based on the choices and probabilities
        specified in *matrix*. '''
        note = initial_note
        for i in range(length):
            rand = random.random()
            for pos, num in enumerate(matrix[note].probs):
                if rand < num:
                    note = matrix[note].choices[pos]
                    break
            yield note

    def create_sequence(self, structure, mapping, section, transition):
        '''Builds a sequence with section structure *structure*, where
        conversion of notes or chords from one section to the next are
        defined in *mapping*. Arguments *section* and *transition*
        refer to the lengths (in notes) of normal and transition
        sections within the sequence. Returns a list.'''
        sequence = []
        for i, letter in enumerate(structure):
            section = Section(generator=self.get_note,
                              length=section,
                              mapping=mapping,
                              section_letter=letter).create_section()
            sequence.extend(section)
            try:
                next_letter = structure[i + 1]
                ascend = letter < next_letter
                section = TransitionSection(generator=self.get_note,
                                            length=transition,
                                            mapping=mapping,
                                            first=letter,
                                            second=next_letter,
                                            ascend=ascend).transition_section()
                sequence.extend(section)
            except IndexError:
                pass
        return sequence

    def __iter__(self):
        for note in self.data:
            yield note

    def __getitem__(self, number):
        return self.data[number]

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self.data)


def main():
    chords = input_midi_chords('chord_test.mid')
    chord_mapping = {'A': list(set(chords)),
               'B': [tuple(x + 7 for x in e) for e in list(set(chords))],
               'C': [tuple(x + 12 for x in e) for e in list(set(chords))]}
    seq = NoteSequence(chords, 'ABACA', chord_mapping, 200, 200)
    print(seq)


if __name__ == '__main__':
    main()
