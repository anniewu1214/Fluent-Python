=================
Text versus Bytes
=================


============ Encoding and Decoding ============


identity of characters vs. specific byte representations:

- code point is the identity of a character: "U+*" where * is a number from 0 to 1114111.
  (base 10), e.g. A -> U+0041, € -> U+20AC.

- the actual bytes that represent a character depend on the encoding in use. An encoding
  is an algorithm that convert code points to byte sequences (encoding) and vice versa.
  (decoding) e.g. in UTF-8 A -> \x41, in UTF-16LE A -> \x41\x00.

    >>> s = 'café'
    >>> len(s)  # The str 'café' has 4 unicode characters
    4
    >>> b = s.encode('utf-8')  # encode str to bytes using UTF-8 encoding
    >>> b  # bytes b has five bytes, the code point for 'é' is encoded as two bytes in UTF-8
    b'caf\xc3\xa9'
    >>> len(b)
    5
    >>> b.decode('utf-8')  # decode bytes to str
    'café'
    >>> for codec in ['latin_1', 'utf_8', 'utf_16']:
    ...     print(codec, 'El Niño'.encode(codec), sep='\t')
    ...
    latin_1 b'El Ni\xf1o'
    utf_8   b'El Ni\xc3\xb1o'
    utf_16  b'\xff\xfeE\x00l\x00 \x00N\x00i\x00\xf1\x00o\x00'



============ Byte Essentials ============


- Two build-in types for binary sequences: immutable bytes type and mutable bytearray.

- Each item in bytes or bytearray is an integer from 0 to 255. A slice of a binary seq
  always produces a binary seq of the same type.

- binary seqs are really seqs of integers, different displays are used:
    * for bytes in the printable ASCII range, the ASCII character itself is used
    * for bytes corresponding to tab, newline, carriage return, and \, the escape seq \t, \n, \r, and \\ are used
    * for every other byte value, a hexadecimal escape seq is used. (e.g. \x00 is the null type)

- creating a bytes or bytearray obj from any buffer-like sources will always copy the bytes.
  memoryview provides shared memory access to slices of data from other binary seqs, packed
  arrays, etc. without copying the bytes.

    >>> cafe = bytes('café', encoding='utf8')  # bytes can be built from a str, given an encoding
    >>> cafe
    b'caf\xc3\xa9'
    >>> cafe[0]  # each item is an integer in range(256)
    99
    >>> cafe[:1]  # slices of bytes are also bytes
    b'c'
    >>> cafe_arr = bytearray(cafe)
    >>> cafe_arr
    bytearray(b'caf\xc3\xa9')
    >>> cafe_arr[-1:]  # a slice of bytearray is also bytearray
    bytearray(b'\xa9')



============ UnicodeError ============


UnicodeError:
    - UnicodeEncodeError, when converting str to binary sequences
    - UnicodeDecodeError, when reading binary sequence into str

    >>> city = 'São Paulo'
    >>> city.encode('utf_8')
    b'S\xc3\xa3o Paulo'
    >>> city.encode('utf_16')
    b'\xff\xfeS\x00\xe3\x00o\x00 \x00P\x00a\x00u\x00l\x00o\x00'
    >>> city.encode('iso8859_1')
    b'S\xe3o Paulo'
    >>> city.encode('cp437')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
      ...
    UnicodeEncodeError: 'charmap' codec can't encode character '\xe3'...
    >>> city.encode('cp437', errors='ignore')
    b'So Paulo'
    >>> city.encode('cp437', errors='replace')
    b'S?o Paulo'
    >>> city.encode('cp437', errors='xmlcharrefreplace')
    b'S&#227;o Paulo'

    >>> octets = b'Montr\xe9al'
    >>> octets.decode('cp1252')
    'Montréal'
    >>> octets.decode('iso8859_7')
    'Montrιal'
    >>> octets.decode('koi8_r')
    'MontrИal'
    >>> octets.decode('utf_8')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 5: invalid continuation byte
    >>> octets.decode('utf_8', errors='replace')
    'Montr�al'



============ Handling Text Files ============


- Best practice for text processing:
    * bytes -> str  decode bytes on input
    * 100% str      process text only
    * str -> bytes  encode text on output


- Code that has to run on multiple machines or on multiple occasions should never depend on
  encoding defaults. Always pass an explicit ``encoding=`` arg when opening text files.

- Do not open text files in binary mode.

- The best advice about encoding defautls is: do not rely on them


    >>> fp = open('cafe.txt', 'w', encoding='utf_8')
    >>> fp  # by default, open operates in text mode and returns a TextIOWrapper object
    <_io.TextIOWrapper name='cafe.txt' mode='w' encoding='utf_8'>
    >>> fp.write('café')  # returns the number of unicode characters written
    4
    >>> fp.close()
    >>> import os
    >>> os.stat('cafe.txt').st_size  # os.stat reports that the file holds 5 bytes
    5
    >>> fp2 = open('cafe.txt')
    >>> fp2
    <_io.TextIOWrapper name='cafe.txt' mode='r' encoding='cp1252'>
    >>> fp2.encoding  # inspect the encoding
    'cp1252'
    >>> fp2.read()
    'cafÃ©'
    >>> fp3 = open('cafe.txt', encoding='utf_8')  # open file with the correct encoding
    >>> fp3
    <_io.TextIOWrapper name='cafe.txt' mode='r' encoding='utf_8'>
    >>> fp3.read()
    'café'
    >>> fp4 = open('cafe.txt', 'rb')  # open a file for reading in binary mode
    >>> fp4
    <_io.BufferedReader name='cafe.txt'>
    >>> fp4.read()  # returns bytes
    b'caf\xc3\xa9'

    >>> expressions = """
    ...     locale.getpreferredencoding()
    ...     type(my_file)
    ...     my_file.encoding
    ...     sys.stdout.isatty()
    ...     sys.stdout.encoding
    ...     sys.stdin.isatty()
    ...     sys.stdin.encoding
    ...     sys.stderr.isatty()
    ...     sys.stderr.encoding
    ...     sys.getdefaultencoding()
    ...     sys.getfilesystemencoding()
    ... """
    >>> my_file = open('dummy', 'w')
    >>> for expression in expressions.split():
    ...     value = eval(expression)
    ...     print(expression.rjust(30), '->', repr(value))
    ...
     locale.getpreferredencoding() -> 'UTF-8'
                     type(my_file) -> <class '_io.TextIOWrapper'>
                  my_file.encoding -> 'UTF-8'
               sys.stdout.isatty() -> True
               sys.stdout.encoding -> 'UTF-8'
                sys.stdin.isatty() -> True
                sys.stdin.encoding -> 'UTF-8'
               sys.stderr.isatty() -> True
               sys.stderr.encoding -> 'UTF-8'
          sys.getdefaultencoding() -> 'utf-8'
       sys.getfilesystemencoding() -> 'utf-8'



============ Normalizing Unicode ============


- String comparisons are complicated by the fact that Unicode has
  combining characters: diacritics and other marks that attach to
  the preceding character, appearing as one when printed.


- In the Unicode standard, sequences like 'é' and 'e\u0301' are called “canonical equivalents,”
  and applications are supposed to treat them as the same. But Python sees two different
  sequences of code points, and considers them not equal.

    >>> s1 = 'café'
    >>> s2 = 'cafe\u0301'
    >>> s1, s2
    ('café', 'café')
    >>> len(s1), len(s2)
    (4, 5)
    >>> s1 == s2
    False



============ NFC & NFD ============


- NFC composes the code points to produce the shortest equivalent string
  NFD decomposes, expanding composed chars into base chars and separate combing chars

    >>> from unicodedata import normalize
    >>> len(normalize('NFC', s1)), len(normalize('NFC', s2))
    (4, 4)
    >>> len(normalize('NFD', s1)), len(normalize('NFD', s2))
    (5, 5)
    >>> normalize('NFC', s1) == normalize('NFC', s2)
    True
    >>> normalize('NFD', s1) == normalize('NFD', s2)
    True


- Western keyboards usually generate composed characters, so text typed by users will be
  in NFC by default. However, to be safe, it may be good to sanitize strings with
  normalize('NFC', user_text) before saving.

- Some single characters are normalized by NFC into another signle character. The symbol for ohm is
  normalized to the Greek uppercase omega. They are visually identical, but they compare
  unequal so it is essential to normalize to avoid surprises.

    >>> from unicodedata import normalize, name
    >>> ohm = '\u2126'
    >>> name(ohm)
    'OHM SIGN'
    >>> ohm_c = normalize('NFC', ohm)
    >>> name(ohm_c)
    'GREEK CAPITAL LETTER OMEGA'
    >>> ohm == ohm_c
    Falsle
    >>> normalize('NFC', ohm) == normalize('NFC', ohm_c)
    True


============ NFKC & NFKD ============


- In the NFKC and NFKD forms, each compatibility character is replaced by a 'comptaibility'
  decomposition' of one or more chars that are considered a prefered representation, even if there
  is some formatting loss - ideally, the formatting should be the responsablity of external
  markup, not part of Unicode.

    To exemplify, the compatibility decomposition of the one half fraction '½' (U+00BD) is
    the sequence of three characters '1/2', and the compatibility decomposition of the micro
    sign 'μ' (U+00B5) is the lowercase mu 'μ' (U+03BC).

    >>> from unicodedata import normalize, name
    >>> half = '½'
    >>> normalize('NFKC', half)
    '1/2'
    >>> micro = 'µ'
    >>> micro_kc = normalize('NFKC', micro)
    >>> micro, micro_kc
    ('μ', 'μ')
    >>> ord(micro), ord(micro_kc)
    (181, 956)
    >>> name(micro), name(micro_kc)
    ('MICRO SIGN', 'GREEK SMALL LETTER MU')


- NFKC and NFKD may lose or distord information, but they can produce convenient
  intermediate representation for searching and indexing. Not for permanent storage.



============ Case Folding ============


- Case folding is essentially converting all text to lowercase, with some
  additional transformations. For any string s containing only latin1 chars,
  s.casefold() produces the same result as s.lower(), with only two exceptions:

  * the micro sign 'µ' is changed to the Greek lowercase mu
  * and the German Eszette 'ß' becomes 'ss'

    >>> micro = 'µ'
    >>> name(micro)
    'MICRO SIGN'
    >>> micro_cf = micro.casefold()
    >>> name(micro_cf)
    'GREEK SMALL LETTER MU'
    >>> micro, micro_cf
    ('μ', 'μ')
    >>> eszette = 'ß'
    >>> name(eszette)
    'LATIN SMALL LETTER SHARP S'
    >>> eszette_cf = eszette.casefold()
    >>> eszett, eszett_cf
    ('ß', 'ss')