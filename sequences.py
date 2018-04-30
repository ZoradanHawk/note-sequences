import random

import sequence_toolkit as tools
from mapping_toolkit import Map


def create_mapseq(melody, map_file):
    
    '''Takes a melody and a map file. Uses the information
    contained in the map file (sequence length, number of
    sections and transitions, sequence structure) to build
    a composite (mapped) sequence.'''
    
    sequence = []
    seq_info = Map.from_map_file(map_file)
    notes = tools.generate_sequence(melody, seq_info.length) 
    section_lengths = iter(seq_info.sections)
    transition_lengths = iter(seq_info.transitions)
    for i, section in enumerate(seq_info.structure):
        # Adding Sections
        sequence.extend(tools.generate_section(generator=notes,
                                               length=next(section_lengths),
                                               mapping=seq_info.mapping,
                                               section=section))
        try:
            # Adding Transitions
            next_section = info.structure[i + 1]
            sequence.extend(tools.generate_transition(generator=notes,
                                         length=next(transition_lengths),
                                         mapping=info.mapping,
                                         section=section,
                                         next_section=next_section))
        except IndexError:
            pass
    return sequence


def create_sparseseq(melody, length, fading=False):
    
    '''Creates a sequence with randomly occurring pauses (sparse sequence).
    With the default fading == False the pauses occur more frequently
    at the beginning, making the sequence emerge gradually from
    silence. If fading == True, pauses occur more often at the end,
    making the sequence gradually fade into silence.'''
    
    sequence = []
    notes = tools.generate_sequence(melody, length)
    if fading:
        calculate_probability = lambda i: 1 - (i / float(length))
    else:
        calculate_probability = lambda i: i / float(length)
    for i in range(length):
        prob = calculate_probability(i)
        if random.random() < prob:
            sequence.append(next(notes))
        else:
            sequence.append((5,))
    return sequence


def create_chordseq(melody, map_file, increase):
    
    '''Creates a variant of the mapped sequence with chords 
    occurring randomly throughout (chorded sequence). The chords 
    are of variable length, and are created by taking a base note 
    and adding other notes from the same section onto it. The chords 
    appear more frequently as the sequence progresses, similar to the 
    pauses in a sparse sequence with fading == False.'''
    
    sequence = []
    info = Map.from_map_file(map_file)
    notes = tools.generate_sequence(melody, info.length)
    section_lengths = iter(info.sections)
    transition_lengths = iter(info.transitions)
    prob = 0.0
    for i, letter in enumerate(info.structure):
        note_set = info.mapping[letter]
        section = tools.generate_section(generator=notes,
                                  length=next(section_lengths),
                                  mapping=info.mapping,
                                  section=letter)
        for note in section:
            sequence.append(tools.update_chord(note, prob, note_set, increase))
            prob += 1 / float(info.length)
        try:
            next_section = info.structure[i + 1]
            note_set = info.mapping[letter] + info.mapping[info.structure[i + 1]]
            transition = tools.generate_transition(generator=notes,
                                         length=next(transition_lengths),
                                         mapping=info.mapping,
                                         section=letter,
                                         next_section=next_section)
            for note in transition:
                sequence.append(tools.update_chord(note, prob, note_set, increase))
                prob += 1 / float(info.length)
        except IndexError:
            pass
    return sequence
