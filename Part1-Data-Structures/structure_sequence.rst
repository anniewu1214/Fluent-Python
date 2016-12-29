======================
Python Data Structures
======================

=========== Tuples unpacking ============


Defining function parameters with *arg to grab arbitrary excess args:

    >>> a, b, *rest = range(5)
    >>> a, b, rest
    (0, 1, [2, 3, 4])
    >>> a, b, *rest = range(3)
    >>> a, b, rest
    (0, 1, [2])
    >>> a, b, *rest = range(5)
    >>> a, b, rest
    (0, 1, [])


* can appear in any position:

    >>> a, *body, c, d = range(5)
    >>> a, body, c, d
    (0, [1, 2], 3, 4)
    >>> *head, b, c, d = range(5)
    >>> head, b, c, d
    ([0, 1], 2, 3, 4)


Nested tuple unpacking:

    >>> metro_areas = [
    ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),   # <1>
    ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
    ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
    ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
    ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833))]

    >>> print('{:15} | {:^9} | {:^9}'.format('', 'lat.', 'long.'))
    >>> fmt = '{:15} | {:9.4f} | {:9.4f}'
    >>> for name, cc, pop, (latitude, longitude) in metro_areas:  # <2>
    ...     if longitude <= 0:  # <3>
    ...         print(fmt.format(name, latitude, longitude))
    ...
                    |   lat.    |   long.
    Mexico City     |   19.4333 |  -99.1333
    New York-Newark |   40.8086 |  -74.0204
    Sao Paulo       |  -23.5478 |  -46.6358


 ============ Slices and +/* ============


 Assigning to slices:

    >>> l = list(range(10))
    >>> l[2:5] = [20, 30]
    >>> l
    [0, 1, 20, 30, 5, 6, 7, 8, 9]
    >>> del l[5:7]
    >>> l
    [0, 1, 20, 30, 5, 8, 9]
    >>> l[2:5] = 100  # doctest: +ELLIPSIS
    Traceback (most recent call last):...
    >>> l[2:5] = [100]
    >>> l
    [0, 1, 100, 8, 9]


Using + and * with sequences:

    >>> l = [1, 2, 3]
    >>> l * 5
    [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]
    >>> 5 * 'abcd'
    'abcdabcdabcdabcdabcd'
    >>> board = [['_'] * 3 for i in range(3)]
    >>> board
    [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
    >>> board[1][2] = 'X'
    >>> board
    [['_', '_', '_'], ['_', '_', 'X'], ['_', '_', '_']]
    >>> weird_board = [['_'] * 3] * 3
    >>> weird_board[1][2] = 'O'
    >>> weird_board
    [['_', '_', 'O'], ['_', '_', 'O'], ['_', '_', 'O']]



============ augmented assignments  ============


Augmented assignment with sequences. __iadd__ makes += workd, if it is not
implemented, Python falls back to calling __add__:

    >>> l = [1, 2, 3]
    >>> id0 = id(l)
    >>> l *= 2
    >>> id(l) == id0
    True
    >>> t = (1, 2, 3)
    >>> id0 = id(t)
    >>> t *= 2
    >>> id0 == id(t)
    False
    >>> t=(1, 2, [30,40])
    >>> t[2] += [50, 60]  # doctest: +ELLIPSIS
    Traceback (most recent call last):...
    >>> t
    (1, 2, [30, 40, 50, 60])



============ list.sort and sorted ============

list.sort and the sorted build-in function. list.sort sorts a list in place, and
it returns None to remaind us that it changes the target object, and does not create
a new list. sorted creates a new list regardless of the type of the iterabe given:

    >>> fruits = ['grape', 'raspberry', 'apple', 'banana']
    >>> sorted(fruits)
    ['apple', 'banana', 'grape', 'raspberry']
    >>> fruits
    ['grape', 'raspberry', 'apple', 'banana']
    >>> sorted(fruits, reverse=True)
    ['raspberry', 'grape', 'banana', 'apple']
    >>> sorted(fruits, key=len)
    ['grape', 'apple', 'banana', 'raspberry']
    >>> sorted(fruits, key=len, reverse=True)
    ['raspberry', 'banana', 'grape', 'apple']
    >>> fruits
    ['grape', 'raspberry', 'apple', 'banana']
    >>> fruits.sort()
    >>> fruits
    ['apple', 'banana', 'grape', 'raspberry']


============ bisect and insort ============


bisect finds insertions points for items in a sorted sequence: ``bisect(haystack, needle)``
bisect is an alias for bisect_right, there's also bisect_left, the difference occurs when
the needle equals to an item:

    >>> import bisect
    >>> def grade(score, breakpoints=[60, 70, 80, 90], grades='FDCBA'):
    ...     i = bisect.bisect(breakpoints, score)
    ...     return grades[i]
    ...
    >>> [grade(score) for score in [33, 99, 77, 70, 89, 90, 100]]
    ['F', 'A', 'C', 'C', 'B', 'A', 'A']


insort(seq, item) inserts item into seq so as to keep seq in ascending order:

    >>> import random
    >>> SIZE = 7
    >>> random.seed(1729)
    >>> my_list = []
    >>> for i in range(SIZE):
    ...     new_item = random.randrange(SIZE*2)
    ...     bisect.insort(my_list, new_item)
    ...     print('%2d ->' % new_item, my_list)



============ When a list is not the answer  ============


array - store 10 million floating-point values
deque - constantly adding or removing items from the ends of a list
set - a lot of containment checks


Arrays: If the list only contains numbers, an array.array is more efficient
than a list: it supports all mutable sequence operations, and additional
methods for fast loading and saving such as .frombytes and .tofile.

Creating, saving, and loading a large array of floats:

    >>> from arrary import array
    >>> from random import random
    >>> floats = array('d', (random() for i in range(10**6)))
    >>> fp = open('floats.bin', 'wb')
    >>> floats.tofile(fp)
    >>> fp.close()
    >>> floats2 = array('d')
    >>> fp = open('floats.bin', 'rb')
    >>> floats2.fromfile(fp, 10**6)
    >>> fp.close()
    >>> floats == floats2
    True

Saving an array of floats with pickle.dump is as fast as with array.tofile, pickle
handles almost all build-in types, including complex numbers, nested collections,
and even instances of classes.



============ deque ============


collections.deque is double-ended queue designed for inserting and removing from both ends.

    >>> from collections import deque
    >>> dq = deque(range(10), maxlen=10)
    >>> dq
    deque([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], maxlen=10)
    >>> dq.rotate(3)
    >>> dq
    deque([7, 8, 9, 0, 1, 2, 3, 4, 5, 6], maxlen=10)
    >>> dq.rotate(-4)
    >>> dq
    deque([1, 2, 3, 4, 5, 6, 7, 8, 9, 0], maxlen=10)
    >>> dq.appendleft(-1)
    >>> dq
    deque([-1, 1, 2, 3, 4, 5, 6, 7, 8, 9], maxlen=10)
    >>> dq.extend([11, 22, 33])
    >>> dq
    deque([3, 4, 5, 6, 7, 8, 9, 11, 22, 33], maxlen=10)
    >>> dq.extendleft([10, 20, 30, 40])
    >>> dq
    deque([40, 30, 20, 10, 3, 4, 5, 6, 7, 8], maxlen=10)



============ Dictionary ============

ways to build dict:

    >>> a = dict(one=1, two=2, three=3)
    >>> b = {'one': 1, 'two': 2, 'three': 3}
    >>> c = dict(zip(['one', 'two', 'three'], [1, 2, 3]))
    >>> d = dict([('one', 1), ('two', 2), ('three', 3)])
    >>> e = dict({'one': 1, 'two': 2, 'three': 3})
    >>> a == b == c == d == e
    True


============ Set ============

Use set to remove duplication

    >>> l = ['spam', 'spam', 'eggs', 'spam']
    >>> set(l)
    {'eggs', 'spam'}
    >>> list(set(l))
    ['eggs', 'spam']

Given two sets a and b, a | b returns their union, a & b is
the intersection, and a - b the difference.

Literal set syntax like {1, 2} is both faster and more readable
then calling the constructor set([1, 2])



============ Practical consequences of how dict works ============

1. Keys must be hashable objects.

    - user-defined types are hashable by default because their hash value
    is their id() and they all compare not equal
    - __eq__ and __hash__ must be implemented at the same time, because
    if a == b is True then hash(a) == hash(b) must be True too.

2. dicts have significant memory overhead.

    - dict uses a hash table internally, and it must be sparse to work,
    they are not space efficient.
    - for user-defined types, the __slots__ class attr changes the storage
    of instance attributes from a dict to a tuple in each instance.

3. Key search is very fast.

    - dict is an example of trading space for time: significant memory overhead,
    but fast access regardless of the size of the dict.

4. Key ordering depends on insertion order

    - when a hash collision happens, the second key ends up in a position that it
    would not normally occupy if it had been inserted first. So, a dict built as
    dict([(key1, value1), (key2, value2)]) compares equal to dict([(key2, value2),
    (key1, value1)]), but their key ordering may not be the same if the hashes of
    key1 and key2 collide.


5. Adding items to a dict may change the order of existing keys.

    - when adding a new item to a dict, Python may decide that the hash table needs
    to grow, this entails building a new, bigger hash table, and adding all current
    items to the new table. During this process, new hash collisions may happen, and
    the keys are likely to be ordered differently in the new hash table.

    - thus modifying the contents of a dict while iterating through it is a bad idea.



============ Practical consequences of how set works ============

1. Set elements must be hashable objects.
2. Sets have a significant memory overhead.
3. Membership testing is very efficient.
4. Element ordering depends on insertion order.
5. Adding elements to a set may change the order of other elements.

