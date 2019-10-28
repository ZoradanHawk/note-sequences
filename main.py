__author__ = 'Thomas Grossi, Matt Giannotti'
__version__ = '0.85'

import os

from midi_toolkit import read_melody, read_rhythms, write_midifile
from sequences import create_mapseq, create_sparseseq, create_chordseq
import sequence_toolkit as tools


def get_map():
    map_file = str(input('Map file (.txt format): '))
    try:
        open(map_file, 'r')
    except TypeError:
        maps = [f for f in next(os.walk('./'))[2] if f[-4:] == '.txt']
        if not maps:
            raise SystemExit('Invalid File Name. No .txt files detected in your directory.')
        print('Invalid File Name. .txt files in your directory: {}.'.format(
                                                                        maps))
        user_input = str(input('Try again? Y|N: '))
        if user_input.upper() == 'Y':
            map_file = get_map()
        else:
            raise SystemExit()
    return map_file


def get_input_method():
    which_method = str(input('Do you want to extract the melody or the ' + 
                               'rhythms from the sequence? (1|2): '))
    if which_method not in ['1', '2']:
        user_input = str(input('Incorrect Option. Try again? (Y|N): '))
        if user_input.upper() == 'Y':
            which_method = get_input_method()
        else:
            raise SystemExit()
    return read_melody if which_method == '1' else read_rhythms


def get_input_sequence(function):
    midifile = str(input('Input File Name (midi): '))
    try:
        input_sequence = function(midifile)
    except (FileNotFoundError, OSError):
        midi_files = [f for f in next(os.walk('./'))[2] if f[-4:] == '.mid']
        if not midi_files:
            raise SystemExit('Invalid File Name. No midi files detected in your directory.')
        print('Invalid File Name. Midi Files in your directory: {}.'.format(
                                                                midi_files))
        user_input = str(input('Try again? Y|N: '))
        if user_input.upper() == 'Y':
            input_sequence = get_input_sequence(function)
        else:
            raise SystemExit()
    if not input_sequence:
        raise SystemExit('Problem with the midi file. Try another one.')
    return input_sequence


def get_output_name():
    output_name = str(input('Output File Name (midi): '))
    if output_name[-4:] != ".mid":
        if '.' not in output_name:
            return '{}.mid'.format(output_name)
        else:
            print('Invalid file name. Output file must have a .mid extension.')
            user_input = str(input('Try again? Y|N: '))
            if user_input.upper() == 'Y':
                output_name = get_output_name()
            else:
                raise SystemExit()
    return output_name


def get_length():
    length = input('Sequence length (in notes): ')
    try:
        return int(length)
    except ValueError:
        user_input = str(input('Length must be an integer. Try again? Y|N: '))
        if user_input.upper() == 'Y':
            length = get_length()
        else:
            raise SystemExit()
    return int(length)


def get_segment_size():
    size = input('Segment size: ')
    try:
        return int(size)
    except ValueError:
        user_input = str(input('Size must be an integer. Try again? Y|N: '))
        if user_input.upper() == 'Y':
            size = get_segment_size()
        else:
            raise SystemExit()
    return int(length)

def write_seq(melody):
    length = get_length()
    return list(tools.generate_sequence(melody, length))



def write_mapseq(melody):
    map_file = get_map()
    return create_mapseq(melody, map_file)


def write_sparseseq(melody):
    length = get_length()
    from_user = str(input('''Do you want the sequence to emerge from silence 
                      or to fade away? 1|2: '''))
    fading = False if from_user == '1' else True
    return list(create_sparseseq(melody, int(length), fading))


def write_chordseq(melody):
    map_file = get_map()
    increase = str(input('Chord Increase: '))
    return create_chordseq(melody, map_file, int(increase))


def write_groupseq(melody):
    grouping = str(input('Do you want to group by pauses, pitch or segments ' +
                         'of a specified size? 1|2|3: '))
    if grouping == '1':
        seq = tools.group_by_pauses(melody)
    elif grouping == '2':
        seq = tools.group_by_pitch(melody)
    elif grouping == '3':
        segment_size = get_segment_size()
        seq = tools.group_by_segment_size(melody, segment_size)
    else:
        from_user = str(input('Incorrect grouping method. Try again? Y|N: '))
        if from_user == 'Y':
            write_groupseq(melody)
        else:
            raise SystemExit
    grouped_seq = write_seq(seq)
    return tools.flatten_sequence(grouped_seq)


sequence_types = {'1': write_seq, '2': write_mapseq, '3': write_sparseseq,
                 '4': write_chordseq, '5': write_groupseq}


def main():
    input_method = get_input_method()
    input_sequence = get_input_sequence(input_method)
    help_msg = ' '.join(('1 : Basic Sequence,',
                         '2 : Mapped Sequence,',
                         '3 : Sparse Sequence,',
                         '4 : Chord Sequence,',
                         '5 : Grouped Sequence.'))
    seq_type = str(input('Sequence Type {}: '.format(help_msg)))
    sequence = sequence_types.get(seq_type)
    if sequence:
        output_tracks = []
        for track in input_sequence:
            seq = sequence(track)
            output_tracks.append(seq)
    else:
        print('Invalid Sequence Type. Must be 1, 2, 3, 4 or 5. Look at Help.')
        raise SystemExit
    output_name = get_output_name()
    output_type = input_method == read_rhythms
    write_midifile(output_name, output_tracks, output_type)

if __name__== '__main__':
    main()
