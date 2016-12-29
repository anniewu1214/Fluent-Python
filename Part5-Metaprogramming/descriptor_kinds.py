"""Simple classes for studying descriptor overriding behaviors.


Overriding descriptor: __set__. A descriptor implementing __set__ will override attempts to
assign to instance attrs. Properties are also overriding descriptors: if setter function is not
provided, the default __set__ will raise AttributeError to signal that the attr is read-only::

    >>> obj = Managed()
    >>> obj.over
    -> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>)
    >>> Managed.over
    -> Overriding.__get__(<Overriding object>, None, <class Managed>)
    >>> obj.over = 7
    -> Overriding.__set__(<Overriding object>, <Managed object>, 7)
    >>> obj.over
    -> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>)
    >>> obj.__dict__['over'] = 8
    >>> vars(obj)
    {'over': 8}
    >>> obj.over
    -> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>)


Overriding descriptor without __get__. Reading the descriptor through an instance will return
the descriptor obj itself because there's no __get__ to handle that access. If a namesake
instance attr is created with a new value via direct access to the instance __dict__,
__set__ will still override further attempts to set that attr, but reading that attr will
simply return the new value from the instance, instead of returning the descriptor obj. That
is: the instance attr will shadow the descriptor, but only when reading::

    >>> obj.over_no_get  # doctest: +ELLIPSIS
    <descriptor_kinds.OverridingNoGet object at ...>
    >>> Managed.over_no_get  # doctest: +ELLIPSIS
    <descriptor_kinds.OverridingNoGet object at ...>
    >>> obj.over_no_get = 7
    -> OverridingNoGet.__set__(<OverridingNoGet object>, <Managed object>, 7)
    >>> obj.over_no_get  # doctest: +ELLIPSIS
    <descriptor_kinds.OverridingNoGet object at ...>
    >>> obj.__dict__['over_no_get'] = 9
    >>> obj.over_no_get
    9
    >>> obj.over_no_get = 7
    -> OverridingNoGet.__set__(<OverridingNoGet object>, <Managed object>, 7)
    >>> obj.over_no_get
    9


Nonoverriding descriptor: no __set__. Setting an instance attr with the same name will
shadow the descriptor, rendering it ineffective for handling that attr in that specific
instance. Methods are implemented as nonoverriding descriptors::

    >>> obj.non_over
    -> NonOverriding.__get__(<NonOverriding object>, <Managed object>, <class Managed>)
    >>> obj.non_over = 7
    >>> obj.non_over
    7
    >>> Managed.non_over
    -> NonOverriding.__get__(<NonOverriding object>, None, <class Managed>)
    >>> del obj.non_over
    >>> obj.non_over
    -> NonOverriding.__get__(<NonOverriding object>, <Managed object>, <class Managed>)


A method is a nonoverriding descriptor::

    >>> obj = Managed()
    >>> obj.spam  # doctest: +ELLIPSIS
    <bound method Managed.spam of <descriptor_kinds.Managed object at 0x...>>
    >>> Managed.spam  # doctest: +ELLIPSIS
    <function Managed.spam at ...>
    >>> obj.spam = 7
    >>> obj.spam
    7


Overriding a descriptor in the class. Regardless of whether a descriptor is
overriding or not, it can be overwritten by assignment to the class. This
monkey-patching technique would break any class that depend on the descriptor
for proper operation::

    >>> Managed.over = 1
    >>> Managed.over_no_get = 2
    >>> Managed.non_over = 3
    >>> obj.over, obj.over_no_get, obj.non_over
    (1, 2, 3)
"""


### auxiliary function for displacy only ###


def cls_name(obj_or_cls):
    cls = type(obj_or_cls)
    if cls is type:
        cls = obj_or_cls
    return cls.__name__.split('.')[-1]


def display(obj):
    cls = type(obj)
    if cls is type:
        return '<class {}>'.format(obj.__name__)
    elif cls in [type(None), int]:
        return repr(obj)
    else:
        return '<{} object>'.format(cls_name(obj))


def print_args(name, *args):
    pseudo_args = ', '.join(display(x) for x in args)
    print('-> {}.__{}__({})'.format(cls_name(args[0]), name, pseudo_args))


### essential classes for this example ###

class Overriding:
    """a.k.a. data or enforced descriptor"""

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class OverridingNoGet:
    """an overriding descriptor without `__get__`"""

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class NonOverriding:
    """a.k.a. non-data or shadowable descriptor"""

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)


class Managed:
    """Using one instance of each of the descriptor classes"""
    over = Overriding()
    over_no_get = OverridingNoGet()
    non_over = NonOverriding()

    def spam(self):
        """for comparison because methods are also descriptors"""
        print('-> Managed.spam({})'.format(display(self)))
