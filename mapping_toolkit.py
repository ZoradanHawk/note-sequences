from midi_toolkit import midi_input
import debug_toolkit as debug


def create_ordered_set(sequence):
    '''Creates a list containing each unique element
    of input sequence, preserving order of appearance.'''
    final = []
    for item in sequence:
        if item not in final:
            final.append(item)
    return final


#@debug.create_map_file
def create_map_file(map_files, structure, output_file='Nameless_Map.txt'):
    '''Takes a list of midi file names, uses them to build a dictionary,
    mapping uppercase ascii letters to the ordered set of notes extracted from
    the files. Writes out a .txt file containing structure, a list of
    section and transition lengths (defaults 16 and 8), and the dictionary.'''
    sections = [16] * len(structure)
    transitions = [8] * (len(structure) - 1)
    with open(output_file, 'w') as f:
        f.write('# From midi files: {0}\n'
                'structure = "{1}"\n# Length of sections (in number'
                ' of notes):\nsections = {2}\n# Length of '
                'transitions between sections (in number of notes):\n'
                'transitions = {3}\nmapping = '
                .format(map_files, structure, sections, transitions))
        f.write('{')
        for i, file_name in enumerate(map_files[:-1]):
            section_letter = chr(i + 65)
            section_values = create_ordered_set(midi_input(file_name))
            f.write('"{0}": {1}, '.format(section_letter, section_values))
        last_letter = chr(len(map_files[:-1]) + 65)
        last_value = create_ordered_set(midi_input(map_files[-1]))
        f.write('"{0}": {1}'.format(last_letter, last_value))
        f.write('}')


def read_map_file(filename):
    '''Takes a mapping .txt file, reads in information about structure,
    mapping, section lengths and transition lengths from it.
    NB. Mapping file must follow the template format. If you are unsure
    of the format, use the function *create_map_file* to generate
    an adeguate file.'''
    with open(filename, 'r') as f:
        output = []
        for line in f.readlines():
            if line.startswith('#'):
                continue
            if line.endswith('\n'):
                line = line[:-1]
            output.append(eval(line.split(' = ')[1]))
    map_data = debug.read_map_file(*tuple(output))
    return map_data


def main():
    create_map_file(map_files=['input_test.mid', 'input_test.mid'],
                    structure='ABA',
                    output_file='map_test.txt')

if __name__ == '__main__':
    main()
