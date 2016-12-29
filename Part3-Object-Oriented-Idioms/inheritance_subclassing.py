"""
Subclassing builtin types like ``dict``, `list`` or ``str`` directly is
error-prone because the built-in methods mostly ignore user-defined overrides.
Derive your class from the ``collections`` module using ``UserDict``,
``UserList``, ``UserString``, which are designed to be easily extended.
"""

import collections


class DoppelDict(dict):
    """
    __setitem__ override is ignored by the __init__ and __update__
    methods of the built-in dict

    >>> dd = DoppelDict(one=1)
    >>> dd
    {'one': 1}
    >>> dd['two'] = 2
    >>> dd
    {'two': [2, 2], 'one': 1}
    >>> dd.update(three=3)
    >>> dd
    {'three': 3, 'two': [2, 2], 'one': 1}
    """

    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)


class AnswerDict(dict):
    """
    __getitem__ override is ignored by dict.update

    >>> ad = AnswerDict(a='foo')
    >>> ad['a']
    42
    >>> d = {}
    >>> d.update(ad)
    >>> d['a']
    'foo'
    >>> d
    {'a': 'foo'}
    """

    def __getitem__(self, item):
        return 42


class DoppelDict2(collections.UserDict):
    """
    Work as expected

    >>> dd = DoppelDict2(one=1)
    >>> dd
    {'one': [1, 1]}
    >>> dd['two'] = 2
    >>> dd
    {'two': [2, 2], 'one': [1, 1]}
    >>> dd.update(three=3)
    >>> dd
    {'three': [3, 3], 'two': [2, 2], 'one': [1, 1]}
    """

    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)


class AnswerDict2(collections.UserDict):
    """
    Work as expected

    >>> ad = AnswerDict2(a='foo')
    >>> ad['a']
    42
    >>> d = {}
    >>> d.update(ad)
    >>> d['a']
    42
    >>> d
    {'a': 42}
    """

    def __getitem__(self, item):
        return 42
