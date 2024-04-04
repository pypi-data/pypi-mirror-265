.. _dtype:
.. role:: py(code)
   :language: python

=================
Note about dtype
=================
By default, almost every operation in dinopy will return results in the Python
type ``bytes``. However, most of these operations accept the keyword argument
``dtype`` which may be set to any of the following values:

* ``bytes``
    Return the ascii-encoded bases as python ``bytes``, e.g.
    ``b'ACGT'`` (which is basically the same as ``[65, 67, 71, 84]``).
    This is the default.

* ``bytearray``
    A mutable version of bytes.

* ``str``
    Return the result as utf-8 string (capital letters), e.g. ``"ACGT"``.

* ``basenumbers``
    Maps ``A → 0, C → 1, G → 2, T → 3, N → 4, ...``, e.g.
    ``[0, 1, 2, 3]`` (or, more correctly, as ``bytes``: ``b'\x00\x01\x02\x03'``).

Sometimes, as is the case with `dinopy.processors.qgrams`, you can also supply
the keyword argument 'encoding' with either of the following values:

* ``two_bit``
    Encodes the result as a ``long`` integer. If characters other than ``"ACGT"``
    are encountered, they will be randomly replaced according to the usual IUPAC mapping
    (see `iupac_mapping` for details).

* ``four_bit``
    Basically the same as two_bit, but does not need to replace characters
    other than ``"ACGT"``, as each character of the IUPAC specification can
    be encoded using exactly 4 bit.
    For example, ``"ACGTM"``  translates to ``0b 0001 0010 0100 1000 0011``.

.. Note::
    All of these types can be accessed like `dinopy.two_bit` or `dinopy.definitions.two_bit`.

    You can use the functions `dinopy.conversion.encode` and `dinopy.conversion.decode` to manually
    convert qgrams to and from 2bit / 4bit encoding.


.. _`iupac_mapping`:

IUPAC mapping
=============
DNA sequences may contain characters other than ``A, C, G`` or ``T``, namely:
``N, U, R, Y, M, K, W, S, B, D, H`` and ``V``.
If such a character is encountered while encoding a sequence to a single long
integer two-bit representation, they will get replaced *randomly* (uniform) according
to the following mapping:

    ==================== = = = =
    Character            Replace
    ==================== =======
    N                    A C G T
    U                          T
    R                    A   G
    Y                      C   T
    M                    A C    
    K                        G T
    W                    A     T
    S                      C G  
    B                      C G T
    D                    A   G T
    H                    A C   T
    V                    A C G  
    ==================== = = = =
