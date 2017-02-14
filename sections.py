import random


class Section(object):
    def __init__(self, generator, length, mapping, section_letter):
        self.generator = generator
        self.length = length
        self.map = mapping
        self.section_letter = section_letter

    @staticmethod
    def convert_to_section(element, mapping, section='A'):
        '''Takes a musical unit *element* (note or chord)
        and converts it to its value in *section* as specified
        in *mapping*.'''
        index = mapping['A'].index(element)
        return mapping[section][index]

    def create_section(self):
        '''Builds section *section_letter* by calling
        the generator and converting each generated element
        to the correct section.'''
        section = []
        for i in range(self.length):
            note = next(self.generator)
            note = Section.convert_to_section(element=note,
                                              mapping=self.map,
                                              section=self.section_letter)
            section.append(note)
        return section


class TransitionSection(Section):
    def __init__(self, generator, length, mapping, first, second, ascend=True):
        Section.__init__(self, generator, length, mapping, first)
        self.next_section = second
        self.ascend = ascend
        self.probability = 0.0 if ascend else 1.0

    def transition_section(self):
        '''Builds a transition section between section_letter
        and next_section by calling the generator and converting
        the notes to the highest section with increasing probability
        (if transitioning to a "higher" section) or decreasing
        probability (if transitioning to a "lower" section).'''
        section = []
        if self.ascend:
            lower, higher = self.section_letter, self.next_section
            update_prob = self.increase_probability
        else:
            lower, higher = self.section_letter, self.next_section
            update_prob = self.decrease_probability
        for i in range(self.length):
            note = next(self.generator)
            if random.random() < self.probability:
                note = Section.convert_to_section(element=note,
                                                  mapping=self.map,
                                                  section=higher)
            else:
                note = Section.convert_to_section(element=note,
                                                  mapping=self.map,
                                                  section=lower)
            update_prob()
            section.append(note)
        return section

    def increase_probability(self):
        '''Increases the probability instance variable by a
        fraction inversely proportional to transition length.'''
        self.probability += 1 / float(self.length)

    def decrease_probability(self):
        '''Decreases the probability instance variable by a
        fraction inversely proportional to transition length.'''
        self.probability -= 1 / float(self.length)
