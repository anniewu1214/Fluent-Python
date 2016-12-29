def quantity(storage_name):
    """The quantity property factory

    the storage_name argument determines where the data for each property is
    stored; for weight, the storage name is 'weight'
    """

    def qty_getter(instance):
        """
        - the first arg could be named ``self``, but that would be strange because
         this is not a class body; ``instance`` refers to the LineItem instance where
         the attribute will be stored

        - the value is retrieved directly from instance.__dict__ to bypass the
         property and avoid an infinite recursion
        """
        return instance.__dict__[storage_name]

    def qty_setter(instance, value):
        """the value is also stored in the instance.__dict__ bypassing the property"""
        if value > 0:
            instance.__dict__[storage_name] = value
        else:
            raise ValueError('value must be > 0')

    # build a custom property object and return it
    return property(qty_getter, qty_setter)


def quantity_auto():
    """quantity property factory with automatic storage name

    We can't rely on class attributes to share the counter across invocations, so
    we define it as an attribute of the quantity function itself.
    """

    try:
        quantity_auto.counter += 1
    except AttributeError:
        # if counter is undefined, set it to 0
        quantity_auto.counter = 0

    # create storage_name as a local variable and rely on closure to keep
    # them alive for later use by qty_getter and qty_setter
    storage_name = '_{}:{}'.format('quantity_auto', quantity_auto.counter)

    def qty_getter(instance):
        return getattr(instance, storage_name)

    def qty_setter(instance, value):
        if value > 0:
            setattr(instance, storage_name, value)
        else:
            raise ValueError('value must be > 0')

    return property(qty_getter, qty_setter)


class LineItem:
    """
    LineItem class using two instances of `quantity` properties::

        >>> nutmeg = LineItem('Moluccan nutmeg', 8, 13.95)
        >>> nutmeg.weight, nutmeg.price
        (8, 13.95)
        >>> sorted(vars(nutmeg).items())
        [('description', 'Moluccan nutmeg'), ('price', 13.95), ('weight', 8)]
    """

    # use the factory to define the properties
    weight = quantity('weight')
    price = quantity('price')

    def __init__(self, description, weight, price):
        self.description = description
        # the property is already active, a <= 0 weight/price is rejected
        self.weight = weight
        self.price = price

    def subtotal(self):
        # property in use, retrieve values stored in the instance
        return self.weight * self.price


class LineItemAuto:
    weight = quantity_auto()
    price = quantity_auto()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


class BlackKnight:
    """
    Attribute deletion: the @my_property.deleter decorator is used to wrap
    the method in charge of deleting the attribute managed by the property.

    >>> knight = BlackKnight()
    >>> knight.member
    next member is:
    'an arm'
    >>> del knight.member
    BLACK KNIGHT (loses an arm)
    -- 'Tis but a scratch.
    >>> del knight.member
    BLACK KNIGHT (loses another arm)
    -- It's just a flesh wound.
    """

    def __init__(self):
        self.members = ['an arm', 'another arm']
        self.phrases = ["'Tis but a scratch.",
                        "It's just a flesh wound."]

    @property
    def member(self):
        print('next member is:')
        return self.members[0]

    @member.deleter
    def member(self):
        text = 'BLACK KNIGHT (loses {})\n-- {}'
        print(text.format(self.members.pop(0), self.phrases.pop(0)))
