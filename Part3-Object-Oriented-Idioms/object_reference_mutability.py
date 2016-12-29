class Bus:
    """Effects of using copy versus deepcopy

    >>> import copy
    >>> bus1 = Bus(['Alice', 'Bill', 'Claire', 'David'])
    >>> bus2 = copy.copy(bus1)
    >>> bus3 = copy.deepcopy(bus1)
    >>> bus1.drop('Bill')
    >>> bus2.passengers
    ['Alice', 'Claire', 'David']
    >>> bus3.passengers
    ['Alice', 'Bill', 'Claire', 'David']
    """

    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            # the passengers argument can be any iterable, because the list constructor
            # accepts any iterable. And it ensures that it supports .remove() and .appennd()
            self.passengers = list(passengers)

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)


class HauntedBus:
    """Mutable types as parameter defaults: bad idea

    The problem is that each default value is evaluated when the function is
    defined, usually when the module is loaded, and the default values become
    attributes of the function object.

    None is often used as the default value for parameters that may receieve
    mutable values.

    >>> bus1 = HauntedBus(['Alice', 'Bill'])
    >>> bus1.passengers
    ['Alice', 'Bill']
    >>> bus1.pick('Charlie')
    >>> bus1.drop('Alice')
    >>> bus1.passengers
    ['Bill', 'Charlie']
    >>> bus2 = HauntedBus()
    >>> bus2.pick('Carrie')
    >>> bus2.passengers
    ['Carrie']
    >>> bus3 = HauntedBus()
    >>> bus3.passengers
    ['Carrie']
    >>> bus3.pick('Dave')
    >>> bus2.passengers
    ['Carrie', 'Dave']
    >>> bus2.passengers is bus3.passengers
    True
    >>> bus1.passengers
    ['Bill', 'Charlie']
    >>> dir(HauntedBus.__init__)  # doctest: +ELLIPSIS
    ['__annotations__', '__call__', ..., '__defaults__', ...]
    >>> HauntedBus.__init__.__defaults__
    (['Carrie', 'Dave'],)
    >>> HauntedBus.__init__.__defaults__[0] is bus2.passengers
    True
    """

    def __init__(self, passengers=[]):
        """This assignment makes self.passengers an alias for passengers, which
        is itself an alias for the default list, when no passnegers arg is given."""
        self.passengers = passengers

    def pick(self, name):
        """.remove() and .append() are actually mutating the default list."""
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)


class TwilightBus:
    """A bus model that makes passengers vanish

    >>> basketball_team = ['Sue', 'Tina', 'Maya', 'Diana', 'Pat']
    >>> bus = TwilightBus(basketball_team)
    >>> bus.drop('Tina')
    >>> bus.drop('Pat')
    >>> basketball_team
    ['Sue', 'Maya', 'Diana']
    """

    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            # this assignment make self.passengers an alias for passengers, which
            # is itself an alias for the actual arg passed to __init__
            self.passengers = passengers

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)


class Cheese:
    """
    WeakValueDictionay: values are weak references to objects, when a referred object
    is garbage collected in the program, the corresponding key is automatically removed.
    This is commonly used for caching.

    >>> import weakref
    >>> stock = weakref.WeakValueDictionary()
    >>> catalog = [Cheese('Red Leicester'), Cheese('Tilsit'), Cheese('Parmesan')]
    >>> for cheese in catalog:
    ...     stock[cheese.kind] = cheese
    ...
    >>> sorted(stock.keys())
    ['Parmesan', 'Red Leicester', 'Tilsit']
    >>> del catalog
    >>> sorted(stock.keys())
    ['Parmesan']
    >>> del cheese
    >>> sorted(stock.keys())
    []
    """

    def __init__(self, kind):
        self.kind = kind

    def __repr__(self):
        return 'Cheese(%r)' % self.kind
