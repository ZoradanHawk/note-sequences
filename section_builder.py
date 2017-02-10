import random


class Section():
    def __init__(self, generator, length, mapping):
        self.note_generator = generator
        self.length = length
        self.map = mapping

    def convert_to_section(self, note, letter):
        '''Converts a note to its equivalent in section "letter". '''
        index = self.map['A'].index(note)
        return self.map[letter][index]


class NormalSection(Section):
    def __init__(self, generator, length, mapping, section_name):
        Section.__init__(self, generator, length, mapping)
        self.letter = section_name
        self.get_note = generator
        self.section = self.create_section()

    def create_section(self):
        '''Returns the section corresponding to "letter".'''
        section = []
        for i in range(self.length):
            note = next(self.get_note)
            note = self.convert_to_section(note, self.letter)
            section.append(note)
        return section


class TransitionSection(Section):
    def __init__(self, generator, length, mapping, first, second, ascend=True):
        Section.__init__(self, generator, length, mapping)
        self.get_note = generator
        self.section1 = first
        self.section2 = second
        self.ascend = ascend
        self.probability = 0.0 if self.ascend else 1.0
        self.section = self.create_section()

    def create_section(self):
        section = []
        if self.ascend:
            lower, higher = self.section1, self.section2
            update_prob = self.increase_probability
        else:
            lower, higher = self.section2, self.section1
            update_prob = self.decrease_probability
        for i in range(self.length):
            note = next(self.get_note)
            if random.random() < self.probability:
                note = self.convert_to_section(note, higher)
            else:
                note = self.convert_to_section(note, lower)
            update_prob()
            section.append(note)
        return section

    def increase_probability(self):
        self.probability += 1 / float(self.length)

    def decrease_probability(self):
        self.probability -= 1 / float(self.length)