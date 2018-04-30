'''Collection of component functions needed to build the various sequences.'''

import random
import collections


def generate_sequence(melody, length):
    
    '''Builds a note sequence based on the transition probabilities 
    of a melody. Takes a melody and length (in notes) as input. Output
    is a generator.'''
    
    note = random.choice(melody)
    matrix = create_transition_matrix(melody)
    repetitions = 0
    for i in range(length):
        if not matrix[note]:  # fix for notes with no followers
            note = max(matrix, key=lambda x: len(matrix[x]))
        note, repetitions = _search_matrix(note, matrix, repetitions)
        yield note


def create_transition_matrix(melody):
    
    '''Component of generate_sequence. Takes a sequence and calculates
    the probability of each item being followed by any other item 
    within the sequence. Output is a dictionary where keys are the unique
    items and values are lists of (item, probability) tuples. 
    E.g. INPUT:[1, 2, 3, 1, 3]; 
    OUTPUT: {1: [(2, .5), (3, 0.5)], 2: [(3, 1.0)], 3: [(1, 1.0)]}.'''
    
    matrix = {}
    pair_counter = collections.Counter(zip(melody[:-1], melody[1:]))  # pairs adjacent notes and counts how often that pair exists in the sequence
    for note in set(melody):
        subset = sorted(item for item in pair_counter.items()
                        if item[0][0] == note)  # extracts the pairs in which the first note is the one were currently observing
        options = [pair[1] for pair, count in subset]  # extracts the second notes of each pair
        total_count = sum(count for pair, count in subset)  
        probs = [count / float(total_count) for pair, count in subset]
        matrix[note] = list(zip(options, probs))  # list because repr of zip objects in Py3
    return matrix


def _search_matrix(note, matrix, repetitions):

    '''Component of generate_sequence. Chooses the next note
    in the sequence based on the current one. Also keeps track
    of repetitions, avoiding notes that have been already selected
    three times in a row. Output is a tuple (note, repetitions).'''
    
    new_note = random.choice([n[0] for n in matrix[note] if n[0] != note])
    if repetitions == 2: # check if *note* appeared three times in a row
        return new_note, 0
    rand = random.random()
    current_prob = 0.0  
    for possible_note, probability in matrix[note]:
        current_prob += probability
        if rand < current_prob:
            if possible_note == note:  # repetition
                return possible_note, repetitions + 1
            else:
                return possible_note, 0


def generate_section(generator, length, mapping, section):
    
    '''Builds a section for mapped and chorded sequences.
    Takes a sequence generator, length (in notes) and a
    mapping dictionary (section to notes) as input. Output
    is a generator.'''

    for _ in range(length):
        note = next(generator)
        yield convert_note(note, mapping, section)


def generate_transition(generator, length, mapping, section, next_section):
    
    '''Builds a gradual transition between two sections. Takes a
    sequence generator, length (in notes) as input and a mapping
    dictionary (section to notes) as input. Output is a generator.'''
    
    for i in range(length):
        note = next(generator)
        if random.random() < i / float(length):
            yield convert_note(note, mapping, next_section)
        else:
            yield convert_note(note, mapping, section)


def convert_note(note_value, mapping, section):
    
    '''Component of generate_section and generate_transition.
    Takes a note value, mapping dictionary (section to notes)
    and a section character as input. Converts the note value
    to its value within the input section. Output is the new
    note value.'''

    if section == 'A':
        return note_value
    index = mapping['A'].index(note_value)
    return mapping[section][index]


def update_chord(note_value, prob, note_set, chord_increase):
    
    '''Component of the chorded sequence. Updates a note or existing chord
    by adding other notes from the current section's note set. Does so
    depending on the input probability and potentially as many times as
    the input chord increase. Returns the updated chord.'''
    
    for _ in range(chord_increase):
        if random.random() < prob:
            note_set = [note for note in note_set if note[0] not in note_value]
            note_value += random.choice(note_set) if note_set else ()
    return note_value


def flatten_sequence(sequence):

    '''Component of the grouped sequence. Takes a sequence of
    sequences (e.g. a list of lists). Flattens it out, returning
    a single sequence containing all items that belonged to the
    lower level sequences.'''
    
    final = []
    for group in sequence:
        final.extend(group)
    return final


def group_by_pitch(sequence):

    '''Component of the grouped sequence. Takes a sequence and
    groups same elements into tuples within the sequence.'''
    
    final = []
    group = []
    for i, note in enumerate(sequence[:-1]):
        next_note = sequence[i + 1]
        if note == next_note:
            group.append(note)
        else:
            final.append(tuple(group + [note]))
            group = []
    group.append(sequence[-1])
    final.append(tuple(group))
    return final


def group_by_pauses(sequence):

    '''Component of the grouped sequence. Takes a sequence and
    groups elements between pauses into tuples within the sequence.'''
    
    final = []
    group = []
    for i, note in enumerate(sequence[:-1]):
        next_note = sequence[i + 1]
        if note == (5,):
            group.append(note)
        elif next_note == (5,):
            final.append(tuple(group) + (note,))
            group = []
        else:
            group.append(note)
    group.append(sequence[-1])
    final.append(tuple(group))
    return final


def group_in_chunks(sequence, chunk_size):
    
    '''Component of the grouped sequence. Takes a sequence and groups
    elements into tuples of length determined by input chunk_size.'''
    
    final = []
    group = []
    for i, note in enumerate(sequence):
        if (i + 1) % chunk_size:
            group.append(note)
        else:
            final.append(tuple(group + [note]))
            group = []
    if group:
        final.append(tuple(group))
    return final
