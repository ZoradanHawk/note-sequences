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


@debug.create_map_template
def create_map_template(output_filename, melody, structure, map_files=[]):
    '''*melody* is a list of note values. *structure* is a string of
    characters, which are labels for the sections (eg. ABACA). *map_files*
    is a list of additional midi file names, each of which should contain
    the version of *melody* in that section. The function creates a template
    mapping file. The file has 4 lines, detailing the structure, a list of
    section lengths (default 16 notes), a list of transition lengths
    (default 8 notes) and a mapping dictionary, describing what each unique
    note from the *melody* corrisponds to within other sections. '''
    A_section = create_ordered_set(melody)
    sections = [16] * len(structure)
    transitions = [8] * (len(structure) - 1)
    with open(output_filename, 'w') as f:
        f.write('structure = "{0}"\n# Length of sections (in number'
                ' of notes):\nsections = {1}\n# Length of '
                'transitions between sections (in number of notes):\n'
                'transitions = {2}\nmapping = {{"A": {3}'
                .format(structure, sections, transitions, A_section))
        for i, file_name in enumerate(map_files):
            section_letter = chr(i + 66)
            section_values = create_ordered_set(midi_input(file_name))
            f.write(', "{}": {}'.format(section_letter, section_values))
        f.write('}')


def read_map_file(filename):
    '''Takes a mapping .txt file, reads in information about structure,
    mapping, section lengths and transition lengths from it.
    NB. Mapping file must follow the template format. If you are unsure
    of the format, use the function *create_map_template* to generate
    an adeguate file.'''
    with open(filename, 'r') as f:
        for line in f.readlines():
            exec(line)
    map_data = debug.read_map_file(structure, mapping, sections, transitions)
    return map_data


def main():
    chords = midi_input('MSL.mid')
    create_map_template(output_filename='Map56.txt',
                    melody=chords,
                    structure='ABC',
                    map_files=['MSL.mid', 'MSL.mid'])

if __name__ == '__main__':
    main()