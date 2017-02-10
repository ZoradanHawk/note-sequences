from collections import Counter, defaultdict, namedtuple
import random

T = namedtuple('Transition', ['choices', 'probs'])


class TransitionMatrix():
    '''Takes a list of numeric values and extracts the probability
    that each individual value be followed by any of the others.'''
    def __init__(self, numbers):
        self.keys = numbers
        self.matrix = transition_matrix(self.keys)

    def __iter__(self):
        for i in self.matrix.items():
            yield i

    def __getitem__(self, name):
        return self.matrix[name]


def merge_probs(probs):
    '''Changes the format of a list of probabilities to
    follow the calculation of our Transition Matrix.'''
    c = 0
    final = []
    for prob in probs:
        c += prob
        final.append(c)
    return tuple(final)


def core_dict(numbers):
    '''Takes a list of numbers as input, returns a dictionary with the
    set of numbers as keys and lists of tuples as values. Each tuple
    contains a number that the key number can transitioned to, and
    the probability that it will do so, based on the input list.'''
    core = defaultdict(list)
    counter = Counter(pair for pair in zip(numbers[:-1], numbers[1:]))
    for num in set(numbers):
        total_num = float(sum(count for pair, count in counter.items() if pair[0] is num))
        value = [(pair[1], count / total_num) for pair, count in counter.items() if pair[0] is num]
        core[num] = value
    return core


def transition_matrix(numbers):
    '''
    Takes a list of numbers as input and returns a dictionary
    with the set of numbers as keys and lists of tuples as values.
    The first element of the tuple presents the possible numbers
    the key number can transition to, all other elements are the
    probability that it shall to so.
    '''
    final = {}
    for key, value in core_dict(numbers).items():
        if value:
            transition, probs = zip(*value)
            final[key] = T(transition, merge_probs(probs))
        else:
            other_choice = random.choice([x for x in numbers if x != key])
            transition, probs = ((other_choice,), (1.0,))
            final[key] = T(transition, probs)
    return final