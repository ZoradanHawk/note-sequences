# note-sequences
Collection of modules for extracting structural information from melodic sequences and using it to build new music with similar structure. Works with sequences of notes or chords.

- note_sequence.py is the main module. It creates the output note sequence.

- sections.py builds the sections of the sequence. It contains a class, Sequence, and a subclass, TransitionSequence.

- transitions.py extracts the structural information from the input notes taken from the midi file and saves them
  as a TransitionMatrix object. The information describes what notes follow each unique note in the input sequence, and with
  what probability.
  
- midi_IO.py contains functions to extract the information from a midi file and write it to an output midi file.
