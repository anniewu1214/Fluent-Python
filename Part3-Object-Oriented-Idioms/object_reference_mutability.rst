======================
Object reference tests
======================

== versus is

``==`` compares the values of objects; ``is`` compares their identities, often
used to compare a variable to a singleton:

    >>> x = 1
    >>> x is None
    >>> x is not None


The relative immutability of tuples.

Tuples hold references to objects, if the referenced items are mutable, they may
change even if the tuple itself does not:

    >>> t1 = (1, 2, [30, 40])
    >>> t2 = (1, 2, [30, 40])
    >>> t1 == t2
    True
    >>> id_0 = id(t1[-1])
    >>> t1[-1].append(99)
    >>> id_0 == id(t1[-1])
    True
    >>> t1 == t2
    False


Copies are shallow by default

Using the constructor or [:] produces a shallow copy. The outmost container is duplicated,
but the copy is filled with references to the same item held by the original container:

    >>> l1 = [3, [66, 55, 44], (7, 8, 9)]
    >>> l2 = list(l1)
    >>> l1.append(100)
    >>> l1[1].remove(55)
    >>> print('l1:', l1)
    l1: [3, [66, 44], (7, 8, 9), 100]
    >>> print('l2:', l2)
    l2: [3, [66, 44], (7, 8, 9)]
    >>> l2[1] += [33, 22]
    >>> l2[2] += (10, 11)
    >>> print('l1:', l1)
    l1: [3, [66, 44, 33, 22], (7, 8, 9), 100]
    >>> print('l2:', l2)
    l2: [3, [66, 44, 33, 22], (7, 8, 9, 10, 11)]


Cyclic references:

    >>> a = [10, 20]
    >>> b = [a, 30]
    >>> a.append(b)
    >>> a
    [10, 20, [[...], 30]]
    >>> c = copy.deepcopy(a)
    >>> c
    [10, 20, [[...], 30]]


Parameters inside the function are aliases of the actual arguments. A function
may change any mutable objects it receieves:

    >>> def f(a, b):
    ...     a += b
    ...     return a
    ...
    >>> x, y = 1, 2
    >>> f(x, y)
    3
    >>> x, y
    (1, 2)
    >>> a = [1, 2]
    >>> b = [3, 4]
    >>> f(a, b)
    [1, 2, 3, 4]
    >>> a, b
    ([1, 2, 3, 4], [3, 4])
    >>> t=(10, 20)
    >>> u=(30, 40)
    >>> f(t, u)
    (10, 20, 30, 40)
    >>>t, u
    ((10, 20), (30, 40))


``del`` and garbage collection.

- ``del`` deletes names, not objects. An obj may be garbage collected as a result of a
``del`` command but only if the variable holds the last reference to the obj, or if the
obj becomes unreacheable.

- The presence of references is what keeps and object alive in memory.
When the reference count of an object reaches 0, the GC disposes of it:

    >>> import weakref
    >>> s1 = {1, 2, 3}
    >>> s2 = s1
    >>> def bye():
    ...     print('Gone with the wind...')
    >>> ender = weakref.finalize(s1, bye)
    >>> ender.alive
    True
    >>> del s1  # del deletes names, not objects
    >>> ender.alive
    True
    >>> s2 = 'spam'
    Gone with the wind...
    >>> ender.alive
    False


Weak references (WR)

- WR to an obj don't increase its reference count. The obj that is the
target of a reference is called the referent. A WR is a callable that
returns the referenced object or None if the referent is no more:

- the ``weakref.ref`` class is a low-level interface intended for advanced uses,
most programs are better served by the use of the weakref collections and finalize.
Consider using ``WeakKeyDictionary``, ``WeakValueDictionary``, ``WeakSet``, and
``finalize`` (which use weak references internally) instead of creating and
handling your own weak ref.ref instances by hand.

    >>> import weakref
    >>> a_set = {0, 1}
    >>> wref = weakref.ref(a_set)
    >>> wref()
    {0, 1}
    >>> a_set = {2, 3, 4}
    # a_set no longer refers to {0, 1}, but the _ variable still refers to it
    >>> wref()
    {0, 1}
    >>> wref() is None  # _ is now bound the the resulting False
    False
    >>> wref() is None  # there is no strong reference to {0, 1}
    True


- A tuple built from another using ``tuple()`` and ``[:]`` is actually the same exact tuple.

- Interning is used to share string literals.

    >>> l1 = [1, 2, 3]
    >>> l2 = list(l1)
    >>> l1 is l2
    False
    >>> l3 = l1[:]
    >>> l3 is l1
    False
    >>> t1 = (1, 2, 3)
    >>> t2 = tuple(t1)
    >>> t3 = t1[:]
    >>> t1 is t2
    True
    >>> t1 is t3
    True
    >>> s1 = 'ABC'
    >>> s2 = 'ABC'
    >>> s1 is s2
    True
