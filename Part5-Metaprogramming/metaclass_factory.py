"""
record_factory: create simple classes just for holding data fields

`type` is a class that creates a new class when invoked with three args:

    MyClass = type('MyClass', (MySuperClass, MyMixin),
                   {'x': 42, 'x2': lambda self: self.x * 2})

    <=>

    class MyClass(MySuperClass, MyMixin):
        x = 42

        def x2(self):
            return self.x * 2


In the real world, metaclasses are used in frameworks and libraries that performs:

    - attribute validation
    - apply to decorators to many methods at once
    - object serialization or data conversion
    - object-relational mapping
    - object-based persistency
    - dynamic translation of class structures from other languages


    >>> Dog = record_factory('Dog', 'name weight owner')
    >>> rex = Dog('Rex', 30, 'Bob')
    >>> rex
    Dog(name='Rex', weight=30, owner='Bob')
    >>> name, weight, _ = rex
    >>> name, weight
    ('Rex', 30)
    >>> "{2}'s dog weighs {1}kg".format(*rex)
    "Bob's dog weighs 30kg"
    >>> rex.weight = 32
    >>> rex
    Dog(name='Rex', weight=32, owner='Bob')
    >>> Dog.__mro__
    (<class 'factories.Dog'>, <class 'object'>)


The factory also accepts a list or tuple of identifiers:

    >>> Dog = record_factory('Dog', ['name', 'weight', 'owner'])
    >>> Dog.__slots__
    ('name', 'weight', 'owner')

"""


def record_factory(cls_name, field_names):
    """A simple class factory"""
    try:
        field_names = field_names.replace(',', ' ').split()
    except AttributeError:  # no .replace or .split
        pass  # assume it's already a sequence of identifiers
    field_names = tuple(field_names)

    def __init__(self, *args, **kwargs):
        """It will become the __init__ method in the new class"""
        attrs = dict(zip(self.__slots__, args))
        attrs.update(kwargs)
        for name, value in attrs.items():
            setattr(self, name, value)

    def __iter__(self):
        """yield the field values in the order given by __slots__"""
        for name in self.__slots__:
            yield getattr(self, name)

    def __repr__(self):
        values = ', '.join('{}={!r}'.format(*i) for i
                           in zip(self.__slots__, self))
        return '{}({})'.format(self.__class__.__name__, values)

    # Assemble dict of class attributes
    cls_attrs = dict(__slots__=field_names,
                     __init__=__init__,
                     __iter__=__iter__,
                     __repr__=__repr__)

    # build and return the new class
    return type(cls_name, (object,), cls_attrs)
