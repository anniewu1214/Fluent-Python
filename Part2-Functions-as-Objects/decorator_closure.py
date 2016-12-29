"""
Variable scope rules: a variable assigned in the body of a function is local.


    When compiling the body of f, Python decides that vairable b is local, because
    it is assigned within the function. Later, when f(3) is called, the body of
    f fetches and prints the value of the local variable a, but when trying to
    fetch the value of local variable b it discovers that b is unbound.

        >>> b = 6
        >>> def f(a):
        ...     print(a)
        ...     print(b)
        ...     b = 9
        ...
        >>> f(3)  # IGNORE_EXCEPTION_DETAIL
        3
        UnboundLocalError: local variable 'b' referenced before assignment


    Use the ``global`` declaration to treat b as a global variable.

        >>> b = 6
        >>> def f(a):
        ...     global b
        ...     print(a)
        ...     print(b)
        ...     b = 9
        ...
        >>> f(3)
        3
        6
        >>> b
        9
"""


# object oriented
class Averager:
    """
    avg is a callable instance of Average
    >>> avg = Averager()
    >>> avg(10)
    10.0
    >>> avg(11)
    10.5
    >>> avg(12)
    11.0
    """

    def __init__(self):
        self.series = []

    def __call__(self, val):
        self.series.append(val)
        total = sum(self.series)
        return total / len(self.series)


# higher-order function
def make_averager():
    """
    A closure is a function with an extended scope that encompasses nonglobal
    variables referenced in the body of the function but not defined there. It
    can access nongloabl variables that are defined outside of its body.


    avg is the inner function averager. The closure for average extends the scope of
    that function to include the binding for the free variable series.

    >>> avg = make_averager()
    >>> avg(10)
    10.0
    >>> avg(11)
    10.5
    >>> avg(12)
    11.0


    The binding for series is kept in the __closure__ attribute of the returned function avg.
    These items are cells, and they have an attr cell_contents where the actual value is stored.

    >>> avg.__code__.co_varnames
    ('val', 'total')
    >>> avg.__code__.co_freevars
    ('series',)
    >>> avg.__closure__  # doctest: +ELLIPSIS
    (<cell at 0x...: list object at 0x...>,)
    >>> avg.__closure__[0].cell_contents
    [10, 11, 12]
    """
    series = []

    def averager(val):
        series.append(val)
        total = sum(series)
        return total / len(series)

    return averager


def make_average_bugs():
    """
    A broken function to calculate a running average without keeping all history.

    With immutable types like numbers, string, tuples. All you can do is read, but
    never update. Rebinding them as in count = count + 1 makes them local variables.
    """
    count = 0
    total = 0

    def averager(val):
        count += 1
        total += val
        return total / count

    return averager


def make_averager2():
    """
    The ``nonlocal`` declaration lets you flag a variable as a free variable
    even when it's assigned a new value within the function.

    >>> avg = make_averager2()
    >>> avg(10)
    10.0
    >>> avg(11)
    10.5
    >>> avg(12)
    11.0
    """
    count = 0
    total = 0

    def averager(val):
        # nonlocal declaratin is compulsory
        nonlocal count, total
        count += 1
        total += val
        return total / count

    return averager
