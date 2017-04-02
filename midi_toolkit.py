'''Contains various functions to extract values from midi files or
write values into midi files.'''

from mido import Message, MidiFile, MidiTrack, MetaMessage
import random


def midi_input(filename):
    '''Takes a midi file, extracts note values as tuples 
    of integers (single int: one note, many ints: chord.
    Returns the tuples in a list.'''
    chords = []
    chord = []
    midi_file = MidiFile(filename)
    for track in midi_file.tracks:
        for message in track:
            if message.type == 'note_on' or message.type == 'note_off':
                if not message.time:
                    if message.velocity:
                        chord.append(message.note)
                    else:
                        chords.append(tuple(chord))
                        chord = []
                else:
                    if message.velocity:
                        chords.append(tuple(chord))
                        chord = []
                        chord.append(message.note)
                    else:
                        chords.append(tuple(chord))
                        chord = []
    return [tup for tup in chords if tup]


def extract_delta_times(sequence, rhythms):
    '''Pairs up elements of a Sequence with delta 
    time values (default 240). If rhythms contains integer
    values, the default delta time of 240 is multiplied by a
    factor of one of the integers (chosen at random).
    Returns a list of (note value, delta time) pairs'''
    index = 0
    if rhythms:
        while index < len(sequence):
            factor = random.choice(rhythms)
            for value in factor:
                delta_time = 240 * value
                index += value
                try:
                    yield sequence[index], delta_time
                except IndexError:
                    break
    else:
        for chord in sequence:
            yield chord, 240


def midi_output(filename, sequence, rhythms=[]):
    '''Takes a Sequence and writes them to a midi file. Optionally
    takes a list of integer factors to vary rhythms in the output.'''
    with MidiFile() as outfile:
        track = MidiTrack()
        outfile.tracks.append(track)
        track.append(MetaMessage('time_signature', numerator=4, denominator=4,
                     clocks_per_click=24, notated_32nd_notes_per_beat=8,
                     time=0))
        track.append(MetaMessage('key_signature', key='C'))
        track.append(MetaMessage('set_tempo', tempo=500000))
        track.append(Message('program_change', channel=0, program=0, time=0))
        track.append(Message('control_change', channel=0, control=121, value=0,
                                                                     time=0))
        track.append(Message('control_change', channel=0, control=64, value=0,
                                                                     time=0))
        track.append(Message('control_change', channel=0, control=91, value=0,
                                                                     time=0))
        track.append(Message('control_change', channel=0, control=10, value=63,
                                                                     time=0))
        track.append(Message('control_change', channel=0, control=7, value=98,
                                                                     time=0))
        for chord, delta_time in extract_delta_times(sequence, rhythms):
            for note in chord:
                track.append(Message('note_on', channel=0, note=note,
                                     velocity=64, time=0))
            track.append(Message('note_off', channel=0, note=chord[0],
                                 velocity=0, time=delta_time))
            if len(chord) > 1:
                for note in chord[1:]:
                    track.append(Message('note_off', channel=0, note=note,
                                 velocity=0, time=0))
        track.append(MetaMessage('end_of_track'))
        outfile.save(filename)
