import random
from mido import MidiFile
from transition_matrix_class import TransitionMatrix

midi_file = MidiFile('chord_test.mid')

note_ons = [m for m in midi_file.tracks[0] if m.type is 'note_on' and m.velocity]

def chord_splitter(note_ons):
    chords = []
    chord = []
    for note in note_ons:
        if note.time:
            chords.append(tuple(chord))
            chord = []
            chord.append(note.note)
        else:
            chord.append(note.note)
    chords.append(tuple(chord))
    return chords


def chord_generator(chord):
    '''
    When next() is called on this generator, it yields the
    value that is more likely to follow the last yielded value,
    based on the probabilities defined in MATRIX.
    '''
    for i in range(20):
        rand = random.random()
        for pos, num in enumerate(matrix[chord].probs):
            if rand < num:
                chord = matrix[chord].choices[pos]
                break
        yield chord


chords = chord_splitter(note_ons)
matrix = TransitionMatrix(chords)
gen = chord_generator(random.choice(chords))
print matrix
for i in range(10):
    print next(gen)