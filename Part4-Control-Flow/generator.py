"""
Generator Functions in the Standard Library.


Filtering generators::

    >>> def vowel(c):
    ...     return c.lower() in 'aeiou'
    >>> list(filter(vowel, 'Aardvark'))
    ['A', 'a', 'a']
    >>> from itertools import filterfalse, dropwhile, takewhile, compress, islice
    >>> list(filterfalse(vowel, 'Aardvark'))
    ['r', 'd', 'v', 'r', 'k']
    >>> list(dropwhile(vowel, 'Aardvark'))
    ['r', 'd', 'v', 'a', 'r', 'k']
    >>> list(takewhile(vowel, 'Aardvark'))
    ['A', 'a']
    >>> list(compress('Aardvark', (1, 0, 1, 1, 0, 1)))
    ['A', 'r', 'd', 'a']
    >>> list(islice('Aardvark', 4))
    ['A', 'a', 'r', 'd']
    >>> list(islice('Aardvark', 4, 7))
    ['v', 'a', 'r']
    >>> list(islice('Aardvark', 1, 7, 2))
    ['a', 'd', 'a']


Mapping generators::

    >>> from itertools import accumulate, starmap
    >>> sample = [5, 4, 2, 8, 7, 6, 3, 0, 9, 1]
    >>> list(accumulate(sample))
    [5, 9, 11, 19, 26, 32, 35, 35, 44, 45]
    >>> list(accumulate(sample, min))
    [5, 4, 2, 2, 2, 2, 2, 0, 0, 0]
    >>> from operator import mul
    >>> list(accumulate(sample, mul))
    [5, 20, 40, 320, 2240, 13440, 40320, 0, 0, 0]
    >>> list(enumerate('albatroz', 1))
    [(1, 'a'), (2, 'l'), (3, 'b'), (4, 'a'), (5, 't'), (6, 'r'), (7, 'o'), (8, 'z')]
    >>> list(map(mul, range(11), [2, 4, 8]))
    [0, 4, 16]
    >>> list(map(lambda a, b: (a, b), range(11), [2, 4, 8]))
    [(0, 2), (1, 4), (2, 8)]
    >>> list(starmap(mul, enumerate('albatroz', 1)))
    ['a', 'll', 'bbb', 'aaaa', 'ttttt', 'rrrrrr', 'ooooooo', 'zzzzzzzz']
    >>> sample = [5, 4, 2, 8, 7, 6, 3, 0, 9, 1]
    >>> list(starmap(lambda a, b: b/a, enumerate(accumulate(sample), 1)))
    [5.0, 4.5, 3.6666666666666665, 4.75, 5.2, 5.333333333333333, 5.0, 4.375, 4.888888888888889, 4.5]


Merging generators::

    >>> from itertools import chain, zip_longest, product
    >>> list(chain('ABC', range(2)))
    ['A', 'B', 'C', 0, 1]
    >>> list(chain(enumerate('ABC')))
    [(0, 'A'), (1, 'B'), (2, 'C')]
    >>> list(chain.from_iterable(enumerate('ABC')))
    [0, 'A', 1, 'B', 2, 'C']
    >>> list(zip('ABC', range(5), [10, 20, 30, 40]))
    [('A', 0, 10), ('B', 1, 20), ('C', 2, 30)]
    >>> list(zip_longest('ABC', range(5), fillvalue="?"))
    [('A', 0), ('B', 1), ('C', 2), ('?', 3), ('?', 4)]
    >>> list(product('ABC', range(2)))
    [('A', 0), ('A', 1), ('B', 0), ('B', 1), ('C', 0), ('C', 1)]
    >>> list(product('ABC'))
    [('A',), ('B',), ('C',)]
    >>> list(product('ABC', repeat=2))
    [('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'B'), ('B', 'C'), ('C', 'A'), ('C', 'B'), ('C', 'C')]
    >>> list(product(range(2), repeat=3))
    [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]
    >>> rows = product('AB', range(2), repeat=2)
    >>> for row in rows: print(row)  # doctest: +ELLIPSIS
    ('A', 0, 'A', 0)
    ('A', 0, 'A', 1)
    ('A', 0, 'B', 0)
    ('A', 0, 'B', 1)
    ('A', 1, 'A', 0)
    ('A', 1, 'A', 1)
    ...

Expanding generators::

    >>> from itertools import count, cycle, repeat, combinations, combinations_with_replacement, permutations
    >>> ct = count()
    >>> next(ct), next(ct), next(ct)
    (0, 1, 2)
    >>> list(islice(count(1, .3), 3))
    [1, 1.3, 1.6]
    >>> cy = cycle('ABC')
    >>> next(cy)
    'A'
    >>> list(islice(cy, 7))
    ['B', 'C', 'A', 'B', 'C', 'A', 'B']
    >>> rp = repeat(7)
    >>> next(rp), next(rp)
    (7, 7)
    >>> list(repeat(8, 4))
    [8, 8, 8, 8]
    >>> list(map(mul, range(11), repeat(5)))
    [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    >>> list(combinations('ABC', 2))
    [('A', 'B'), ('A', 'C'), ('B', 'C')]
    >>> list(combinations_with_replacement('ABC', 2))
    [('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'B'), ('B', 'C'), ('C', 'C')]
    >>> list(permutations('ABC', 2))
    [('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')]
    >>> list(product('ABC', repeat=2))
    [('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'B'), ('B', 'C'), ('C', 'A'), ('C', 'B'), ('C', 'C')]


Rearranging generators::

    >>> from itertools import groupby, tee
    >>> list(groupby('LLLLAAGGG'))  # doctest: +ELLIPSIS
    [('L', <itertools._grouper object at ...>), ('A', <itertools._grouper object at ...>), ('G', <itertools._grouper object at ...>)]
    >>> for char, group in groupby('LLLLAAGGG'):
    ...     print(char, '->', list(group))
    L -> ['L', 'L', 'L', 'L']
    A -> ['A', 'A']
    G -> ['G', 'G', 'G']
    >>> animals = ['duck', 'eagle', 'rat', 'giraffe', 'bear', 'bat', 'dolphin', 'shark', 'lion']
    >>> animals.sort(key=len)
    >>> for length, group in groupby(animals, len):
    ...     print(length, '->', list(group))
    3 -> ['rat', 'bat']
    4 -> ['duck', 'bear', 'lion']
    5 -> ['eagle', 'shark']
    7 -> ['giraffe', 'dolphin']
    >>> for length, group in groupby(reversed(animals), len):
    ...     print(length, '->', list(group))
    7 -> ['dolphin', 'giraffe']
    5 -> ['shark', 'eagle']
    4 -> ['lion', 'bear', 'duck']
    3 -> ['bat', 'rat']
    >>> list(tee('ABC'))  # doctest: +ELLIPSIS
    [<itertools._tee object at ...>, <itertools._tee object at ...>]
    >>> list(zip(*tee('ABC')))
    [('A', 'A'), ('B', 'B'), ('C', 'C')]


Reducing Functions::

    >>> all([1, 2, 3])
    True
    >>> all([1, 0, 3])
    False
    >>> all([])
    True
    >>> any([1, 2, 3])
    True
    >>> any([1, 0, 3])
    True
    >>> any([0, 0.0])
    False
    >>> any([])
    False
    >>> g = (n for n in [0, 0.0, 7, 8])
    >>> any(g)
    True
    >>> next(g)
    8
"""
import itertools


class ArithmeticProgression:
    """
    >>> ap = ArithmeticProgression(0, 1, 3)
    >>> list(ap)
    [0, 1, 2]
    >>> ap = ArithmeticProgression(1, .5, 3)
    >>> list(ap)
    [1.0, 1.5, 2.0, 2.5]
    >>> ap = ArithmeticProgression(0, 1/3, 1)
    >>> list(ap)
    [0.0, 0.3333333333333333, 0.6666666666666666]
    >>> from fractions import Fraction
    >>> ap = ArithmeticProgression(0, Fraction(1, 3), 1)
    >>> list(ap)
    [Fraction(0, 1), Fraction(1, 3), Fraction(2, 3)]
    >>> from decimal import Decimal
    >>> ap = ArithmeticProgression(0, Decimal('.1'), .3)
    >>> list(ap)
    [Decimal('0'), Decimal('0.1'), Decimal('0.2')]

    """

    def __init__(self, begin, step, end=None):
        self.begin = begin
        self.step = step
        self.end = end  # None -> "infinite" series

    def __iter__(self):
        # coerce the type of begin to the subsequent additions
        result = type(self.begin + self.step)(self.begin)
        forever = self.end is None
        index = 0
        while forever or result < self.end:
            yield result  # current result is produced
            index += 1
            result = self.begin + self.step * index  # the next potential result is calculated.


def aritprog_gen(begin, step, end=None):
    """
    If the whole point of a class is to build a generator by implementing
    __iter__, the class can be reduced to a generator function. A generator
    function is, after all, a generator factory.
    """
    result = type(begin + step)(begin)
    forever = end is None
    index = 0
    while forever or result < end:
        yield result
        index += 1
        result = begin + step * index


def aritprog_gen2(begin, step, end=None):
    """When implementing generators, know what is available in the standard
    library, otherwise there's a good chance you'll reinvent the wheel."""
    first = type(begin + step)(begin)
    ap_gen = itertools.count(first, step)
    if end is not None:
        ap_gen = itertools.takewhile(lambda n: n < end, ap_gen)
    return ap_gen
