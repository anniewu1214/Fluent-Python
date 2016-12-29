"""
A class implementing a __get__, a __set__, or a __del__ method
 is a descriptor. You use a descriptor by declaring instances of
 it as class attributes of another class.

Definitions:

- Descriptor class: Quantity, a class implementing the descriptor protocol

- Managed class: LineItem, the class where the descriptor instances are declared as class attributes

- Descriptor instance: LineItem.weight, LineItem.price, declared as a class attribute of the manged class

- Managed instance: LineItem instances

- Storage attribute: LineItem instance attributes weight and price, an attribute of
  the managed instance that will hold the value of the managed attribute for that
  particular instance.

- Managed attribute: a public attribute in the manged class that will be handled by
  a descritpor instance, with values stored in storage attributes.
"""


class Quantity:
    """Descriptor is a protocol-based feature; no subclassing is needed."""

    def __init__(self, storage_name):
        """
        :param storage_name: hold the value in LineItem instances
        """
        self.storage_name = storage_name

    def __set__(self, instance, value):
        """
        Called when there's an attempt to assign to the managed attribute. Values
        should be stored in the managed instances, that's why Python provides the
        instance argument to the descriptor methods.

        :param self: descriptor instance, LineItem.weight, LineItem.price
        :param instance: managed instance, a LineItem instance
        :param value: the value being assigned
        """
        if value > 0:
            # handle __dict__ directly; trying to use the setattr build-in would
            # trigger the __set__ method again, leading to infinite recursion.
            instance.__dict__[self.storage_name] = value
        else:
            raise ValueError('value must be > 0')


class LineItem:
    """
    There are really 2 distinct attributes named `weight`: one is a class
    attribute of LineItem, the other is an instance attribute that will
    exist in each LineItem object. This also applies to `price`
    """
    # descriptor instance is bound to the weight attr
    weight = Quantity('weight')
    price = Quantity('price')

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


class QuantityAuto:
    """To avoid retyping the attribute name in the descriptor declarations, generate
    a unique string for the storage_name of each QuantityAuto instance"""
    __counter = 0

    def __init__(self):
        """Using _ garantees the storage_name won't clash with attributes created by
        the user, because nutmeg._Quantite#0 is invalid syntax. But we can always
        get and set attributes with such 'invalid' identifiers using the getattr and
        setattr buildin functions. or by poking the instance __dict__"""
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(prefix, index)
        cls.__counter += 1

    def __get__(self, instance, owner):
        """must implement __get__ because the name of the managed attribute is not
        the same as storage_name.

        :param owner: reference to the managed class(e.g. LineItem), handy when the
        descriptor is used to get attrs from the class. If a managed attr, such as weight,
        is retrieved via the class like LineItem.weight, __get__ receives None as the value for instance
        """
        # if the call was not through an instance, return the descriptor itself
        if instance is None:
            return self
        # otherwise use getattr to retrieve value from the instance
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        """use the higher-level getattr and setattr to store the value - instead of
        resorting to instance.__dict__ - because the managed attr and the storage
        attr have different names, so calling getattr on the storage attr will not
        trigger the descriptor, avoiding the infinite recursion in Quantity"""
        if value > 0:
            # use setattr to store the value in the instance
            setattr(instance, self.storage_name, value)
        else:
            raise ValueError('value must be > 0')


class LineItemAuto:
    """
    >>> LineItemAuto.price  # doctest: +ELLIPSIS
    <descriptor_bulkfood.QuantityAuto object ...>
    >>> coconuts = LineItemAuto('Brazilian coconut', 20, 17.95)
    >>> coconuts.weight, coconuts.price
    (20, 17.95)
    >>> getattr(coconuts, '_QuantityAuto#0'), getattr(coconuts, '_QuantityAuto#1')
    (20, 17.95)
    """
    weight = QuantityAuto()
    price = QuantityAuto()

    def __init__(self, description, weight, price):
        self.description = description
        self.price = price
        self.weight = weight

    def subtotal(self):
        return self.weight * self.price
