import collections

from descriptor_bulkfood2 import Validated, Quantity, NonBlank


class EntityMeta(type):
    """Metaclass for business entities with validated fields"""

    def __init__(cls, name, bases, attr_dict):
        # call __init__ on the superclass
        super().__init__(name, bases, attr_dict)
        for key, attr in attr_dict.items():
            if isinstance(attr, Validated):
                type_name = type(attr).__name__
                attr.storage_name = '_{}#{}'.format(type_name, key)


class Entity(metaclass=EntityMeta):
    """Business entity with validated fields

    This class exists for convenience only: the user can just subclass
    Entity and not worry about EntityMeta."""


class EntityMeta2(type):
    """Metaclass for business entities with validated fields"""

    @classmethod
    def __prepare__(mcs, name, bases):
        """
        __prepare__ is invoked before __new__ in the metaclass to create the mapping
         that will be filled with the attrs from the class body.
        :param mcs: metaclass
        :param name: name of the class to be constructed
        :param bases: tuple of base classes of the class to be constructed
        :return: a mapping that will be receieved as the last arg by __new__ and then
            __init__ when the metaclass builds a new class
        """
        # return an empty OrderedDict instance, where the class attrs will be stored
        return collections.OrderedDict()

    def __init__(cls, name, bases, attr_dict):
        super().__init__(name, bases, attr_dict)
        # create a _field_names attribute in the class under construction
        cls._field_names = []
        # attr_dict is the OrderDict obtained by calling __prepare__
        for key, attr in attr_dict.items():
            # add the name of each Validated field found to _field_names
            if isinstance(attr, Validated):
                type_name = type(attr).__name__
                attr.storage_name = '_{}#{}'.format(type_name, key)
                cls._field_names.append(key)


class Entity2(metaclass=EntityMeta2):
    """Business entity with validated fields"""

    @classmethod
    def field_names(cls):
        for name in cls._field_names:
            yield name


class LineItem(Entity2):
    """
    >>> for name in LineItem.field_names():
    ...     print(name)
    ...
    description
    weight
    price
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
