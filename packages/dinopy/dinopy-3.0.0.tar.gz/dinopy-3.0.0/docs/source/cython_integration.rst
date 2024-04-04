.. _Cython API:
.. role:: py(code)
   :language: python


Cython API
==================
Almost all modules of dinopy are implemented in Cython. The .pxd files are included in the dinopy installation,
so you can cimport the c-level functions and classes. See the `sharing declarations <http://docs.cython.org/src/userguide/sharing_declarations.html>`_ entry in the cython documentation for details.


import vs. cimport
==================

All dinopy modules (except the fai_io module) are implemented in Cython and can be cimported.
If you are developing in Cython cimporting can grant a speedup, as only efficient c-level operations are performed.

The modules can be accessed by cimporting dinopy, which provides all c-level classes and functions via the `__init__.pxd` file.

.. note::

    Some functions and all iterators (for example the :func:`qgrams` iterator) are not defined on c-level,
    so they can't be cimported.
    Please use `from dinopy import qgrams` to access these functions.

    It is always advised to both import and cimport dinopy::
      
      import dinopy
      cimport dinopy

    Cython will use c-level functions whenever possible.

data types
==========

The data types needed and returned by dinopy should be documented in the respective functions or methods.
If that somehow is not the case the following rule of thumb applies:

    - `bytes` and `bytearray` use the respective Python / Cython types

    - `basenumbers` are stored as `bytes` (containing only `\\x00 - \\x04`)

    - The return values of FASTA and FASTQ reader are named tuples and are definend in the file `definitions.pyx`

    - The custom encodings and dtypes are defined in `definitions.pxd`

Also if you run into a missing documentation, please let us know.

