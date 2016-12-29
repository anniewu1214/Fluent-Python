"""
A decorator is a callable that takes another function as argument (the decorated function).
The decorator may perform some processing with the decorated function, and returns it or
replaces it with another function or callable objects.


Decorators are executed as soon as the module is imported, but the decorated function only
run when they are explicitly invoked.

    $ python3 registration.py
    running register(<function f1 at 0x...>)
    running register(<function f2 at 0x...>)
    running main()
    registry-> [<function f1 at 0x...>, <function f2 at 0x...>]
    running f1()
    running f2()
    running f3()


    >>> import decorator_registration
    running register(<function f1 at 0x...>)
    running register(<function f2 at 0x...>)
"""

registry = []


def register(func):
    """register runs before any other function in the module"""
    print('running register(%s)' % func)
    registry.append(func)
    return func


@register
def f1():
    print('running f1()')


@register
def f2():
    print('running f2()')


def f3():
    print('running f3()')


def main():
    print('running main()')
    print('registry->', registry)
    f1()
    f2()
    f3()


if __name__ == '__main__':
    main()
