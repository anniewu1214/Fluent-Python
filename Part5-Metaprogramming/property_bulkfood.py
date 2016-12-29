class LineItem:
    """
    A line item for a bulk food order has description, weight and price fields::

        >>> raisins = LineItem('Golden raisins', 10, 6.95)
        >>> raisins.weight, raisins.description, raisins.price
        (10, 'Golden raisins', 6.95)
        >>> raisins.subtotal()
        69.5


    The weight of a ``LineItem`` must be greater than 0::

        >>> raisins.weight = -20
        Traceback (most recent call last):
            ...
        ValueError: value must be > 0


    No change was made::

        >>> raisins.weight
        10


    The check is also performed on instantiation::

        >>> walnuts = LineItem('walnuts', 0, 10.00)
        Traceback (most recent call last):
            ...
        ValueError: value must be > 0


    The proteced attribute can still be accessed if needed for some reason::

        >>> raisins._LineItem__weight
        10
    """

    def __init__(self, description, weight, price):
        """the property setter is already in use, making sure
        that no instances with negative weight can be created
        """
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    @property
    def weight(self):
        """
        - @property decorates the getter method

        - the methods that implement a property all have the name
        of the public attribute: weight

        - the actual value is stored in a private attribute __weight
        """
        return self.__weight

    @weight.setter
    def weight(self, value):
        """the decorated getter has a .setter attribute, which is also
        a decorator; this ties the getter and setter together"""
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('value must be > 0')


class LineItemClassic:
    """ Defining properties without decorators

    The full signature of the ``property`` constructor:
        property(fget=None, fset=None, fdel=None, doc=None)
    """

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight  # weight is a property
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    def get_weight(self):
        """a plain getter"""
        return self.__weight

    def set_weight(self, value):
        """a plain setter"""
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('value must be > 0')

    # build the property and assign it to a public class attribute
    weight = property(get_weight, set_weight)
