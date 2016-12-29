from functools import singledispatch
from collections import abc
import html
import numbers


@singledispatch
# @singledispatch marks the base function that handles the object type
def htmlize(obj):
    """
    If you decorate a plain function with @singledispatch, it becomes a
    generic function: a group of functions to perform the same operation
    in different ways, depending on the type of the first argument.

    >>> htmlize({1, 2, 3})
    '<pre>{1, 2, 3}</pre>'
    >>> htmlize(abs)
    '<pre>&lt;built-in function abs&gt;</pre>'
    >>> htmlize(42)
    '<pre>42 (0x2a)</pre>'
    >>> print(htmlize(['alpha', 66, {3, 2, 1}]))
    <ul>
    <li><p>alpha</p></li>
    <li><pre>66 (0x42)</pre></li>
    <li><pre>{1, 2, 3}</pre></li>
    </ul>
    """
    content = html.escape(repr(obj))
    return '<pre>{}</pre>'.format(content)


@htmlize.register(str)
def _(text):
    """each specialized function is decorated with @<base_function>.register(<type>)

    The name of the specialized function is irrelevant; _ is a good choice to make this clear.
    """
    content = html.escape(text).replace('\n', '<br>\n')
    return '<p>{0}</p>'.format(content)


@htmlize.register(numbers.Integral)
def _n(n):
    """
    numbers.Integral is a virtual superclass of int

    When possible, register the specialized functions to handle ABCs
    (abstract classes) such as numbers.Integral and abc.MutableSequence
    instead of concrete implementations like int and list. This allows
    your code to support a greater variety of compatible types.
    """
    return '<pre>{0} (0x{0:x})</pre>'.format(n)


@htmlize.register(tuple)
@htmlize.register(abc.MutableSequence)
def _(seq):
    """Stack several register decorators to support different
     types with the same function"""
    inner = '</li>\n<li>'.join(htmlize(item) for item in seq)
    return '<ul>\n<li>' + inner + '</li>\n</ul>'
