Changelog
=========

Version 3.0.0 (2024-04-03)
--------------------------

- Added Cython 3 compatibility. Thanks to @galaxy001 for the contribution!
  Since this means dinopy is no longer compatible with Cython 2, this 
  requires a major version change.
- Deprecated compatibility for Python 3.5 to 3.7.
- Added compatibility with Python 3.11 and 3.12.
- Added readthedocs config file.



Version 2.2.1 (2022-03-22)
--------------------------

- Added ``pyproject.toml`` to correctly handle build dependencies
  (see `Issue #11 <https://bitbucket.org/HenningTimm/dinopy/issues/11>`__).
  Thanks to Sanjay Kumar Srikakulam for the input!
- Added compatibility with Python 3.10



Version 2.2.0 (2020-04-22)
--------------------------

Removed the pre-cythonized .c-files from the repository since they were always
created using a specific Python ABI. Always cythonizing on installation makes
Cython a hard requirement, but increases the compatibility with different Python
releases.

Other Changes
~~~~~~~~~~~~~

- Added test pipeline.
- Fixed some typos in the documentation.


Version 2.1.0 (2020-04-16)
--------------------------

Other Changes
~~~~~~~~~~~~~

- Clarified documentation of FASTQ reader return types.
- Added support for Python 3.8
  

Version 2.0.3 (2019-11-04)
--------------------------

Bugs Fixed
~~~~~~~~~~
- Updated required numpy version to a version compatible with the one used to generate the .c files.
  This lead to an error with a :ref:`cryptic error message<numpy_error>`.


Version 2.0.2 (2019-10-22)
--------------------------


Bugs Fixed
~~~~~~~~~~

- FASTA reader no longer fails on empty files, when `read_names=True` is set.
  Now reading an empty file works without error, allowing to pass over empty files.

- Error messages for FASTA files missing the inital `>` of the first name line are now more informative.


Other Changes
~~~~~~~~~~~~~

- Added test for accessing index FASTA files by index.

- Clarified some test names.

- Minor work on documentation.

- Reformatted code.


Version 2.0.1 (2018-08-17)
--------------------------

Other Changes
~~~~~~~~~~~~~

- Generated new .c files that play nicely with Python 3.7.
  The old Cython version (25.2) generated code that 
  `conflicted with Python 3.7 <https://github.com/cython/cython/issues/1978#ref-issue-345098121>`__.
  The files cythonized with Cython 28.5 do not have this problem.


Version 2.0.0 (2017-4-19)
-------------------------

New Features
~~~~~~~~~~~~
- Added NamelineParser for automagic interpretation of FASTQ namelines.

- Added reader and writer classes for SAM files.


API Changes
~~~~~~~~~~~
- Changed behaviour of 2bit/ 4bit

- The ``names`` parameter of ``FastqReader.reads`` has been renamed to ``read_names`` to be consistent with the signature of ``FastaReader.reads``.

Other Changes
~~~~~~~~~~~~~

- Replaced named tuples with cdef classes to increase performance and flexibility.
  The classes should handle a lot like the tuples.

- Removed Cython as a dependency. It is now an extra requirement.
  To install dinopy with Cython support use ``$ pip install dinopy[cython]``.
  Conda does not offer this functionality yet, hence you need to manually install Cython.

- Added sphinx >= 1.4 as requirement to build the documentation (needed for images).

- Several minor documentation changes.

Bugs Fixed
~~~~~~~~~~

- When creating solid q-grams using a shape consisting of only one character, a random shape
  was generated. This is fixed and behaves as expected: ``[1,1,1] -> ###``.




Version 1.2.1 (2016-05-12)
--------------------------

Other Changes
~~~~~~~~~~~~~

- Adopted a shorter notation for code in docstrings using ``default_role = 'any'``. This should greatly improve readability, especially when using the `help` function.

- Updated documentation to include installation via bioconda.

- Added problem with missing C-compiler to FAQ.

- Added more tests for `fai_io`.

- Added missing file for `fai_io` tests.

- Code blocks about installation in the README.rst are now properly indented.

- Added an example for counting gapped q-grams.


Version 1.2.0 (2016-01-07)
--------------------------

New Features
~~~~~~~~~~~~

- The `replace_ambiguities` processor resolves IUPAC
  ambiguity codes by replacing them. For example an ``N`` is replaced by ``A``, ``C``, ``G`` or ``T``,
  ``Y`` would be replaced by either ``C`` or ``T``.
  For mutable data types, like bytearray, this works on the input data without creating a copy.

API Changes
~~~~~~~~~~~

- Bit encoding of q-grams no longer uses leading sentinel bits.
  This feature was intended to allow variable length bit encoded sequences::

     Sequence   2-bit with sentinel         2-bit w/o sentinel

       AAA        0b 11 00 00 00  = 192      0b 00 00 00  = 0
        AA           0b 11 00 00  =  48         0b 00 00  = 0

  Per default, all functions will now use bit encoding **without** sentinel bits.
  All functions dealing with bit encoding now have a sentinel parameter,
  which can be set to ``True`` to get the old behavior back.

  The new behavior has the advantage, that encoded q-gram of the same length map nicely to
  the numbers ``0 .. 2^(2q)-1``. This can, for example, be used to directly index
  data structures.

- The leading ``+`` is no longer removed from FASTA name lines.
  When using the :meth:`~dinopy.fasta_reader.FastaReader.lines` method sequence and name lines
  could not be easily distinguished. 


Other Changes
~~~~~~~~~~~~~

- The writer classes now use a general output opener.

- Several minor fixes in the documentation.


Bugs Fixed
~~~~~~~~~~

- The documentation of the suffix array processor is now completely visible.


Version 1.1.2 (2015-12-04)
--------------------------

Other Changes
~~~~~~~~~~~~~

- Clarified documentation of FASTQ reader.

- Removed notes from changelog.

- Removed documentation for deprecated width parameter in FASTA writer.

- Added new installation options (pip, conda) to documentation.


Version 1.1.1 (2015-11-23)
--------------------------

Other Changes
~~~~~~~~~~~~~

- Added cythonized ``.c`` files to the repository to allow installing dinopy without Cython.
  To convert the ``.pyx`` sources to C code yourself, you can pass the ``--cythonize`` parameter
  to the ``setup.py`` script. Example::

      (dinopy)me@machine:~$ python setup.py build_ext --inplace --cythonize
      or
      (dinopy)me@machine:~$ python setup.py install --cythonize

  This is only necessary if you have modified the code and your ``.c`` files are outdated.

- Installation has been tested on OS X and Arch Linux.

- Added conversion of ``README.md`` to ReStructured Text format in order required by PyPI.

- Updated the README

Bugs Fixed
~~~~~~~~~~

- Fixed a bug where the wrapper for the suffix array code was not detected properly.


Version 1.1.0 (2015-09-29)
--------------------------

New Features
~~~~~~~~~~~~

- random access to FASTA files if a matching fasta index file (*fai-file*) is available

  - Doc: :meth:`~dinopy.fasta_reader.FastaReader.random_access`
  - Example::
      
      import dinopy
      far = dinopy.FastaReader("foo.fasta", write_fai=True)  # if no fai file is found, will create one
      
      # accessing subsequences of chromosomes
      seq1a = far.random_access('chromosome_I', 21, 36)  # subsequence from index 21 (inclusive) to 36 (exclusive) in chromosome_I of 'foo.fasta'
      seq1b = far.random_access(0, 21, 36)  # supports both access by chromosome name and by index
      seq2a = far[('chromosome_I', 21, 36)]  # syntactic sugar
      seq2b = far[(0, 21, 36)]  # → seq1a == seq1b == seq2a == seq2b
      seqs = far[[(0, 21, 36), (1, 2, 3), ('chromosome_II', 6, 12)]]  # lists are okay, too
      
      # accessing chromosomes
      chromosomes1 = far[0]  # will return the whole first chromosome
      chromosomes2 = far[[0, 2]]  # will return the first and the third chromosome
      chromosomes3 = far[['chromosome_I', 2]]  # mixed mode works, too. chromosomes2 == chromosomes3 iff 'chromosome_I' is the first chromosome in 'foo.fasta'
      

- linear time suffix array computation of byte-sequences using SAIS

  - Doc: `dinopy.processors.suffix_array`
  - Example::
      
      from dinopy.processors import suffix_array
      sa = suffix_array(b"mississippi$")
      print(list(sa))  # [11, 10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]


Other changes
~~~~~~~~~~~~~~~~~~~~~~~~~~

- Always assume '\\n' as line separator where manual checks occur. Note that lines are stripped off of their line separators using ``rstrip`` anyway.

- Added AUTHORS.rst with affiliation information.

- General comment and test cleanup.

- More tests!
