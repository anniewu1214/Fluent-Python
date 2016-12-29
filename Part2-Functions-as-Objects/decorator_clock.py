import time
import functools


def clock(func):
    """The typical behavior of a decorator: replace the decorated function with
    a new function that accepts the same arguments and returns whatever the
    decorated function was supposed to return, while also doing some extra processing"""

    def clocked(*args):
        t0 = time.perf_counter()
        # the closure for clocked encompassed the func free variable
        result = func(*args)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[%0.8fs]%s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result

    return clocked


def clock_better(func):
    """use functools.wraps decorator to copy relevant attributes from func to clocked"""

    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - t0
        name = func.__name__
        arg_list = []
        if args:
            arg_list.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
            arg_list.append(', '.join(pairs))
        arg_str = ', '.join(arg_list)
        print('[%0.8fs] %s(%s) -> %r ' % (elapsed, name, arg_str, result))
        return result

    return clocked


def clock_run():
    @clock_better
    def snooze(seconds):
        time.sleep(seconds)

    @clock_better
    def factorial(n):
        return 1 if n < 2 else n * factorial(n - 1)

    print('*' * 40, 'Calling snooze(.123)')
    snooze(.123)
    print('*' * 40, 'Calling factorial(6)')
    print('6! =', factorial(6))


def lru_cache_run():
    """functools.lru_cache implements memoization by saving the results
    of previous invocations of an expensive function."""

    @clock
    def fib(n):
        if n < 2:
            return n
        return fib(n - 2) + fib(n - 1)

    print(fib(6))

    @functools.lru_cache(maxsize=128, typed=False)
    @clock
    def fib_cache(n):
        """
        - maxsize is the number of stored call results, after the cache is full, older
        results are discarded to make room. It should be the power of 2 for max performence.

        - typed if True, results of different argument types are stored separately, i.e.
        distinguishing between float and integer args 1 and 1.0
        """
        if n < 2:
            return n
        return fib_cache(n - 2) + fib_cache(n - 1)

    print(fib_cache(6))


if __name__ == '__main__':
    clock_run()
    lru_cache_run()
