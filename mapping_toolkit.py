from midi_toolkit import read_melody


def build_mapping(midi_files):
    data = {}
    for i, file_name in enumerate(midi_files):
        section_letter = chr(i + 65)
        section_values = create_ordered_set(read_melody(file_name)[0])  # only takes first track
        data[section_letter] = section_values
    return data


def create_ordered_set(sequence):
    
    '''Creates a list containing each unique element
    of input sequence, preserving order of appearance.'''
    
    final = []
    for item in sequence:
        if item not in final:
            final.append(item)
    return final


def read_map_file(filename):
    
    '''Takes a mapping .txt file, reads in information about structure,
    mapping, section lengths and transition lengths from it.
    NB. Mapping file must follow the template format. Create a Map object
    and use the *write_map_file* method to generate a suitable file, or run
    *mapping_toolkit.py* after changing the settings of its *main* function.
    You will need a list of midi files, which correspond to the sections, and 
    a structure.'''
    
    with open(filename, 'r') as f:
        output = []
        for line in f.readlines():
            if line.startswith('#'):
                continue
            if line.endswith('\n'):
                line = line[:-1]
            output.append(eval(line.split(' = ')[1]))
    map_data = debug_read_map_file(*tuple(output))
    return map_data


class Map(object):

    def __init__(self, structure, sections, transitions, mapping):
        self.structure = structure
        self.sections = sections
        self.transitions = transitions
        self.length = sum(sections + transitions)
        self.mapping = mapping

    @classmethod
    def from_midi_files(cls, midi_files, structure):
        midi_files, structure = debug_from_midi_files(midi_files, structure)
        sections = [16] * len(structure)
        transitions = [8] * (len(structure) - 1)
        mapping = build_mapping(midi_files)
        return cls(structure, sections, transitions, mapping)

    @classmethod
    def from_map_file(cls, filename):
        data = read_map_file(filename)
        return cls(*data)

    def write_map_file(self, output_file='Nameless_Map.txt'):
        with open(output_file, 'w') as f:
            f.write('structure = "{0}"\n# Length of sections (in number'
                    ' of notes):\nsections = {1}\n# Length of '
                    'transitions between sections (in number of notes):\n'
                    'transitions = {2}\ntotal_length = {3}\nmapping = {4}'
                    .format(self.structure, self.sections, self.transitions,
                            self.length, self.mapping))

    def __iter__(self):
        return (var for var in (self.structure, self.sections, self.transitions,
                            self.mapping))

    def __str__(self):
        return '''Map object. Structure: {}, Section Lengths: {}, Transition
               Lengths: {}, Mapping: {}.'''.format(
                self.structure, self.sections, self.transitions, self.mapping)

    def __repr__(self):
        return '''Map object. Structure: {}, Section Lengths: {}, Transition
               Lengths: {}, Mapping: {}.'''.format(
                self.structure, self.sections, self.transitions, self.mapping)


# Debugger functions

def debug_read_map_file(structure, sections, transitions, length, mapping):
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


def debug_from_midi_files(midi_files, structure):
    for filename in midi_files:
        if filename[-4:] != '.mid':
            raise ValueError('*midi_files* must contain midi file names!')
    if 'A' not in structure:
        raise ValueError('Structure must contain character "A".')
    letters = set([chr(i) for i in range(65, 65 + len(midi_files))])
    if set(structure) != letters:
        raise ValueError('Invalid structure: {}. Must be based on {}'.
                         format(structure, letters))
    return midi_files, structure


def main():
    data = Map.from_midi_files(midi_files=['1Prime.mid', '2Prime.mid', '4Prime.mid', '5Prime.mid'],
                               structure='ABABCDABA')
    data.write_map_file('Map10.txt')
    
if __name__ == '__main__':
    main()
