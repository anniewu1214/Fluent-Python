import re
import reprlib
import random

"""
Why sequences are iterable: Whenever the interpreter needs to iterate over an object x,
it automatically calls iter(x). iter

1. checks whether the object implements __iter__, and calls that to obtain an iterator
2. if __iter__ is not defined, but __getitem__ is, Python creates an iterator that
attempts to fetch items in order, starting from index 0
3. if that fails, Python raises TypeError

Note: the standard sequence also implement __iter__, and yours should too.
__getitem__ exits for backward compability reasons and may be gone in the future.


Iterable vs. Iterator:

- iterables have an __iter__ method that instantiates a new iterator every time

- iterators implement __next__ that returns individual items, and __iter__
 that returns self

- iterators are iterable, but iterables are not iterators

- an iterable should never act as an iterator over itself =>
 iterables must implement __iter__, but not __next__

"""
RE_WORD = re.compile('\w+')


class Sentence:
    """
    A Sentence as a sequence of words.

    >>> s = Sentence('"The time has come," the Walrus said,')
    >>> s
    Sentence('"The time ha... Walrus said,')
    >>> for word in s:
    ...     print(word)  # doctest: +ELLIPSIS
    The
    time
    has
    ...
    >>> list(s)  # Being iterable, Sentence objects can be used as input to build lists and other iterable types.
    ['The', 'time', 'has', 'come', 'the', 'Walrus', 'said']
    """

    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __getitem__(self, item):
        return self.words[item]

    def __len__(self):
        return len(self.words)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)


class SentenceIterator:
    """The standard interface for an interator has two methods:

    - __next__: returns the next available item, raising StopIteration
    when there are no more items

    - __iter__: Returns `self`; this allows iterators to be used where
    an iterable is expected, e.g. in a for loop.
    """

    def __init__(self, words):
        self.words = words
        self.index = 0

    def __next__(self):
        try:
            word = self.words[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return word

    def __iter__(self):
        return self


class Sentence2:
    """Sentence implenented using the Iterator pattern"""

    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        """__iter__ fullfills the iterable protocol by instantiating and
        returning the iterator."""
        return SentenceIterator(self.words)


class Sentence3:
    """Sentence implemented using a generator function"""

    def __init__(self, text):
        """eagerly builds a list of all words in the text"""
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        for word in self.words:
            yield word


"""
A generator function builds a generator object that wraps the body of the function.
When we invoke next() on the generator, execution advances to the next yield in the
function body, and the the next() call evaluates to the value yielded when the function
body is suspended. Finally, when the function body returns, the enclosing generator object
raise StopIteration, in accordance with the Iterator prptocol.
"""


def genAB():
    """
    >>> res1 = [x*3 for x in genAB()]
    start
    continue
    end.
    >>> for i in res1:
    ...     print('-->', i)
    --> AAA
    --> BBB
    >>> res2 = (x*3 for x in genAB())
    >>> res2  # doctest: +ELLIPSIS
    <generator object <genexpr> at ...>
    >>> for i in res2:
    ...     print('-->', i)
    start
    --> AAA
    continue
    --> BBB
    end.
    """
    print('start')
    yield 'A'
    print('continue')
    yield 'B'
    print('end.')


class Sentence4:
    """Sentence implemented using a generator function calling
    the re.finditer generator function."""

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return 'Sentence (%s)' % reprlib.repr(self.text)

    def __iter__(self):
        """re.finditer is a lazy version of re.findall, which returns
        a generator producing re.MatchObject instances on demand.
        """
        return (match.group() for match in RE_WORD.finditer(self.text))


def d6():
    """
    iter can be called with two args, the frist arg is a callable to be
    invoked repeatedly to yield values, and the second arg is a sentinel:
    a marker value which when returned by the callable, causes the
    iterator to raise StopIteration instead of yielding the sentinel.

    >>> random.seed('7')
    >>> d6_iter = iter(d6, 3)
    >>> for roll in d6_iter:
    ...     print(roll)
    ...
    6
    5
    5
    2

    Read lines from a file until a blank line is found or the EOF is reached::

    >>> with open('./iterator_sentence.py') as fp:
    ...     for line in iter(fp.readline, 'import random'):
    ...         print(line)
    """
    return random.randint(1, 6)
