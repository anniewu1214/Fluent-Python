from metaclass_evalsupport import deco_alpha

"""
Import time vs. Runtime

- At import time, the interpreter parses the source code of a .py file, and
generates the bytecode to be executed. Syntax error may occur. If there's an
.pyc file in the local __pycache__, those steps are skipped.

- the import statement is not merely a declaration but it runs all the top-level
code of the imported module when it's imported first time in the process - further
imports of the same module will use a cache, and only name binding occurs then.

- top-level code:
    -- functions: compiles function body and binds the function obj to its global
    name, does not execute the body of the function.
    -- classes: interpreter executes the body of every class, even the body of
    classes nested in other classes; methods are not executed.
"""

print('<[1]> evaltime module start')


class ClassOne:
    print('<[2]> ClassOne body')

    def __init__(self):
        print('<[3]> ClassOne.__init__')

    def __del__(self):
        print('<[4]> ClassOne.__del__')

    def method_x(self):
        print('<[5]> ClassOne.method_x')

    class ClassTwo:
        print('<[6]> ClassTwo body')


@deco_alpha
class ClassThree:
    print('<[7]> ClassThree body')

    def method_y(self):
        print('<[8]> ClassThree.method_y')


class ClassFour(ClassThree):
    """The effects of a class decorator may not affect subclasses.
    method_y of ClassThree is replaced by @deco_alpha, but that does not
    affect ClassFour at all.
    """
    print('<[9]> ClassFour body')

    def method_y(self):
        print('<[10]> ClassFour.method_y')


if __name__ == '__main__':
    print('<[11]> ClassOne tests', 30 * '.')
    one = ClassOne()
    one.method_x()
    print('<[12]> ClassThree tests', 30 * '.')
    three = ClassThree()
    three.method_y()
    print('<[13]> ClassFour tests', 30 * '.')
    four = ClassFour()
    four.method_y()

print('<[14]> evaltime module end')

"""
Scenario #1: the module metaclass_evaltime.py is imported interactively in the Python console:
>>> import evaltime
<[100]> evalsupport module start
<[400]> MetaAleph body
<[700]> evalsupport module end
<[1]> evaltime module start
<[2]> ClassOne body
<[6]> ClassTwo body
<[7]> ClassThree body
<[200]> deco_alpha
<[9]> ClassFour body
<[14]> evaltime module end

Scenario #2: the module metaclass_evaltime.py is run from the command shell:
$ python3 metaclass_evaltime.py
<[100]> evalsupport module start
<[400]> MetaAleph body
<[700]> evalsupport module end
<[1]> evaltime module start
<[2]> ClassOne body
<[6]> ClassTwo body
<[7]> ClassThree body
<[200]> deco_alpha
<[9]> ClassFour body
<[11]> ClassOne tests ..............................
<[3]> ClassOne.__init__
<[5]> ClassOne.method_x
<[12]> ClassThree tests ..............................
<[300]> deco_alpha:inner_1  <3>
<[13]> ClassFour tests ..............................
<[10]> ClassFour.method_y
<[14]> evaltime module end
<[4]> ClassOne.__del__  <4>
"""
