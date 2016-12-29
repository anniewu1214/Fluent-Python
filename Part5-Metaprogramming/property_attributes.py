"""
Properties are always class attributes, but they actually manage
attribute access in the instance of the class.


The main point of this section is that an expression like obj.attr does not
search for attr starting with obj. The search actually starts at obj.__class__
and only if there is no property named attr in the class, Python looks in the
obj instance itself. This rule applies not only to properties but to a whole
category of descriptors, the overriding descriptors.
"""


class Class:
    """
    ``vars`` returns the __dict__ of obj. showing it has no instance attributes::

        >>> obj = Class()
        >>> vars(obj)
        {}

    Reading from obj.data retrieves the value of Class.data; writting to obj.data
    creates an instance attribute::

        >>> obj.data
        'the class data attr'
        >>> obj.data = 'bar'
        >>> vars(obj)
        {'data': 'bar'}

    When an instance and its class both have a attribute by the same name, the
    instance attribute shadows the class attribute, the Class.data is intact::

        >>> obj.data
        'bar'
        >>> Class.data
        'the class data attr'


    Reading prop directly from Class retrieves the property object itself,
    reading obj.prop executes the property getter::

        >>> Class.prop  # doctest: +ELLIPSIS
        <property object at 0x...>
        >>> obj.prop
        'the prop value'

    Setting an instance prop attribute fails.
    Putting 'prop' directly in the obj.__dict__ works::

        >>> obj.prop = 'foo'
        Traceback (most recent call last):
            ...
        AttributeError: can't set attribute
        >>> obj.__dict__['prop'] = 'foo'
        >>> vars(obj)
        {'prop': 'foo', 'data': 'bar'}


    Instance attribute does not shadow class property. Overriding Class.prop
    destroys the property object::

        >>> obj.prop
        'the prop value'
        >>> Class.prop = 'baz'
        >>> obj.prop
        'foo'

    New class property shadows existing instance attribute::

        >>> obj.data
        'bar'
        >>> Class.data
        'the class data attr'
        >>> Class.data = property(lambda self: 'the "data" prop value')
        >>> obj.data
        'the "data" prop value'
        >>> del Class.data
        >>> obj.data
        'bar'
    """
    data = 'the class data attr'

    @property
    def prop(self):
        return 'the prop value'
