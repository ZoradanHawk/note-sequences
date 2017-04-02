from midi_toolkit import midi_input
from mapping_toolkit import read_map_file
import sequences

melody = midi_input('MSL.mid')
map_data = read_map_file('Map56.txt')

b = sequences.NoteSequence(melody, *map_data)