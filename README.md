Collection of modules for extracting structural information from melodic sequences and using it to build new music with similar structure. Supports sequences of single notes or chords. Has option to read in melodic information from midi files and to write out the new sequences as midi files.

N.B. within this program, note values are tuples containing integers. A tuple of one element is a single note, whereas longer tuples are chords. The integers are meant to represent midi notes, and should be within range 0 - 127. Length of a sequence or section is measured in number of notes or chords.

Dependencies: Mido 1.1.19

*main.py* is the interactive version of the program, which will ask for specific input step by step. Recommended for users who need to familiarise with the content, or are not comfortable with command line arguments, or simply want better documentation of their settings. Will build one of five note sequences, as a midi file:
- Generic Sequence: requires a midi file and a length (in notes). Builds a new melody of the desired length. which follows the same melodic structure of the input melody.
- Mapped Sequence: a more complex sequence built around one or more midi files. The melody contained in each file is used as a      base for a specific section within the output melody. Allows for transition periods between sections. Aside from the midi files it requires a .txt file with information about the desired structure (e.g. 'ABACA'), the lengths of sections (e.g. [16, 16, 16, 32, 8]) and transitions between sections (e.g. [8, 0, 8, 12, 0]), plus a mapping between section names and note values (e.g. {'A': [(64,), (67,), (71,), (65,)], 'B': ... }. This file is called a Map and can be built using the main of mapping_toolkit.py, or by modifying the test map provided (Map10.txt).
- Sparse Sequence: a sequence where the melody emerges gradually out of silence, or fades into silence. Requires a midi file, a length and indications on which of the two varieties (emerging or fading) is required.
- Chorded Sequence: every note in the sequence has a certain probability (increasing over time) of turning
  into a chord. Requires midi file/s, a Map, and a decision on the maximum extension of the chords (number of notes added).
- Grouped Sequence: a sequence that maintains specific patterns of the original melody in the output (e.g. groups of notes repeating, or separated by pauses). Requires a midi file, length and an indication on the type of grouping preferred.

*notesequence.py* is a version of main.py for command prompt. Supports command line arguments.

*sequences.py* contains higher level functions to build the more complex sequences.

*sequence_toolkit.py* contains various lower level functions used to build the sequences.

*midi_toolkit.py* contains functions to extract note values from midi files, and to write out new midi files from sequences 

*mapping_toolkit.py* contains functions to read in information from Map files, required to build Mapped and Chorded sequences. The module can also be run to build a new Map file. It is currently set to build the test map, Map10.txt. Change the arguments in main() to produce a different map.

*notesequence_unittests.py* currently contains unit tests for the functions in sequence_toolkit.py. It will be expanded within the next few months.
