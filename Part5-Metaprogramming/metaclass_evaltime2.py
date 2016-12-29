"""
Classes are objects, therefore each class must be an instance of some
other class. By default, Python classes are instances of type.

str, type, and LineItem are subclasses of object; are instances of type.
object is an instance of type, type is a subclass of object!

    >>> 'spam'.__class__
    <class 'str'>
    >>> str.__class__
    <class 'type'>
    >>> from descriptor_bulkfood2 import LineItem
    >>> LineItem.__class__
    <class 'type'>
    >>> type.__class__
    <class 'type'>


Every class is an instance of type, but only metaclasses are also subclasses
of type, a metaclass inherits from type the power to construct classes.

    >>> import collections
    >>> collections.Iterable.__class__
    <class 'abc.ABCMeta'>
    >>> import abc
    >>> abc.ABCMeta.__class__
    <class 'type'>
    >>> abc.ABCMeta.__mro__
    (<class 'abc.ABCMeta'>, <class 'type'>, <class 'object'>)

"""

from metaclass_evalsupport import deco_alpha
from metaclass_evalsupport import MetaAleph

print('<[1]> evaltime_meta module start')


@deco_alpha
class ClassThree:
    """ replace method_y by inner_1"""
    print('<[2]> ClassThree body')

    def method_y(self):
        print('<[3]> ClassThree.method_y')


class ClassFour(ClassThree):
    """@deco_alpha has no effect on ClassFour"""
    print('<[4]> ClassFour body')

    def method_y(self):
        print('<[5]> ClassFour.method_y')


class ClassFive(metaclass=MetaAleph):
    """MetaAleph.__init__ is invoked to initilize ClassFive

    - The interpreter evaluates the body of ClassFive, but then instead of
    calling type to build the actual class body, it calls MetaAleph.
    - method_z is replaced with inner_2, so is ClassSix
    """
    print('<[6]> ClassFive body')

    def __init__(self):
        print('<[7]> ClassFive.__init__')

    def method_z(self):
        print('<[8]> ClassFive.method_y')


class ClassSix(ClassFive):
    """ ClassSix makes no direct reference to MetaAleph, but it's a subclass
    of ClassFive and therefore an instance of MetaAlepha, so it's initialized
    by MetaAleph.__init__"""
    print('<[9]> ClassSix body')

    def method_z(self):
        print('<[10]> ClassSix.method_y')


if __name__ == '__main__':
    print('<[11]> ClassThree tests', 30 * '.')
    three = ClassThree()
    three.method_y()
    print('<[12]> ClassFour tests', 30 * '.')
    four = ClassFour()
    four.method_y()
    print('<[13]> ClassFive tests', 30 * '.')
    five = ClassFive()
    five.method_z()
    print('<[14]> ClassSix tests', 30 * '.')
    six = ClassSix()
    six.method_z()

print('<[15]> evaltime_meta module end')

"""
Scenario #3: The module metaclass_evaltime2.py is imported interactively in the Python console.
>>> import metaclass_evaltime2.py
<[100]> evalsupport module start
<[400]> MetaAleph body
<[700]> evalsupport module end
<[1]> evaltime_meta module start
<[2]> ClassThree body
<[200]> deco_alpha
<[4]> ClassFour body
<[6]> ClassFive body
<[500]> MetaAleph.__init__  <1>
<[9]> ClassSix body
<[500]> MetaAleph.__init__  <2>
<[15]> evaltime_meta module end


Scenario #4: The module metaclass_evaltime2.py is run from the command shell.
$ python metaclass_evaltime2.py
<[100]> evalsupport module start
<[400]> MetaAleph body
<[700]> evalsupport module end
<[1]> evaltime_meta module start
<[2]> ClassThree body
<[200]> deco_alpha
<[4]> ClassFour body
<[6]> ClassFive body
<[500]> MetaAleph.__init__
<[9]> ClassSix body
<[500]> MetaAleph.__init__
<[11]> ClassThree tests ..............................
<[300]> deco_alpha:inner_1  <1>
<[12]> ClassFour tests ..............................
<[5]> ClassFour.method_y  <2>
<[13]> ClassFive tests ..............................
<[7]> ClassFive.__init__
<[600]> MetaAleph.__init__:inner_2  <3>
<[14]> ClassSix tests ..............................
<[7]> ClassFive.__init__
<[600]> MetaAleph.__init__:inner_2  <4>
<[15]> evaltime_meta module end
"""
