print('<[100]> evalsupport module start')


def deco_alpha(cls):
    print('<[200]> deco_alpha')

    def inner_1(self):
        print('<[300]> deco_alpha:inner_1')

    cls.method_y = inner_1
    return cls


class MetaAleph(type):
    print('<[400]> MetaAleph body')

    def __init__(cls, name, bases, dic):
        """
        Build the actual class body
        :param cls: refers to the class being created (e.g. ClassFive);
                    conventional to replace self with cls.
        :param name, bases, dic: same args passed to type to build a class
        """
        print('<[500]> MetaAleph.__init__')

        def inner_2(self):
            """
            :param self: eventually refer to an instance of the class we'are creating
                        (e.g. an instance of ClassFive)
            """
            print('<[600]> MetaAleph.__init__:inner_2')

        cls.method_z = inner_2


print('<[700]> evalsupport module end')
