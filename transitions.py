import random
from collections import Counter, defaultdict, namedtuple


class TransitionMatrix(object):
    def __init__(self, numbers):
        self.data = self.create_matrix(numbers)
        self.numbers = self.data.keys()

    def create_matrix(self, numbers):
        '''Takes a list of numbers (notes) or a list of tuples (chords)
        as input and constructs a dictionary: the keys are the set of
        unique elements in the input list, the values are named tuples
        of two elements, choices and prob, each in turn tuples.
        The element *choices* contains the notes or chords that follow
        the key in the input sequence; the element *probs* indicates
        the probability of the key note turning into the *choices*.
        e.g. {1: (choices=(2, 3, 5), prob=(.33, .66, 1.0)), ... }. '''
        transition_matrix = {}
        T = namedtuple('Transition', ['choices', 'probs'])
        for key, value in self.calculate_probabilities(numbers).items():
            if value:
                transition, probs = zip(*value)
                transition_matrix[key] = T(transition, self.merge_probs(probs))
            else:
                other_choice = random.choice([x for x in numbers if x != key])
                transition, probs = ((other_choice,), (1.0,))
                transition_matrix[key] = T(transition, probs)
        return transition_matrix

    @staticmethod
    def merge_probs(probs):
        '''Changes the format of a list of probabilities:
        e.g. input: (.33, .33, .33); output: (.33, .66, 1.0)'''
        probability = 0.0
        output = []
        for prob in probs:
            probability += prob
            output.append(probability)
        return tuple(output)

    @staticmethod
    def calculate_probabilities(numbers):
        '''Takes a list of numbers as input, returns a dictionary with the
        set of numbers as keys and lists of tuples as values. Each tuple
        will contain a number that the key number can transition to, and
        the probability that it will do so, based on the input list.
        e.g. {1: [(2, .33), (3, .33), (5, .33)], ... }'''
        core = defaultdict(list)
        counter = Counter(pair for pair in zip(numbers[:-1], numbers[1:]))
        for num in set(numbers):
            total_num = float(sum(count for pair, count in counter.items() if pair[0] == num))
            value = [(pair[1], count / total_num) for pair, count in counter.items() if pair[0] == num]
            core[num] = value
        return core

    def __iter__(self):
        for pair in self.data.items():
            yield pair

    def __getitem__(self, name):
        return self.data[name]

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self.data)


def main():
    notes = [1, 2, 3, 4, 5, 6, 3, 2, 1, 2, 3, 3, 4, 1, 1]
    matrix = TransitionMatrix(notes)
    print(matrix)


if __name__ == '__main__':
    main()
