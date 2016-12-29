import contextlib

"""
else block:

for/else: run else if the for loop runs to completion (no break).

while/else: run else if no while loop exits because the condition
became falsy (no break).

try/else: run else if no break raised in try block.

In all cases, else clause is skipped if an exception or a return, break,
or continue statement causes control to jump out of the main block of the
compound statement.
"""


class LookingGlass:
    """
    The with statement is designed to simplify the try/finally pattern. The
    context manager protocol consists of the __enter__ and __exit__ methods.
    At the start __enter__ is invoked on the context manager obj, the role
    of the finally clause is played by a call to __exit__ on the context
    manager at the end of the with block.

    >>> with LookingGlass() as what:
    ...     print('Alice, Kitty and Snowdrop')
    ...     print(what)
    ...
    pordwonS dna yttiK ,ecilA
    YKCOWREBBAJ
    >>> what
    'JABBERWOCKY'
    >>> print('Back to normal.')
    Back to normal.
    >>> manager = LookingGlass()
    >>> monster = manager.__enter__()
    >>> monster == 'JABBERWOCKY'
    eurT
    >>> monster
    'YKCOWREBBAJ'
    >>> manager.__exit__(None, None, None)
    >>> monster
    'JABBERWOCKY'
    """

    def __enter__(self):
        """
        - called before entering with-statement
        - return value bound to ``as value``
        - commonly returns context-manager itself
        """
        import sys
        self.original_write = sys.stdout.write
        # monkey-patch sys.stdout.write, replacing it with our own method
        sys.stdout.write = self.reverse_write
        # return this string so that we have something to put in the target variable
        return 'JABBERWOCKY'

    def reverse_write(self, text):
        self.original_write(text[::-1])

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        - called when with-statement body exits
        - handles exception in the body block; all args are None if no exception
        - by default, __exit__() progagates exceptions; it should never explicitly
         re-raise exceptions, only raise exceptions if it fails itself
        """
        # it's cheap to import modules again, because Python will cache them
        import sys
        sys.stdout.write = self.original_write
        if exc_type is ZeroDivisionError:
            print('Please do not divide by zero!')
            # return True to tell the interpreter that the exception is handled
            return True


@contextlib.contextmanager
def looking_glass():
    """
    - @contextmanager reduces the boilplate of creating a context manager: instead
    of writing a whole class with __enter__ and __exit__, just implement a generator
    with a single yield that should produce whatever you want __enter__ to return.

    - yield is used to split the boyd of the function in two parts: everything before
    yield will be executed at the begining of the while block when the interpreter
    calls __enter__; the code after yield will run when __exit__ is called

    - __exit__() propagates the exception by default, returning True to suppress
    it. @contextmanager assumes that any exception is handled and should be
    suppressed. Explicitly re-raise an exceptin if you don't want to suppress it.

    - the try/finally block is unavoidable, because you never know what the user
    are going to do inside the with block.

    >>> with looking_glass() as what:
    ...    print('Alice, Kitty and Snowdrop')
    ...    print(what)
    ...
    pordwonS dna yttiK ,ecilA
    YKCOWREBBAJ
    >>> what
    'JABBERWOCKY'
    """
    import sys
    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])

    sys.stdout.write = reverse_write
    msg = ''
    try:
        yield 'JABBERWOCKY'
    except ZeroDivisionError:
        msg = 'Please DO NOT divide by zero!'
    finally:
        sys.stdout.write = original_write
        if msg:
            print(msg)
