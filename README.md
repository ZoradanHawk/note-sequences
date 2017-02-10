# note-sequences
Collection of modules for extracting structural information from melodic sequences and using it to build new music with similar structure.

- section_builder contains the class Section and subclasses NormalSection (a stand-alone musical section) and TransitionSection (a section that unites two *NormalSection*s, where notes have an increasing or decreasing probability of turning into the next section's equivalent).

- note_sequence contains the classes TransitionMatrix (which takes a list of notes and extracts the probabilities that one note be followed by any of the others) and NoteSequence (which takes a transition matrix, generates notes based on it and uses the *Section* subclasses to build up a sequence that follows a specific mapping and structure.
