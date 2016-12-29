import keyword
from urllib.request import urlopen
import warnings
import os
import json
from collections import abc

URL = 'http://www.oreilly.com/pub/sc/osconfeed'
JSON = 'attribute_osconfeed.json'

"""
Data attributes and methods are known as attributes in Python: a method is
just an attribute that is callable. Properties can be used replace public data
attribute with accessor methods without changing the class interface.
"""


def load():
    """
    >>> feed = load()
    >>> sorted(feed['Schedule'].keys())
    ['conferences', 'events', 'speakers', 'venues']
    >>> for key, value in sorted(feed['Schedule'].items()):
    ...     print('{:3} {}'.format(len(value), key))
      1 conferences
    494 events
    357 speakers
     53 venues
    >>> feed['Schedule']['speakers'][-1]['name']
    'Carina C. Zona'
    >>> feed['Schedule']['speakers'][-1]['serial']
    141590
    >>> feed['Schedule']['events'][40]['name']
    'There *Will* Be Bugs'
    >>> feed['Schedule']['events'][40]['speakers']
    [3471, 5199]
    """
    if not os.path.exists(JSON):
        msg = 'downloading {} to {}'.format(URL, JSON)
        warnings.warn(msg)

        cwd = os.getcwd()
        # using two context managers to read the remote file and save it
        with urlopen(URL) as remote, open(cwd + '/' + JSON, 'wb') as local:
            local.write(remote.read())

    with open(JSON) as fp:
        # parses a JSON file and returns Python objects
        return json.load(fp)


class FrozenJSON:
    """
    A read-only facade for navigating a JSON-like object
    using attribute notation

    >>> raw_feed = load()
    >>> feed = FrozenJSON(raw_feed)
    >>> len(feed.Schedule.speakers)
    357
    >>> sorted(feed.Schedule.keys())
    ['conferences', 'events', 'speakers', 'venues']
    >>> for key, value in sorted(feed.Schedule.items()):
    ...     print('{:3} {}'.format(len(value), key))
      1 conferences
    494 events
    357 speakers
     53 venues
    >>> feed.Schedule.speakers[-1].name
    'Carina C. Zona'
    >>> talk = feed.Schedule.events[40]
    >>> type(talk)
    <class 'attribute_osconfeed.FrozenJSON'>
    >>> talk.name
    'There *Will* Be Bugs'
    >>> talk.speakers
    [3471, 5199]
    >>> talk.flavor
    Traceback (most recent call last):
    ...
    KeyError: 'flavor'
    """

    def __init__(self, mapping):
        self.__data = {}
        # append a _ to attribute names that are Python keywords
        for key, value in mapping.items():
            if keyword.iskeyword(key):
                key += '_'
            self.__data[key] = value

    def __getattr__(self, name):
        """
        only invoked when the usual process fails to retrieve an attribute.
        i.e. when the named attribute cannot be found in the instance, nor
        in the class or its superclass.

        first look if the self.__data dict has an attribute (not a key!) by
        that name; this allows to handle any dict method such as items, by
        delegating to self.__data.items()

        build allows navigating through nested structures in the JSON data,
        as each nested mapping is converted to another FronzenJSON instance
        """
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return FrozenJSON.build(self.__data[name])

    @classmethod
    def build(cls, obj):
        # if obj is a mapping, build a FrozenJSON with it
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        # if obj is a MutableSequence, build a list by passing every
        # item in obj recursively to .build()
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
        # otherwise, return the item as it is
        else:
            return obj


class FrozenJSONnew:
    """
    __new__ must return an instance, that will be passed as the first arg self of __init__;
    when __new__ returns an instance of a different class, __init__ is not called

    __new__ gets the class as the first arg, because usually the created obj will be an
    instance of that class
    """
    def __new__(cls, arg):
        # the default behavior is to delegate to the __new__ of a super class
        if isinstance(arg, abc.Mapping):
            return super().__new__(cls)
        elif isinstance(arg, abc.MutableSequence):
            return [cls(item) for item in arg]
        else:
            return arg

    def __init__(self, mapping):
        self.__data = {}
        for key, value in mapping.items():
            if keyword.iskeyword(key):
                key += '_'
            self.__data[key] = value

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return FrozenJSONnew(self.__data[name])
