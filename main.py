__author__ = 'Thomas Grossi, Matt Giannotti'
__version__ = '0.7'

import midi_toolkit as midi
import sequences

notes = midi.midi_input('test_input.mid')

# Example of creating sequences
seq = sequences.Sequence(melody=notes, length=100)
note_seq = sequences.NoteSequence(melody=notes, map_filename='test_map.txt')
sparse_seq = sequences.SparseSequence(melody=notes, length=100, pause_value=60)
chord_seq = sequences.ChordSequence(melody=notes, map_filename='test_map.txt', chord_increase=3)

midi.midi_output(filename='test_output_with_rhythms.mid', sequence=seq, rhythms=[(2, 3), (2, 2)])
midi.midi_output(filename='test_output.mid', sequence=note_seq)
