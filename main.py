__author__ = 'Thomas Grossi, Matt Giannotti'
__version__ = '0.7'

import midi_toolkit as midi
import sequences

# shows new version of midi input and how to use GroupedSequences

notes = midi.melody_input('Guitar1.mid')

seq = sequences.GroupedSequence(notes, 150)

midi.midi_output('grouped_by_pauses.mid', seq.grouped_by_pauses)
midi.midi_output('grouped_by_pitch.mid', seq.grouped_by_pitch)
