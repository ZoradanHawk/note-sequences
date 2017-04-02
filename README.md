# note-sequences
Collection of modules for extracting structural information from melodic sequences and using it to build new music with similar structure. Supports sequences of single notes or chords. Has option to read in melodic information from midi files and to write out the new sequences as midi files.

N.B. within this program, note values are tuples containing integers. A tuple of one element is a single note, whereas longer tuples are chords. The integers are meant to represent midi notes, and should be within range 0 - 127. Length of a sequence or section is measured in number of notes or chords.

Dependencies: Mido 1.1.19

sequences.py contains classes to build the output note sequences. Classes are:
- Sequence: takes a list of note values (created in python or read in from a midi file, see midi_toolkit.py) or       
  another Sequence object, and a length. Builds a sequence which follows the same melodic structure.
- NoteSequence: subclass of Sequence. Requires a .txt file with information about the desired structure (e.g. 'ABACA'), the
  section lengths (e.g. [16, 16, 16, 32, 8]), lengths of transitions between sections (e.g. [8, 0, 8, 12, 0]), and the mapping
  between section letters and note set to use (e.g. {'A': [(64,), (67,), (71,), (65,)], 'B': ... }.
- SparseSequence: subclass of Sequence. Also takes a specific note value to be converted into a pause within Sibelius or other score reading   
  software. Pause note is very prevalent in the beginning (making actual melody notes rather sparse), gradually disappears, leaving the normal 
  melody.
- ChordSequence: subclass of NoteSequence. Every note in the sequence has a certain probability (0 in the beginning, 1.0 by the end) of turning
  into a chord (argument chord_increase indicates the maximum amount of notes that can be added)

section_toolkit.py contains classes Section and TransitionSection, used to build NoteSequences. It also contains the function to create transition matrices, used by all sequences. 

midi_toolkit.py contains functions to extract note values from midi files, and to write out new midi files with note values from Sequence
objects (if rhythms aren't specified, defaults to eight-note values)

mapping_toolkit.py contains functions to create and read in the .txt files containing the structural information needed by NoteSequence and ChordSequence.

debug_toolkit.py contains wrapper functions to test the arguments of various functions (e.g. type checking).

main.py runs example Sequences based on test_input.mid and test_map.txt
