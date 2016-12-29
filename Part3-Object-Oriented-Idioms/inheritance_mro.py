class A:
    def ping(self):
        print('ping:', self)


class B(A):
    def pong(self):
        print('pong:', self)


class C(A):
    def pong(self):
        print('PONG:', self)


class D(B, C):
    """
    MRO: Method Resolution Order. Classes have an attribute called
    __mro__ holding a tuple of references to the superclasses in MRO
    order, from the current class all the way to the object class.

    >>> d = D()
    >>> d.pingpong()  # doctest: ELLIPSIS
    ping: ...
    post-ping ...
    ping: ...
    pong: ...
    pong: ...
    PONG: ...
    >>> D.__mro__
    (<class 'inheritance_mro.D'>, <class 'inheritance_mro.B'>, <class 'inheritance_mro.C'>,
    <class 'inheritance_mro.A'>, <class 'object'>)

    >>> def print_mro(cls):
    ...     print(', '.join(c.__name__ for c in cls.__mro__))
    ...
    >>> print_mro(bool)
    bool, int, object
    >>> from structure_frenchdeck import FrenchDeck2
    >>> print_mro(FrenchDeck2)
    FrenchDeck2, MutableSequence, Sequence, Sized, Iterable, Container, object
    >>> import numbers
    >>> print_mro(numbers.Integral)
    Integral, Rational, Real, Complex, Number, object
    >>> import io
    >>> print_mro(io.BytesIO)
    BytesIO, _BufferedIOBase, _IOBase, object
    """

    def ping(self):
        super().ping()
        print('post-ping', self)

    def pingpong(self):
        self.ping()
        super().ping()
        self.pong()
        super().pong()
        C.pong(self)
