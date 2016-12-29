import abc
import random


class Tombola(abc.ABC):
    """
    Subclass anc.ABC to define an ABC

    With goose typing, ABCs are used to make interfaces explicit
    and classes claim to implement an interface by subclassing
    and ABC or by registering with it -- without requring
    the strong and static link of an inheritance relationship.
    """

    @abc.abstractmethod
    def load(self, iterable):
        """
        - An abstract method is marked with the @abstractmethod decorator,
        and often its body is empty except for a docstring.

        - An abstract method can have an implementation, even then subclasses
        are still forced to override it.

        Add items from an iterable."""

    @abc.abstractmethod
    def pick(self):
        """Remove item at random, returning it.

        This method should raise `LookupError` when the instance is empty
        """

    def loaded(self):
        """An ABC may include concrete methods, they must rely only on the
        interface defined by the ABC.

        Return `True` if there's at least 1 item, False otherwise"""
        return bool(self.inspect())

    def inspect(self):
        """Return a sorted tuple with the items currently inside"""
        items = []
        while True:
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)
        return tuple(sorted(items))


class BingoCage(Tombola):
    def __init__(self, items):
        self._randomizer = random.SystemRandom()
        self._items = []
        self.load(items)

    def load(self, iterable):
        self._items.extend(iterable)
        self._randomizer.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')

    def __call__(self):
        self.pick()


class LotteryBlower(Tombola):
    def __init__(self, iterable):
        self._balls = list(iterable)

    def load(self, iterable):
        self._balls.extend(iterable)

    def pick(self):
        try:
            position = random.randrange(len(self._balls))
        except ValueError:
            raise LookupError('pick from empty LotteryBlower')
        return self._balls.pop(position)

    def loaded(self):
        return bool(self._balls)

    def inspect(self):
        return tuple(sorted(self._balls))


@Tombola.register
class TomboList(list):
    """
    - TomboList is registered as a virtual subclass of Tombola. This will be
    recognized as such by functioins like issubclass and isinstance, but it
    will not inherit any methods or attributes from the ABC

    - inherits __bool__ from list, and that returns True is the list is not empty

    - register in practice: widely deployed as a function to register classes
    defined elsewhere. Built-in types tuple, str, range are registered
    as virtual subclasses of Sequence like this: Sequence.register(tuple),
    Sequence.register(str), Sequence.register(range)


    >>> issubclass(TomboList, Tombola)
    True
    >>> t = TomboList(range(100))
    >>> isinstance(t, Tombola)
    True
    >>> TomboList.__mro__
    (<class 'abc_tombola.TomboList'>, <class 'list'>, <class 'object'>)
    """

    def pick(self):
        if self:
            position = random.randrange(len(self))
            return self.pop(position)
        else:
            raise LookupError('pick from empty TomboList')

    load = list.extend

    def loaded(self):
        return bool(self)

    def inspect(self):
        return tuple(sorted(self))
