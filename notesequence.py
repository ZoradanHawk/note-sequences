__author__ = 'Thomas Grossi, Matt Giannotti'
__version__ = '0.7'

import os
import argparse

from midi_toolkit import read_melody, write_midifile
from sequences import create_mapseq, create_sparseseq, create_chordseq
import sequence_toolkit as tools


parser = argparse.ArgumentParser()
parser.add_argument('type', help=' '.join(('1 : Basic Sequence,',
                                      '2 : Mapped Sequence,',
                                      '3 : Sparse Sequence,',
                                      '4 : Chord Sequence,',
                                      '5 : Grouped Sequence,')))
parser.add_argument('midi_file', help='Name of origin midi file.')
parser.add_argument('output_file', help='Name of output midi file.')

ARGS = parser.parse_args()


def get_map():
    map_file = str(input('Map file (.txt format): '))
    try:
        open(map_file, 'r')
    except TypeError:
        maps = [i for i in next(os.walk('./'))[2] if i[-4:] == '.txt']
        if not maps:
            print('No .txt maps in your directory. Build one with maps.py')
            raise SystemExit()
        print('Invalid Map file. .txt files in your directory: {}.'.format(
                                                                        maps))
        user_input = str(input('Try again? Y|N '))
        if user_input == 'Y':
            get_map()
        else:
            raise SystemExit
    return map_file


def write_seq(melody):
    length = str(input('Sequence length (in notes): '))
    return list(tools.generate_sequence(melody, int(length)))


def write_mapseq(melody):
    map_file = get_map()
    return create_mapseq(melody, map_file)


def write_sparseseq(melody):
    length = str(input('Sequence length (in notes): '))
    from_user = str(input('''Do you want the sequence to emerge from silence 
                      or to fade away? 1|2: '''))
    fading = False if from_user == '1' else True
    return list(create_sparseseq(melody, int(length), fading))


def write_chordseq(melody):
    map_file = get_map()
    increase = str(input('Chord Increase: '))
    return create_chordseq(melody, map_file, int(increase))


def write_groupseq(melody):
    grouping = str(input('Pauses or Pitch? 1|2: '))
    if grouping == '1':
        seq = tools.group_by_pauses(melody)
    elif grouping == '2':
        seq = tools.group_by_pitch(melody)
    else:
        from_user = str(input('Incorrect grouping method. Try again? Y|N '))
        if from_user == 'Y':
            write_groupseq(melody)
        else:
            raise SystemExit
    return tools.flatten_sequence(seq)


functions = {'1': write_seq, '2': write_mapseq, '3': write_sparseseq,
             '4': write_chordseq, '5': write_groupseq}


def main():
    melody = read_melody(ARGS.midi_file)
    sequence = functions.get(ARGS.type)
    if sequence:
        seq = sequence(melody)
    else:
        print('Invalid Sequence Type. Must be 1 , 2, 3, 4 or 5. Look at Help.')
        raise SystemExit
    output_name = ARGS.output_file
    write_midifile(output_name, seq)

main()
