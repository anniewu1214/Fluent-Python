"""Build an index mapping word -> list of occurrences"""
import collections
import sys
import re

WORD_RE = re.compile('\w+')

"""
setdefault gets the list of occurences for word, or set it to [] if not found;
it then returns the value, so it can be updated without requiring a second search.
"""
# setdefault
index = {}
with open(sys.argv[1], encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1):
        for match in WORD_RE.finditer(line):
            word = match.group()
            column_no = match.start() + 1
            location = (line_no, column_no)
            # this is ugly
            # occurences = index.get(word, [])
            # occurences.append(location)
            # index[word] = occurences
            index.setdefault(word, []).append(location)

"""
Sometimes it is convenient to have mappings that return some made-up value when a
missing key is searched. One approach is to use a ``defaultdict``, the other is to
subclass dict or other mapping type and add a __missing__ method.

When instiatiating a defaultdict, provide a callable that is used to produce
a default value when __getitem__ is passed a nonexistant key argument.
"""
# collections.defaultdict
index = collections.defaultdict(list)
with open(sys.argv[1], encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1):
        for match in WORD_RE.finditer(line):
            word = match.group()
            column_no = match.start() + 1
            location = (line_no, column_no)
            index[word].append(location)

# print in alphabetical order
for word in sorted(index, key=str.upper):
    print(word, index[word])


class StrKeyDict0(dict):
    """
    When searching for a nonstring key, StrKeyDict0 converts
    it to str when it is not found.

    __missing__ method is just called by __getitem__ whenever a key
    is not found, instead of raising KeyError.

    A better-way to create a user-defined mapping type is to subclass
    UserDict instead of dict, we subclass dict just to show that __missing
    is supported by the build-in dict.__getitem__ method.

    Tests for item retrivial using `d[key]` notation::

        >>> d = StrKeyDict0([('2', 'two'), ('4', 'four')])
        >>> d['2']
        'two'
        >>> d[4]
        'four'
        >>> d[1]
        Traceback (most recent call last):
        ...
        KeyError: '1'

    Tests for item retrieval using `d.get(key)` notation::

         >>> d.get('2')
         'two'
         >>> d.get(4)
         'four'
         >>> d.get(1, 'N/A')
         'N/A'

    Tests for the `in` operator::

        >>> 2 in d
        True
        >>> 4 in d
        False
    """

    def __contains__(self, item):
        # item in self => infinite recursion
        return item in self.keys() or str(item) in self.keys()

    def __missing__(self, key):
        # without the if test => infinite recursion
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def get(self, key, d=None):
        try:
            # delegates to __getitem__ to benefit from __missing__
            return self[key]
        except KeyError:
            return d


class StrKeyDict(collections.UserDict):
    """
    StrKeyDict always converts non-string keys to str - on
    insertion, update, and lookup.

    It's preferable to subclass UserDict, because the build-in has some
    implementation shortcuts that end up forcing us to override methods
    that we can just inherit from UserDict with no problems.

    Because UserDict subclasses MutableMapping, the remaining methods that make
    StrKeyDict a full-fledged mapping are inherited from UserDict, MutableMapping
    or Mapping, including:

    - MutableMapping.update: update with items from mapping or iterable of (key, val)
    pairs. It uses self[key] = value to add items, and calls __setitem__

    - Mapping.get: In StrKeyDict, we had to code get to obtain results consistent
    with __getitem__, but here we inherited Mapping.get which is implemented
    exactly like StrKeyDict0.get
    """

    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def __contains__(self, item):
        return str(item) in self.data

    def __setitem__(self, key, value):
        """
        UserDict does not inherit from dict, but has an internal dict instance
        called ``data``, that holds the actual items. This avoids undesired
        recursion when coding special methods like __setitem__."""
        self.data[str(key)] = value
