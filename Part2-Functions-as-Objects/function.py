"""
Packages for functional programming

        >>> from functools import reduce, partial
        >>> from operator import mul, itemgetter, attrgetter

    reduce

        >>> def fact(n):
        ...     return reduce(mul, range(1, n + 1))
        >>> fact(5)
        120

    itemgetter(item) returns a callable object that fetches item from its operand.
    If multiple items are specified, returns a tuple of lookup values.

        >>> itemgetter(1)('ABCDEFG')
        'B'
        >>> itemgetter(1, 3, 5)('ABCDEFG')
        ('B', 'D', 'F')
        >>> itemgetter(slice(2, None))('ABCDEFG')
        'CDEFG'
        >>> metro_data = [
        ... ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
        ... ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
        ... ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
        ... ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
        ... ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833))]
        >>> for city in sorted(metro_data, key=itemgetter(1)):
        ...     print(city)
        ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833))
        ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889))
        ('Tokyo', 'JP', 36.933, (35.689722, 139.691667))
        ('Mexico City', 'MX', 20.142, (19.433333, -99.133333))
        ('New York-Newark', 'US', 20.104, (40.808611, -74.020386))
        >>> cc_name = itemgetter(1, 0)
        >>> for city in metro_data:
        ...     print(cc_name(city))
        ...
        ('JP', 'Tokyo')
        ('IN', 'Delhi NCR')
        ('MX', 'Mexico City')
        ('US', 'New York-Newark')
        ('BR', 'Sao Paulo')

    attrgetter returns a callable obj that fetches attr from its operand. If more than one
    attr is requested, returns a tuple of attrs.

        >>> from collections import namedtuple
        >>> LatLong = namedtuple('LatLong', 'lat long')
        >>> Metropolis = namedtuple('Metropolis', 'name cc pop coord')
        >>> metro_areas = [Metropolis(name, cc, pop, LatLong(lat, long))
        ...     for name, cc, pop, (lat, long) in metro_data]
        >>> metro_areas[0].coord.lat
        35.689722
        >>> name_lat = attrgetter('name', 'coord.lat')
        >>> for city in sorted(metro_areas, key=attrgetter('coord.lat')):
        ...     print(name_lat(city))
        ...
        ('Sao Paulo', -23.547778)
        ('Mexico City', 19.433333)
        ('Delhi NCR', 28.613889)
        ('Tokyo', 35.689722)
        ('New York-Newark', 40.808611)

        >>> import operator
        >>> [name for name in dir(operator) if not name.startswith('_')]
        ['abs', 'add', 'and_', 'attrgetter', 'concat', 'contains', 'countOf', 'delitem', 'eq', 'floordiv', 'ge', 'getitem', 'gt', 'iadd', 'iand', 'iconcat', 'ifloordiv', 'ilshift', 'imatmul', 'imod', 'imul', 'index', 'indexOf', 'inv', 'invert', 'ior', 'ipow', 'irshift', 'is_', 'is_not', 'isub', 'itemgetter', 'itruediv', 'ixor', 'le', 'length_hint', 'lshift', 'lt', 'matmul', 'methodcaller', 'mod', 'mul', 'ne', 'neg', 'not_', 'or_', 'pos', 'pow', 'rshift', 'setitem', 'sub', 'truediv', 'truth', 'xor']


    methodcaller returns a callable obj that calls the method name on its operand. If additional
    args and/or keyword args are given, they will be given to the method as well.

        >>> from operator import methodcaller
        >>> s = 'The time has come'
        >>> upcase = methodcaller('upper')
        >>> upcase(s)
        'THE TIME HAS COME'
        >>> hiphenate = methodcaller('replace', ' ', '-')
        >>> hiphenate(s)
        'The-time-has-come'


    functools.partial allows partial application of a function, which produces a new callable with some
    of the arguments of the original function fixed. It takes a callable as first arg, followed by an
    arbitrary number of positional and keyword args.

        >>> triple = partial(mul, 3)
        >>> triple(7)
        21
        >>> import unicodedata
        >>> nfc = partial(unicodedata.normalize, 'NFC')
        >>> s1 = 'café'
        >>> s2 = 'cafe\u0301'
        >>> s1, s2
        ('café', 'café')
        >>> s1 == s2
        False
        >>> nfc(s1) == nfc(s2)
        True

"""


def clip_annot(text: str, max_len: 'int > 0' = 80) -> str:
    """Return text clipped at the last space before or after max_len

    - Each arg in the function declaration may have an annotation expression preceded by :

    - the only thing Python does with annotations is to store them in the __annotations__ attr
    of the function. Annotations have no meaning to the interpreter, they'are just metadata that
    may be used by tools, such as IDEs, frameworks, and decorators.

    Extracting annotations from the function signature

        >>> clip_annot.__annotations__
        {'text': <class 'str'>, 'max_len': 'int > 0', 'return': <class 'str'>}
        >>> from inspect import signature
        >>> sig = signature(clip_annot)
        >>> sig.return_annotation
        <class 'str'>
        >>> for param in sig.parameters.values():
        ...     note = repr(param.annotation).ljust(13)
        ...     print(note, ':', param.name, '=', param.default)
        ...
        <class 'str'> : text = <class 'inspect._empty'>
        'int > 0'     : max_len = 80

    """
    end = None
    if len(text) > max_len:
        space_before = text.rfind(' ', 0, max_len)
        if space_before >= 0:
            end = space_before
        else:
            space_after = text.rfind(' ', max_len)
            if space_after >= 0:
                end = space_after
    if end is None:  # no spaces were found
        end = len(text)
    return text[:end].rstrip()


def clip(text, max_len=80):
    """Return text clipped at the last space before or after max_len

    Extracting information about the function arguments

        >>> clip.__defaults__
        (80,)
        >>> clip.__code__  # doctest: +ELLIPSIS
        <code object clip at 0x...>
        >>> clip.__code__.co_varnames
        ('text', 'max_len', 'end', 'space_before', 'space_after')
        >>> clip.__code__.co_argcount
        2

    Extracting the function signature. inspect.signature returns an inspect.Signature obj,
    which has a parameters attr that lets you read an ordered mapping of names to
    inspect.Paramater objects. Each Parameter instance has attrs such as name, default, and kind.

        >>> from inspect import signature
        >>> sig = signature(clip)
        >>> sig  # doctest: +ELLIPSIS
        <Signature (text, max_len=80)>
        >>> str(sig)
        '(text, max_len=80)'
        >>> for name, param in sig.parameters.items():
        ...     print(param.kind, ':', name, '=', param.default)
        ...
        POSITIONAL_OR_KEYWORD : text = <class 'inspect._empty'>
        POSITIONAL_OR_KEYWORD : max_len = 80
    """
    end = None
    if len(text) > max_len:
        space_before = text.rfind(' ', 0, max_len)
        if space_before >= 0:
            end = space_before
        else:
            space_after = text.rfind(' ', max_len)
            if space_after >= 0:
                end = space_after
    if end is None:  # no spaces were found
        end = len(text)
    return text[:end].rstrip()


def tag(name, *content, cls=None, **attrs):
    """Generate one or more HTML tags

    Some of the many ways of calling the target function

        >>> tag('br')
        '<br />'
        >>> tag('p', 'hello')
        '<p>hello</p>'
        >>> print(tag('p', 'hello', 'world'))
        <p>hello</p>
        <p>world</p>
        >>> tag('p', 'hello', id=33)
        '<p id="33">hello</p>'
        >>> print(tag('p', 'hello', 'world', cls='sidebar'))
        <p class="sidebar">hello</p>
        <p class="sidebar">world</p>
        >>> tag(content='testing', name="img")
        '<img content="testing" />'
        >>> my_tag = {'name': 'img', 'title': 'Sunset Boulevard',
        ...           'src': 'sunset.jpg', 'cls': 'framed'}
        >>> tag(**my_tag)
        '<img class="framed"  src="sunset.jpg"  title="Sunset Boulevard" />'

    Binding the function signature from the tag function. The Python data model exposes the same
    machinery the interpreter uses to bind arguments to formal paramters in function calls.

        >>> import inspect
        >>> sig = inspect.signature(tag)
        >>> bound_args = sig.bind(**my_tag)
        >>> bound_args  # doctest: +ELLIPSIS
        <BoundArguments (name='img', cls='framed', attrs={...})>
        >>> for name, value in bound_args.arguments.items():  # doctest: +ELLIPSIS
        ...     print(name, '=', value)
        ...
        name = img
        cls = framed
        attrs = {...}
        >>> del my_tag['name']
        >>> bound_args = sig.bind(**my_tag)  # IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        TypeError: missing a required argument: 'name'


    functool.partial applied to tag

        >>> from functools import partial
        >>> picture = partial(tag, 'img', cls='pic-frame')
        >>> picture(src='wumpus.jpeg')
        '<img class="pic-frame" src="wumpus.jpeg" />'
        >>> picture  # doctest: +ELLIPSIS
        functools.partial(<function tag at 0x...>, 'img', cls='pic-frame')
        >>> picture.func  # doctest: +ELLIPSIS
        <function tag at 0x...>
        >>> picture.args
        ('img',)
        >>> picture.keywords
        {'cls': 'pic-frame'}

    """
    if cls is not None:
        attrs['class'] = cls
    if attrs:
        attr_str = ' '.join(' %s="%s"' % (attr, value)
                            for attr, value in sorted(attrs.items()))
    else:
        attr_str = ''
    if content:
        return '\n'.join('<%s%s>%s</%s>' %
                         (name, attr_str, c, name) for c in content)
    else:
        return '<%s%s />' % (name, attr_str)
