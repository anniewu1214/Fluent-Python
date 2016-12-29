import itertools
import numbers

from abc_tombola import BingoCage, Tombola
from class_Vector import Vector


class Vector2(Vector):
    """
    Operator Overloading:
    - We cannot overload operators for the built-in types
    - We cannot create new operators, only overload existing ones
    - A few operatos cannot be overloaded: is, and, or ,not.

    Unary operator tests::
    Unary and infix operators should produce results by creating new objects,
    and should never change their operands

        >>> v1 = Vector2([3, 4])
        >>> abs(v1)
        5.0
        >>> -v1
        Vector([-3.0, -4.0])
        >>> +v1
        Vector([3.0, 4.0])


    Basic tests of operator ``+``::

        >>> v1 = Vector2([3, 4, 5])
        >>> v2 = Vector2([6, 7, 8])
        >>> v1 + v2
        Vector([9.0, 11.0, 13.0])
        >>> v1 + v2 == Vector2([3+6, 4+7, 5+8])
        True
        >>> v3 = Vector2([1, 2])
        >>> v1 + v3  # short Vector2s are filled with 0.0 on addition
        Vector([4.0, 6.0, 5.0])


    Tests of ``+`` with mixed types::

        >>> v1 + (10, 20, 30)
        Vector([13.0, 24.0, 35.0])
        >>> from class_Vector2d import Vector2d
        >>> v2d = Vector2d(1, 2)
        >>> v1 + v2d
        Vector([4.0, 6.0, 5.0])


    Tests of ``+`` with mixed types, swapped operands::

        >>> (10, 20, 30) + v1
        Vector([13.0, 24.0, 35.0])
        >>> v2d = Vector2d(1, 2)
        >>> v2d + v1
        Vector([4.0, 6.0, 5.0])


    Tests of ``+`` with an unsuitable operand:

        >>> v1 + 1
        Traceback (most recent call last):
          ...
        TypeError: unsupported operand type(s) for +: 'Vector2' and 'int'
        >>> v1 + 'ABC'
        Traceback (most recent call last):
          ...
        TypeError: unsupported operand type(s) for +: 'Vector2' and 'str'


    Basic tests of operator ``*``::

        >>> v1 = Vector2([1, 2, 3])
        >>> v1 * 10
        Vector([10.0, 20.0, 30.0])
        >>> 10 * v1
        Vector([10.0, 20.0, 30.0])


    Tests of ``*`` with unusual but valid operands::

        >>> v1 * True
        Vector([1.0, 2.0, 3.0])
        >>> from fractions import Fraction
        >>> v1 * Fraction(1, 3)  # doctest:+ELLIPSIS
        Vector([0.3333..., 0.6666..., 1.0])


    Tests of ``*`` with unsuitable operands::

        >>> v1 * (1, 2)
        Traceback (most recent call last):
          ...
        TypeError: can't multiply sequence by non-int of type 'Vector2'


    Tests of operator `==`.
    Rich comparison operators never generate errors because Python
    compares the object id as a last resort::


        >>> va = Vector2(range(1, 4))
        >>> vb = Vector2([1.0, 2.0, 3.0])
        >>> va == vb
        True
        >>> vc = Vector2([1, 2])
        >>> v2d = Vector2d(1, 2)
        >>> vc == v2d
        True
        >>> va == (1, 2, 3)
        False


    Tests of operator `!=`::

        >>> va != vb
        False
        >>> vc != v2d
        False
        >>> va != (1, 2, 3)
        True

    Test of augmented assignment operators::

    - If a class does not implement the in-place operator, ``a += b`` is evaluated
      as ``a = a + b``. If __iadd__ is implemented, it is used to compute the result
      of ``a += b``. Those operators are expected to change the lefthand operand
      in place, and not create a new object as the result.

    - the in-place special methods should never be implemented for immutable types like
      our Vector2 class.

        >>> v1 = Vector2([1, 2, 3])
        >>> v1_alias = v1
        >>> v1 += Vector2([4, 5, 6])
        >>> v1
        Vector([5.0, 7.0, 9.0])
        >>> v1_alias
        Vector([1.0, 2.0, 3.0])
        >>> v1 *= 11
        >>> v1
        Vector([55.0, 77.0, 99.0])
    """

    def __neg__(self):
        """always return a new object, do not modify self"""
        return Vector2(-x for x in self)

    def __pos__(self):
        return Vector2(self)

    def __add__(self, other):
        """
        Computing a + b with __add__ and __radd__:
        1. If a has __add__, call a.__add__(b) and return result unless it's NotImplemented
        2. If a doesn't have __add__, or calling it returns NotImplemented, check if b has
        __radd__, then call b.__radd__(a) and return result unless it's NotImplemented
        3. If b doesn't have __add__, or calling it returns NotImplemented, raise TypeError.

        If an operator method cannot return a valid result because of type incompatibility,
        it should return NotImplemented and not raise TypeError. This allows the interpreter
        to try calling the reversed operator method, which may correctly handle it.
        """
        try:
            pairs = itertools.zip_longest(self, other, fillvalue=0.0)
            return Vector2(a + b for a, b in pairs)
        except TypeError:
            return NotImplemented

    def __radd__(self, other):
        """
        - If not defined, augmented assignment operators are just syntactic sugar: a += b is
        evaluated as a = a + b.

        - If __iadd__ is implemented, it is called to compute a += b. In-place operators are
        expected to change the lefthand operand in place, and not create a new object.

        - In-place special methods should never be implemented for immutable types like Vector2.
        """
        return self + other

    def __mul__(self, scalar):
        """Operator overloading is one area where isinstance tests are common.
        In general, libraries should leverage dynamic typing - to be more flexible -
        by avoiding explicit type tests and just trying operations and then handling
        the exceptions, opening the door for working with objects regardless of their
        types, as long as they support the necessary operations.
        """
        if isinstance(scalar, numbers.Real):
            return Vector2(n * scalar for n in self)
        else:
            return NotImplemented

    def __rmul__(self, scalar):
        return self * scalar

    def __matmul__(self, other):
        try:
            return sum(a * b for a, b in zip(self, other))
        except TypeError:
            return NotImplemented

    def __rmatmul__(self, other):
        return self @ other


class AddableBingoCage(BingoCage):
    """
    AddableBingoCage extends BingoCage to support + and +=

    __add__: the result is produced by calling the constructor
    AddableBingoCage to build a new instance

    __iadd__: the result is produced by returning self, ater
    it has been modified

    >>> vowels = "AEIOU"
    >>> globe = AddableBingoCage(vowels)
    >>> globe.inspect()
    ('A', 'E', 'I', 'O', 'U')
    >>> globe.pick() in vowels
    True
    >>> len(globe.inspect())
    4
    >>> globe2 = AddableBingoCage('XYZ')
    >>> globe3 = globe + globe2
    >>> len(globe3.inspect())
    7
    >>> void = globe + [10, 20]
    Traceback (most recent call last):
        ...
    TypeError: unsupported operand type(s) for +: 'AddableBingoCage' and 'list'
    >>> globe_origin = globe
    >>> len(globe.inspect())
    4
    >>> globe += globe2
    >>> len(globe.inspect())
    7
    >>> globe += ['M', 'N']
    >>> len(globe.inspect())
    9
    >>> globe is globe_origin
    True
    >>> globe += 1
    Traceback (most recent call last):
        ...
    TypeError: right operand in += must be 'AddableBingoCage' or an iterable
    """

    def __add__(self, other):
        """
        - __add__ will only work with an instance of Tombola as the 2nd operand

        - In general, if a forward infix operator method is designed to work with
          operands of the same type as self, it's useless to implement the
          corresponding reverse method, because that, by definition, will only
          be invoked when dealing with an operand of a different type.
        """
        if isinstance(other, Tombola):
            return AddableBingoCage(self.inspect() + other.inspect())
        else:
            return NotImplemented

    def __iadd__(self, other):
        """Very important! augmented assignment special methods must return self"""
        if isinstance(other, Tombola):
            other_iterable = other.inspect()
        else:
            try:
                # try to obtain an iterator over other
                other_iterable = iter(other)
            except TypeError:
                self_cls = type(self).__name__
                msg = "right operand in += must be {!r} or an iterable"
                raise TypeError(msg.format(self_cls))
        self.load(other_iterable)
        return self
