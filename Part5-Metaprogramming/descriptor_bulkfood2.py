import abc

"""
The relationship between Validated, Quantity, and NonBlank is an application
of the Template Method design pattern. In particular the Validated.__set__
defines an algorighm in terms of abstract operations that subclasses override
to provide concrete behavoir.
"""


class AutoStorage:
    """Descriptor class that manages storage attrs automatically"""
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(prefix, index)
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)


class Validated(abc.ABC, AutoStorage):
    """Handles validation by delegating to an abstract validate method."""

    def __set__(self, instance, value):
        value = self.validate(instance, value)
        super().__set__(instance, value)

    @abc.abstractmethod
    def validate(self, instance, value):
        """return validated value or raise ValueError"""


class Quantity(Validated):
    """a number greater then 0"""

    def validate(self, instance, value):
        if value <= 0:
            raise ValueError('value must be > 0')
        return value


class NonBlank(Validated):
    """a string with at least one non-space character"""

    def validate(self, instance, value):
        value = value.strip()
        if len(value) == 0:
            raise ValueError('value cannot be empty or blank')
        return value


def entity(cls):
    """A class decorator for customizing descriptors names, e.g. '_Quantity#weight'

    Class decorators are a simpler way of doing sth that metaclass does: customizing
    a class the moment it's created.
    """
    # iterate over dict holding the class attrs
    for key, attr in cls.__dict__.items():
        if isinstance(attr, Validated):
            type_name = type(attr).__name__
            attr.storage_name = '_{}#{}'.format(type_name, key)
    return cls


@entity
class LineItem:
    """
    >>> raisins = LineItem("Golden raisins", 10, 6.95)
    >>> dir(raisins)[:3]
    ['_NonBlank#description', '_Quantity#price', '_Quantity#weight']
    >>> LineItem.description.storage_name
    '_NonBlank#description'
    >>> raisins.description
    'Golden raisins'
    >>> getattr(raisins, '_NonBlank#description')
    'Golden raisins'
    """
    description = NonBlank()
    weight = Quantity()
    price = Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.price = price
        self.weight = weight

    def subtotal(self):
        return self.weight * self.price
