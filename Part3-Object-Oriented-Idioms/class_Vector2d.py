from array import array
from math import hypot, atan2, pi


class Vector2d:
    """
    A two-dimensional vector class

        >>> v1 = Vector2d(3, 4)
        >>> print(v1.x, v1.y)
        3.0 4.0
        >>> x, y = v1
        >>> x, y
        (3.0, 4.0)
        >>> v1
        Vector2d(3.0, 4.0)
        >>> print(v1)
        (3.0, 4.0)
        >>> octets = bytes(v1)
        >>> octets
        b'd\\x00\\x00\\x00\\x00\\x00\\x00\\x08@\\x00\\x00\\x00\\x00\\x00\\x00\\x10@'
        >>> abs(v1)
        5.0
        >>> bool(v1), bool(Vector2d(0, 0))
        (True, False)


    Test of ``.frombytes()`` class method:

        >>> v1_clone = Vector2d.frombytes(bytes(v1))
        >>> v1_clone
        Vector2d(3.0, 4.0)
        >>> v1 == v1_clone
        True



    Test of ``format()`` with Cartesian coordinates

        >>> format(v1)
        '(3.0, 4.0)'
        >>> format(v1, '.2f')
        '(3.00, 4.00)'
        >>> format(v1, '.3e')
        '(3.000e+00, 4.000e+00)'

    Tests of the ``angle`` method:

        >>> Vector2d(0, 0).angle()
        0.0
        >>> Vector2d(1, 0).angle()
        0.0
        >>> epsilon = 10**-8
        >>> abs(Vector2d(0, 1).angle() - pi/2) < epsilon
        True
        >>> abs(Vector2d(1, 1).angle() - pi/4) < epsilon
        True


    Tests of ``format()`` with polar coordinates:

        >>> format(Vector2d(1, 1), 'p')  # doctest: +ELLIPSIS
        '<1.414213..., 0.785398...>'
        >>> format(Vector2d(1, 1), '.3ep')
        '<1.414e+00, 7.854e-01>'
        >>> format(Vector2d(1, 1), '0.5fp')
        '<1.41421, 0.78540>'

    Tests of `x` and `y` read-only properties:

        >>> v1.x, v1.y
        (3.0, 4.0)
        >>> v1.x = 123
        Traceback (most recent call last):
          ...
        AttributeError: can't set attribute


    Tests of hashing:

        >>> v1 = Vector2d(3, 4)
        >>> v2 = Vector2d(3.1, 4.2)
        >>> hash(v1), hash(v2)
        (7, 384307168202284039)
        >>> len(set([v1, v2]))
        2

    Tests of name mangling:

        # >>> v1.__dict__  # slots used
        # {'_Vector2d_y': 4.0, '_Vector2d_x': 3,0}
        >>> v1._Vector2d__x
        3.0

    Test of class attribute overriding:

        >>> v1 = Vector2d(1.1, 2.2)
        >>> dumpd = bytes(v1)
        >>> dumpd
        b'd\x9a\x99\x99\x99\x99\x99\xf1?\x9a\x99\x99\x99\x99\x99\x01@'
        >>> len(dumpd)
        17
        >>> v1.typecode = 'f'
        >>> dumpf = bytes(v1)
        >>> dumpf
        b'f\xcd\xcc\x8c?\xcd\xcc\x0c@'
        >>> len(dumpf)
        9
        >>> Vector2d.typecode
        'd'

    """
    # By default, instance attrs are stored in a per-instance dict named __dict__
    # But dicts have significant memory overhead because of the underlying hash table
    # used. When dealing with millions of instances with few attrs, the __slots__
    # class attr can save a lot of memory.
    # these are all the instance attributes in this class
    __slots__ = ('__x', '__y')

    typecode = 'd'  # useful for converting Vector2d instances to/from bytes

    def __init__(self, x, y):
        """Name mangling: Python stores __x in the instance __dict__ as _Vector2d__x

        - float(x) helps to catch error early

        - use __ to make an attribute private

        - ``from mymod import *`` won't import names prefixed with _, however you
        can still write ``from mymod import _privatefunc``
        """

        self.__x = float(x)
        self.__y = float(y)

    @property  # @property marks the getter method of a property
    def x(self):  # the getter method is named after the public property it exposes: x
        return self.__x

    @property
    def y(self):
        return self.__y

    # iterable -> unpacking
    def __iter__(self):
        # <=> yield self.x; yield self.y
        return (i for i in (self.x, self.y))

    def __repr__(self):
        """By reading the name from the type of the instance, __repr__ is safe to inherit.
        If class_name is hardcoded, subclasses of Vector2d have to overwrite __repr__ just
        to change the class_name"""
        class_name = type(self).__name__
        # *self feeds the x and y components to format
        return '{}({!r}, {!r})'.format(class_name, *self)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) +
                bytes(array(self.typecode, self)))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        return hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def __hash__(self):
        # use the bitwise XOR operator ^ to mix the hashes of the components
        return hash(self.x) ^ hash(self.y)

    @classmethod
    def frombytes(cls, octets):
        """An alternative constructor that accepts a binary sequence"""
        typecode = chr(octets[0])
        # create a memoryview from the octets binary seq and use the typecode to cast it
        memv = memoryview(octets[1:]).cast(typecode)
        # unpack the memoryview into the pair of arguments needed for the constructor
        return cls(*memv)

    def __format__(self, format_spec):
        """
        ``format()`` and ``str.format()`` does the actual formatting by
        calling ``.__format__(format_spec)``, format_spec is either:

            - the second argument in format(my_obj, format_spec)
            - whatever appears after : in {} inside a format string

         If a class has no __format__, format falls back to __str__

        >>> brl = 1/2.43
        >>> brl
        0.4115226337448559
        >>> format(brl, '0.4f')
        '0.4115'
        >>> '1 BRL = {rate:0.2f} USD'.format(rate=brl)
        '1 BRL = 0.41 USD'
        >>> format(42, 'b')
        '101010'
        >>> format(2/3, '.1%')
        '66.7%'

        :param format_spec: the formatting specifier
        :return: formatted string
        """
        if format_spec.endswith('p'):
            format_spec = format_spec[:-1]
            coords = (abs(self), self.angle())
            outer_format = '<{}, {}>'
        else:
            coords = self
            outer_format = '({}, {})'
        components = (format(c, format_spec) for c in coords)
        return outer_format.format(*components)

    def angle(self):
        return atan2(self.y, self.x)


class ShortVector2d(Vector2d):
    """
    >>> sv = ShortVector2d(1/11, 1/27)
    >>> sv
    ShortVector2d(0.09090909090909091, 0.037037037037037035)
    >>> len(bytes(sv))
    9
    """
    typecode = 'f'


class ClassStaticMethodDemo:
    """
    Comparing behaviors of classmethod and staticmethod

    - classmethod operates on the class and not on the instances, so it's
      first argument is the class itself, insetead of an instance. Its
      most common use is for alternative constructors

    - staticmethod changes the method so that it receieves no special
      first argument. In essence, a static method is just like a plain
      function that happens to live in a class body, instead of being
      defined at the module level

    >>> ClassStaticMethodDemo.klassmeth()
    (<class 'class_Vector2d.ClassStaticMethodDemo'>,)
    >>> ClassStaticMethodDemo.klassmeth('spam')
    (<class 'class_Vector2d.ClassStaticMethodDemo'>, 'spam')
    >>> ClassStaticMethodDemo.staticmethod()
    ()
    >>> ClassStaticMethodDemo.staticmethod('spam')
    ('spam',)
    """

    @classmethod
    def klassmeth(*args):
        return args

    @staticmethod
    def staticmethod(*args):
        return args
