import random
from transitions import TransitionMatrix
from section_builder import NormalSection, TransitionSection


class NoteSequence():
    def __init__(self, initial_notes, structure, mapping, lengths=(400, 400)):
        self.matrix = TransitionMatrix(initial_notes)
        self.structure = structure
        self.map = mapping
        self.section_length = lengths[0]
        self.transition_length = lengths[1]
        self.total_length = (self.section_length * len(self.structure)) + (
                     self.transition_length * (len(self.structure) - 1))
        self.get_note = self.note_generator(random.choice(initial_notes))
        self.sequence = self.create_sequence()

    def note_generator(self, note):
        for i in range(self.total_length):
            rand = random.random()
            for pos, num in enumerate(self.matrix[note].probs):
                if rand < num:
                    note = self.matrix[note].choices[pos]
                    break
            yield note

    def create_sequence(self):
        sequence = []
        for i, letter in enumerate(self.structure):
            section = NormalSection(self.get_note, self.transition_length,
                                    self.map, letter).section
            sequence.extend(section)
            try:
                next_letter = self.structure[i + 1]
                ascend = letter < next_letter
                section = TransitionSection(self.get_note, self.section_length,
                                            self.map, letter, next_letter,
                                            ascend=ascend).section
                sequence.extend(section)
            except IndexError:
                pass
        return sequence

notes = [1, 2, 3, 2, 3, 2, 1, 2, 3, 1]

new_map = {'A': notes,
           'B': [n + 7 for n in notes],
           'C': [n + 12 for n in notes]}

# a = NoteSequence(notes, 'ABA', new_map, (200, 200))