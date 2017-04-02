from mido import Message, MidiFile, MidiTrack, MetaMessage
import random


def midi_input(filename):
    '''Takes a midi file that only contains chords, extracts
    the note values of the chord components and stores them
    in tuples, and the tuples in a list.'''
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
    '''Yes, it's a generator. That's new. '''
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


def midi_output(filename, sequence, rhythms=[], tempo=500000):
    '''Takes a sequence of notes and writes them to a midi file.'''
    with MidiFile() as outfile:
        track = MidiTrack()
        outfile.tracks.append(track)
        track.append(MetaMessage('time_signature', numerator=4, denominator=4,
                     clocks_per_click=24, notated_32nd_notes_per_beat=8,
                     time=0))
        track.append(MetaMessage('key_signature', key='C'))
        track.append(MetaMessage('set_tempo', tempo=tempo))
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


def group_midi_output(sequence_list, rhythms):
    for index, sequence in enumerate(sequence_list):
        filename = 'test_sequence{}.mid'.format(index)
        midi_output(filename, sequence, rhythms[index])
