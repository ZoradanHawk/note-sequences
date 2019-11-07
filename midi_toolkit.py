'''Contains various functions to extract values from midi files or
write values into midi files.'''

import random
import os

from mido import Message, MidiFile, MidiTrack, MetaMessage


def match_note_offs(note_off, note_ons, time, ticks):
    
    '''Closes an "open" note, by identifying which
    of the current "note on" messages has the same note
    value as the input "note off". Returns the note with
    an added "note off" time and removes the "note on"
    from the list.'''
    
    i = 0
    while i < len(note_ons):
        chord = note_ons[i]
        if chord[0] == note_off.note:
            note_ons.remove(chord)
            return chord + [time]
        else:
            i += 1


def convert_group_to_chord(group, ticks):
    
    '''Takes a group of notes with the same starting
    and ending time and builds a chord out of them
    ((note1, note2), delta_time). Groups with one element
    become single notes (tuples with 1 element).'''
    
    note_values = tuple([note[0] for note in group])
    delta_time = group[0][2] - group[0][1]
    delta_time = int(round(delta_time / ticks * 240))
    return (note_values, (delta_time,))


def group_notes_into_chords(note_list, ticks):
    '''Takes a list of notes and returns a list of
    lists. Each sublist contains notes that have
    the same start time and end time (thus belong
    in a chord).'''
    output = []
    group = []
    for i, note in enumerate(note_list[:-1]):
        next_note = note_list[i + 1]
        if note[1:] == next_note[1:]:
            group.append(note)
        else:
            group.append(note)
            output.append(convert_group_to_chord(group, ticks))
            group = []
    group.append(note_list[-1])
    output.append(convert_group_to_chord(group, ticks))
    return output


def read_midifile(filename):
    
    '''Extracts note values and delta times from a midi file.'''
    
    output = []
    time = 0
    current_note_ons = []
    finished_notes = []
    with MidiFile(filename) as f:
        ticks = float(f.ticks_per_beat)
        for track in f.tracks:
            for msg in track:
                if msg.time == 1:
                    msg.time = 0  # fix for bug introduced by Musescore
                if msg.type == 'note_on' and msg.velocity and msg.time:
                    time_off = time + msg.time
                    note = (5, time, time_off)
                    finished_notes.append(note)
                time += msg.time
                if msg.type == 'note_on' and msg.velocity:
                    note_on = [msg.note, time]
                    current_note_ons.append(note_on)
                elif msg.type == 'note_on' and not msg.velocity:
                    note = match_note_offs(msg, current_note_ons, time, ticks)
                    finished_notes.append(note)
                elif msg.type == 'note_off':
                    note = match_note_offs(msg, current_note_ons, time, ticks)
                    finished_notes.append(note)
        finished_notes = sorted(finished_notes, key=lambda x: x[1])
        output.append(group_notes_into_chords(finished_notes, ticks))
    return output


def read_melody(filename):
    
    '''Extracts melody from a midi file, which can be used
     as input by current Sequences.'''
    
    data = read_midifile(filename)
    final_melody = []
    return [[note_value for note_value, delta_time in track] for track in data]


def read_rhythms(filename):
    
    '''Extracts delta times from a midi file, which can
     be used as input by current Sequences.'''
    
    data = read_midifile(filename)
    rhythms = []
    for track in data:
        new_track = []
        for note_value, delta_time in track:
            if note_value == (5,):  # (5,) is pauses
                new_track.append(note_value + delta_time)
            else:
                new_track.append(delta_time)
        rhythms.append(new_track)
    return rhythms
    # return [[delta_time for note_value, delta_time in data[track]]]


def test_midi_filename(midi_file_name):

    '''Checks if a specified midi file is present in your directory.'''
    
    try:
        read_melody(midi_file_name)
        read_rhythms(midi_file_name)
    except (FileNotFoundError, OSError):
        midi_files = [f for f in next(os.walk('./'))[2] if f[-4:] == '.mid']
        if not midi_files:
            raise SystemExit('''Invalid File Name. No midi files detected
                        in your directory.''')
        print('Invalid File Name. Midi Files in your directory: {}.'.format(
                                                                midi_files))
        user_input = str(input('Try again? Y|N: '))
        if user_input.upper() == 'Y':
            new_attempt = str(input('''New Midi file attempt: '''))
            midi_file_name = test_midi_filename(new_attempt)
        else:
            raise SystemExit()
    return midi_file_name


def create_midi_file_list():

    '''Creates a list of midi files specified by the user. The list is
    needed to build a Map object from midi files.'''
    
    list_length = int(input('How many Midi files do you need in your Map? '))
    for file_nr in range(list_length):
        file_name = str(input('''Midi File {}: '''.format(chr(file_nr + 65))))
        tested_name = test_midi_filename(file_name)
        midi_file_list.append(tested_name)
    return midi_file_list


def list_midi_files_in_directory():
    midis= [f for f in next(os.walk('./'))[2] if f[-4:] == '.mid']
    if not midis:
        print('No midi files in directory.')
        raise SystemExit()
    print('Midi Files in your directory: {}'.format(midis))


def extract_delta_times(sequence, rhythms):
    
    '''Pairs up elements of a Sequence with delta
    time values (default 240). If rhythms contains integer
    values, the default delta time of 240 is multiplied by a
    factor of one of the integers (chosen at random).
    Returns a list of (note value, delta time) pairs'''
    
    index = 0
    if rhythms:
        for delta_time in sequence:
            if len(delta_time) == 2:  # (pause, delta time)
                yield (5,), delta_time[1]
            else:
                yield (64,), delta_time[0]
    else:
        for chord in sequence:
            yield chord, 240


def write_midifile(filename, sequence, rhythms=False):
    
    '''Takes a Sequence and writes it to a midi file. In default
    mode, with rhythms = False, it expects a sequence of notes or
    chords. With rhythms set to True, it expects a sequence of
    delta times.'''
    
    with MidiFile() as outfile:
        for seq in sequence:
            track = MidiTrack()
            outfile.tracks.append(track)
            track.append(
                MetaMessage('time_signature', numerator=4, denominator=4,
                            clocks_per_click=24, notated_32nd_notes_per_beat=8,
                            time=0))
            track.append(MetaMessage('key_signature', key='C'))
            track.append(MetaMessage('set_tempo', tempo=500000))
            track.append(Message('program_change', channel=0, program=0, time=0))
            track.append(
                Message('control_change', channel=0, control=121, value=0, time=0))
            track.append(
                Message('control_change', channel=0, control=64, value=0, time=0))
            track.append(
                Message('control_change', channel=0, control=91, value=0, time=0))
            track.append(
                Message('control_change', channel=0, control=10, value=63, time=0))
            track.append(
                Message('control_change', channel=0, control=7, value=98, time=0))
            for chord, delta_time in extract_delta_times(seq, rhythms):
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
