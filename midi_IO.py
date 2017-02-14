from mido import Message, MidiFile, MidiTrack, MetaMessage


def input_midi_notes(filename):
    '''Takes a midi file and extracts all note values
    from it, stores them in a list.'''
    midi_in = MidiFile(filename)
    note_list = []
    for message in midi_in.tracks[1]:
        if message.type == 'note_on' and message.velocity:
            note_list.append(message.note)
    return note_list


def input_midi_chords(filename):
    '''Takes a midi file that only contains chords, extracts
    the note values of the chord components and stores them
    in tuples, and the tuples in a list.'''
    chords = []
    midi_file = MidiFile(filename)
    note_ons = [m for m in midi_file.tracks[0] if m.type is 'note_on' and m.velocity]
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


def output_midi_notes(filename, sequence):
    '''Takes a sequence of notes and writes them to a midi file.'''
    with MidiFile() as outfile:
        track = MidiTrack()
        outfile.tracks.append(track)
        track.append(MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))#clocks_per_click=24
        track.append(MetaMessage('key_signature', key='C'))
        track.append(MetaMessage('set_tempo', tempo=1000000))
        track.append(Message('program_change', channel=0, program=0, time=0))
        track.append(Message('control_change', channel=0, control=121, value=0, time=0))
        track.append(Message('control_change', channel=0, control=64, value=0, time=0))
        track.append(Message('control_change', channel=0, control=91, value=0, time=0))
        track.append(Message('control_change', channel=0, control=10, value=0, time=0))
        track.append(Message('control_change', channel=0, control=7, value=0, time=0))
        for note in sequence:
            track.append(Message('note_on', channel=0, note=note, velocity=64, time=0))
            track.append(Message('note_off', channel=0, note=note, velocity=0, time=240))
        track.append(MetaMessage('end_of_track'))
        outfile.save(filename)


def main():
    notes = input_midi_notes('note_file.mid')
    # chords = input_midi_chords('chord_file.mid')
    output_midi_notes('notes_output.mid', sequence=notes)

if __name__ == '__main__':
    main()