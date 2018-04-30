'''Unit tests for sequence_toolkit'''

import midi_toolkit
import sequence_toolkit as tools
import unittest

MELODY = midi_toolkit.read_melody('151.mid')[0]  # first track


class TestTransitionMatrix(unittest.TestCase):

    def test_intlist(self):
        num_list = [1, 2, 3, 1, 3]
        self.assertEqual(tools.create_transition_matrix(num_list),
                         {1: [(2, .5), (3, 0.5)], 2: [(3, 1.0)], 3: [(1, 1.0)]})

    def test_str(self):
        string = 'helloyou'
        self.assertEqual(tools.create_transition_matrix(string),
                         {'u': [], 'e': [('l', 1.0)], 'y': [('o', 1.0)],
                          'l': [('l', 0.5), ('o', 0.5)],
                          'h': [('e', 1.0)], 'o': [('u', 0.5), ('y', 0.5)]})

    def test_melody(self):
        self.assertEqual(tools.create_transition_matrix(MELODY),
                         {(79,): [((67,), 0.25), ((74,), 0.75)],
                          (74,): [((67,), 1.0)], (69,): [((79,), 1.0)],
                          (67,): [((69,), 1.0)]})

    def test_not_iterable(self):
        self.assertRaises(TypeError, tools.create_transition_matrix, 12)

    def test_empty_list(self):
        self.assertEqual(tools.create_transition_matrix([]), {})
        

MATRIX = {1: [(1, 1.0), (2, 1.0)],
          2: [(1, 1.0)]}


class TestSearchMatrix(unittest.TestCase):

    def test_0_repetition(self):
        self.assertEqual(tools._search_matrix(1, MATRIX, 0), (1, 1))

    def test_1_repetition(self):
        self.assertEqual(tools._search_matrix(1, MATRIX, 1), (1, 2))
        
    def test_2_repetition(self):
        self.assertEqual(tools._search_matrix(1, MATRIX, 2), (2, 0))

    def test_note_not_in_matrix(self):
        self.assertRaises(KeyError, tools._search_matrix, 3, MATRIX, 1)

    
class TestGenerateSequence(unittest.TestCase):

    def test_length(self):
        self.assertEqual(len(list(tools.generate_sequence(MELODY, 10))), 10)

    def test_no_length(self):
        self.assertEqual(list(tools.generate_sequence(MELODY, 0)), [])

    def test_empty_list(self):
        melody = tools.generate_sequence([], 10)
        self.assertRaises(IndexError, list, melody)

    def test_not_iterable(self):
        melody = tools.generate_sequence(1, 10)
        self.assertRaises(TypeError, list, melody)


MAPPING = {'A': [1, 2], 'B': [3, 4], 'C': [5, 6]}


class TestGenerateSection(unittest.TestCase):

    def test_length(self):
        generator = (i for i in [1, 2, 1, 1, 2, 2, 1])
        section = tools.generate_section(generator, 7, MAPPING, 'B')
        self.assertEqual(len(list(section)), 7)

    def test_set(self):
        generator = (i for i in [1, 2, 1, 1, 2, 2, 1])
        section = tools.generate_section(generator, 7, MAPPING, 'B')
        self.assertEqual(set(section), {3, 4})

    def test_compare_sections(self):
        generator = (i for i in [1, 2, 1, 1, 2, 2, 1])
        section = tools.generate_section(generator, 7, MAPPING, 'B')
        self.assertEqual(list(section), [3, 4, 3, 3, 4, 4, 3])

    def test_0_length(self):
        generator = (i for i in [1, 2, 1, 1, 2, 2, 1])
        section = tools.generate_section(generator, 0, MAPPING, 'B')
        self.assertEqual(list(section), [])

    def test_wrong_section(self):
        generator = (i for i in [1, 2, 1, 1, 2, 2, 1])
        section = tools.generate_section(generator, 7, MAPPING, 'D')
        self.assertRaises(KeyError, list, section)


class TestGenerateTransition(unittest.TestCase):
    
    def test_length(self):
        generator = (i for i in [1, 2, 1, 1, 2, 2, 1])
        transition = tools.generate_transition(generator, 7, MAPPING, 'A', 'B')
        self.assertEqual(len(list(transition)), 7)

    def test_set(self):
        generator = (i for i in [1, 2, 1, 1, 2, 2, 1]*10)
        transition = tools.generate_transition(generator, 70, MAPPING, 'A', 'B')
        self.assertEqual(set(transition), {1, 2, 3, 4})

    def test_0_length(self):
        generator = (i for i in [1, 2, 1, 1, 2, 2, 1])
        transition = tools.generate_transition(generator, 0, MAPPING, 'A', 'B')
        self.assertEqual(list(transition), [])

    def test_wrong_section(self):
        generator = (i for i in [1, 2, 1, 1, 2, 2, 1])
        transition = tools.generate_transition(generator, 7, MAPPING, 'A', 'D')
        self.assertRaises(KeyError, list, transition)


class TestConvertNote(unittest.TestCase):

    def test_conversion(self):
        self.assertEqual(tools.convert_note(1, MAPPING, 'B'), 3)
        self.assertEqual(tools.convert_note(2, MAPPING, 'C'), 6)

    def test_wrong_note(self):
        self.assertRaises(ValueError, tools.convert_note, 3, MAPPING, 'B')

    def test_wrong_section(self):
        self.assertRaises(KeyError, tools.convert_note, 1, MAPPING, 'D')


class TestUpdateChord(unittest.TestCase):

    def test_update(self):
        nvalue = (1,)
        nset = [(1,), (2,), (3,), (4,)]
        self.assertEqual(set(tools.update_chord(nvalue, 1, nset, 4)),
                         {1, 2, 3, 4})       

    def test_invalid_note(self):
        note_value = 1
        note_set = [(2,), (3,), (4,)]
        self.assertRaises(TypeError, tools.update_chord,
                          note_value, 1, note_set, 2)

    def test_note_not_in_set(self):
        nvalue = (1,)
        nset = [(2,), (3,), (4,)]
        self.assertEqual(len(tools.update_chord(nvalue, 1, nset, 2)), 3)

    def test_zero_prob(self):
        nvalue = (1,)
        nset = [(1,), (2,), (3,), (4,)]
        self.assertEqual(tools.update_chord(nvalue, 0, nset, 4), (1,))

    def test_zero_increase(self):
        nvalue = (1,)
        nset = [(1,), (2,), (3,), (4,)]
        self.assertEqual(tools.update_chord(nvalue, 1, nset, 0), (1,))


class TestFlattenSequence(unittest.TestCase):

    def test_flatten(self):
        self.assertEqual(tools.flatten_sequence(['he', (1, 2), [3, 4]]),
                         ['h', 'e', 1, 2, 3, 4])

    def test_is_notiter(self):
        self.assertRaises(TypeError, tools.flatten_sequence, 50)
        
    def test_contains_notiter(self):
        self.assertRaises(TypeError, tools.flatten_sequence, [1, 2, 3, 4])
        

class TestGroupByPitch(unittest.TestCase):

    def test_pitch_grouping(self):
        seq = [1, 2, 2, 1, 1, 1, 3, 1, 3, 2]
        grouped_seq = [(1,), (2, 2), (1, 1, 1), (3,), (1,), (3,), (2,)]
        self.assertEqual(tools.group_by_pitch(seq), grouped_seq)

    def test_all_same(self):
        seq = [1, 1, 1, 1, 1, 1]
        grouped_seq = [(1, 1, 1, 1, 1, 1)]
        self.assertEqual(tools.group_by_pitch(seq), grouped_seq)

    def test_all_different(self):
        seq = [1, 2, 3, 1, 2, 3, 4]
        grouped_seq = [(1,), (2,), (3,), (1,), (2,), (3,), (4,)]
        self.assertEqual(tools.group_by_pitch(seq), grouped_seq)

    def test_string(self):
        seq = 'hello'
        grouped_seq = [('h',), ('e',), ('l','l'), ('o',)]
        self.assertEqual(tools.group_by_pitch(seq), grouped_seq)
        
    def test_empty_list(self):
        self.assertRaises(IndexError, tools.group_by_pitch, [])
    
    def test_notiter(self):
        self.assertRaises(TypeError, tools.group_by_pitch, 1)

PAUSE = (5,)
class TestGroupByPauses(unittest.TestCase):

    def test_pause_grouping(self):
        seq = [1, 2, PAUSE, 1, PAUSE, 1, 1, 3, PAUSE, 3]
        grouped_seq = [(1, 2), (PAUSE, 1), (PAUSE, 1, 1, 3), (PAUSE, 3)]
        self.assertEqual(tools.group_by_pauses(seq), grouped_seq)

    def test_all_pauses(self):
        seq = [PAUSE, PAUSE, PAUSE]
        grouped_seq = [(PAUSE, PAUSE, PAUSE)]
        self.assertEqual(tools.group_by_pauses(seq), grouped_seq)

    def test_no_pauses(self):
        seq = [1, 2, 3, 1, 2, 3, 4]
        grouped_seq = [(1, 2, 3, 1, 2, 3, 4)]
        self.assertEqual(tools.group_by_pauses(seq), grouped_seq)
    
    def test_empty_list(self):
        self.assertRaises(IndexError, tools.group_by_pauses, [])
    
    def test_notiter(self):
        self.assertRaises(TypeError, tools.group_by_pauses, 1)


class TestGroupInChunks(unittest.TestCase):

    def test_chunk_grouping(self):
        seq = [1, 2, 2, 1, 3, 1, 3, 2]
        grouped_seq = [(1, 2, 2, 1), (3, 1, 3, 2)]
        self.assertEqual(tools.group_in_chunks(seq, 4), grouped_seq)

    def test_0len_chunks(self):
        seq = [1, 1, 1, 1, 1, 1]
        self.assertRaises(ZeroDivisionError, tools.group_in_chunks, seq, 0)

    def test_longer_chunk(self):
        seq = [1, 2, 2, 1, 3, 1, 3, 2]
        grouped_seq = [(1, 2, 2, 1, 3, 1, 3, 2)]
        self.assertEqual(tools.group_in_chunks(seq, 9), grouped_seq)

    def test_empty_list(self):
        self.assertEqual(tools.group_in_chunks([], 2), [])
    
    def test_notiter(self):
        self.assertRaises(TypeError, tools.group_in_chunks, 1, 2)

        
if __name__=='__main__':
    unittest.main()
