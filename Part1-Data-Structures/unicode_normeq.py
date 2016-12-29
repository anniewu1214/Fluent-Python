"""
Utility functions for normalized Unicode string comparison.

Using Normal Form C, case sensitive:

    >>> s1 = 'café'
    >>> s2 = 'cafe\u0301'
    >>> s1 == s2
    False
    >>> nfc_equal(s1, s2)
    True
    >>> nfc_equal('A', 'a')
    False

Using Normal Form C with case folding:

    >>> s3 = 'Straße'
    >>> s4 = 'strasse'
    >>> s3 == s4
    False
    >>> nfc_equal(s3, s4)
    False
    >>> fold_equal(s3, s4)
    True
    >>> fold_equal(s1, s2)
    True
    >>> fold_equal('A', 'a')
    True

Remove all diacritic marks

    >>> order = '“Herr Voß: • 1⁄2 cup of ŒtkerTM caffè latte • bowl of açaí.”'
    >>> shave_marks(order)
    '“Herr Voß: • 1⁄2 cup of ŒtkerTM caffe latte • bowl of acai.”'
    >>> Greek = 'Ζέφυρος, Zéfiro'
    >>> shave_marks(Greek)
    'Ζεφυρος, Zefiro'

"""

from unicodedata import normalize, combining, numeric, name
import re


def nfc_equal(str1, str2):
    return normalize('NFC', str1) == normalize('NFC', str2)


def fold_equal(str1, str2):
    return (normalize('NFC', str1).casefold() ==
            normalize('NFC', str2).casefold())


def shave_marks(txt):
    """Remove all diacritic marks"""
    # Decompose all characters into base characters and combining marks
    norm_txt = normalize('NFD', txt)
    # filter out all combing marks
    shaved = "".join(c for c in norm_txt
                     if not combining(c))
    # recompose all characters
    return normalize('NFC', shaved)


"""
The Unicode standard provides an entire database that includes not only the table mapping code
points to char names, but also metadata about the individual chars and how they are related. e.g.
the database records whether a char is printable, is a letter, is a decimal digit, or is some
other numeric symbol.
"""
re_digit = re.compile(r'\d')
sample = '1\xbc\xb2\u0969\u136b\u216b\u2466\u2480\u3285'

for char in sample:
    print('U+%04x' % ord(char),
          char.center(6),
          're_digit' if re_digit.match(char) else '-       ',
          'isdig' if char.isdigit() else '-    ',
          'isnum' if char.isnumeric() else '-    ',
          format(numeric(char), '5.2f'),
          name(char),
          sep='\t')
