.. _faq:

===
FAQ
===

Installation
------------

How do I install dinopy?
^^^^^^^^^^^^^^^^^^^^^^^^

The recommended ways to install dinopy are with conda_ (using the bioconda_ channel) or from PyPI using pip.
You can also download the code from out bitbucket_ repository or PyPI_ and compile it yourself.

.. _conda: https://www.continuum.io/downloads
.. _bioconda: https://github.com/bioconda/bioconda-recipes
.. _bitbucket: https://bitbucket.org/HenningTimm/dinopy
.. _PyPI: https://pypi.python.org/pypi/dinopy

Do I need Cython to use dinopy?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Since version 2.2.0, Cython is required to install dinopy.

Prior to version 2.2.0 Cython was not a requirement as all extension modules were packaged as ``.c``-files.
For these versions, you only need to compile these extension modules, which does not require Cython. 
This is handled by setuptools and is automatically executed when you install dinopy, as long as you have the ``build-essential`` package installed.


During testing a lot of KeyErrors are raised.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Running ::

    nosetests -v --nocapture

yields a lot of the following KeyErrors::

   ERROR: Does the iteration over qgrams work correctly?
   ----------------------------------------------------------------------
   Traceback (most recent call last):
       File "/vol/home/timm/repos/dna_handler/test/fasta_parser_test.py", line 295, in test_iterate_qgrams
           chr1_sequence = cnv.string_to_bytes("ACGTTGCATCTACGTTGCATCTACGTTGCATCACGTTGCATCTACGTTGCATCTACGTTGCATCACGTTGCATCTACGTTGCATCTACGTTGCATC")
       File "conversion.pyx", line 112, in dinopy.conversion.string_to_bytes (dinopy/conversion.c:3308)
       File "conversion.pyx", line 127, in dinopy.conversion.string_to_bytes (dinopy/conversion.c:3168)
   KeyError: 65

This is due to an old (<0.20) Cython version. 

To fix this issue, please download a newer Cython version and install it.

The version used can either be checked by importing the Cython module in the interpreter.::

    >>> import Cython
    >>> Cython.__version__
    '0.22'

or by running::

    user@machine:~$ cython --version
    Cython version 0.22

on a terminal of your choice.


Building dinopy fails with: ``gcc: error trying to exec 'cc1plus'``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The installation of dinopy fails during the compilation step with the following error.::

    me@machine:~$ pip install dinopy
    [...]
    .linux-x86_64-3.5/dinopy/wrap_sais.o -O3
      gcc: error trying to exec 'cc1plus': execvp: No such file or directory
      error: command 'gcc' failed with exit status 1
    
      ----------------------------------------
      Failed building wheel for dinopy
    Failed to build dinopy
    Installing collected packages: dinopy
      Running setup.py install for dinopy
        Complete output from command /home/timm/anaconda3/envs/dinoenv/bin/python3 -c "import setuptools, tokenize;__file__='/tmp/pip-build-5oyzgq9i/dinopy/setup.py';exec(compile(getattr(tokenize, 'open', open)(__file__).read().replace('\r\n', '\n'), __file__, 'exec'))" install --record /tmp/pip-p5ogilb7-record/install-record.txt --single-version-externally-managed --compile:
        running install
        running build
        running build_py
        running build_ext
        building 'dinopy.wrap_sais' extension
        gcc -pthread -Wsign-compare -Wunreachable-code -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -fPIC -Idinopy/cpp/ -I/home/timm/anaconda3/envs/dinoenv/include/python3.5m -c dinopy/wrap_sais.cpp -o build/temp.linux-x86_64-3.5/dinopy/wrap_sais.o -O3
        gcc: error trying to exec 'cc1plus': execvp: No such file or directory
        error: command 'gcc' failed with exit status 1
    
        ----------------------------------------
    Command "/home/timm/anaconda3/envs/dinoenv/bin/python3 -c "import setuptools, tokenize;__file__='/tmp/pip-build-5oyzgq9i/dinopy/setup.py';exec(compile(getattr(tokenize, 'open', open)(__file__).read().replace('\r\n', '\n'), __file__, 'exec'))" install --record /tmp/pip-p5ogilb7-record/install-record.txt --single-version-externally-managed --compile" failed with error code 1 in /tmp/pip-build-5oyzgq9i/dinopy

Dinopy requires `cc1plus`, the c++ compiler, which is not pre-installed on a vanilla ubuntu.
This can be solved by installing the ``build-essential`` package.::

    me@machine:~$ sudo apt-get install build-essential
    me@machine:~$ pip install dinopy

    Collecting dinopy
      Using cached dinopy-1.2.0.tar.gz
    Requirement already satisfied (use --upgrade to upgrade): numpy>=1.9 in /home/timm/anaconda3/envs/dinoenv/lib/python3.5/site-packages (from dinopy)
    Requirement already satisfied (use --upgrade to upgrade): cython>=0.22 in /home/timm/anaconda3/envs/dinoenv/lib/python3.5/site-packages (from dinopy)
    Building wheels for collected packages: dinopy
      Running setup.py bdist_wheel for dinopy
      Stored in directory: /home/timm/.cache/pip/wheels/e3/7d/99/a140b9cef01ff2bf07ef28a0df1595a1b1f5cd7165afc20ae2
    Successfully built dinopy
    Installing collected packages: dinopy
    Successfully installed dinopy-1.2.0


``ImportError: No module named 'dinopy.output_opener'`` is raised when importing dinopy in the interpreter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After installing dinopy from the sources using ``me@machine:~$ python setup.py install`` dinopy can not be imported.

Python interpreter version of the error::

    >>> import dinopy
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/home/timm/repos/dinofoo/dinopy/__init__.py", line 15, in <module>
        from .output_opener import OutputOpener
    ImportError: No module named 'dinopy.output_opener'

IPython version::
    
    In [1]: import dinopy
    ---------------------------------------------------------------------------
    ImportError                               Traceback (most recent call last)
    <ipython-input-1-e19a24a8118b> in <module>()
    ----> 1 import dinopy
    
    /home/timm/repos/dinofoo/dinopy/__init__.py in <module>()
         13 __all__ = ['fasta_reader', 'fasta_writer', 'fastq_reader', 'fastq_writer', 'auxiliary', 'shaping', 'shape',
         14            'processors', 'definitions', 'exceptions', 'output_opener', 'nameline_parser', 'sambam', 'sam_reader', 'sam_writer']
    ---> 15 from .output_opener import OutputOpener
         16 from .fastq_reader import FastqReader
         17 from .fasta_reader import FastaReader
    
    ImportError: No module named 'dinopy.output_opener'
    
This error occurs, when the interpreter is started in the dinopy repository.
For example if you checked out to ``~/repos/dinopy``, installed ``me@machine:~/repos/dinopy$ python setup.py install`` and started python ``me@machine:~/repos/dinopy$ python``.

Python will first check the local folder for imports according to ``sys.path``.
There it will find a folder named dinopy that contains an ``__init__.py`` and will happily try to use the folder as the dinopy package.
The Cython extensions are not compiled locally though, so the ``.so`` are missing there, rendering ``output_opener`` an undefined import.

To solve this, leave the dinopy repository structure and retry.
For projects that use dinopy as a dependency this should not be a problem.


After locally building the documentation all module pages are empty
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When building the documentation, sphinx traverses the package and imports all autodoc modules (extensions) in order to get the docstrings.
As the extensions are implemented in Cython the modules are compiled as ``.so`` files, which can be imported by python.
After running ``python setup.py install`` the ``.so`` files are copied to the installation target.
The documentation configuration file expects those extensions to be in the local dinopy package though.

To solve this run ``python setup.py build_ext --inplace``.
This compiles the ``.c`` extensions and places the ``.so`` files next to their ``.pyx`` and ``.c`` files.
After this sphinx should find the modules and build the autodoc pages.



``numpy.ufunc has the wrong size, try recompiling. Expected 192, got 216`` is raised when importing dinopy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. _numpy_error:

If installed together with other packages, conda can install a numpy version incompatible with the one used to generate the .c files.
This results in the following error message::

    Python 3.6.7 | packaged by conda-forge | (default, Jul  2 2019, 02:18:42) 
    Type 'copyright', 'credits' or 'license' for more information
    IPython 7.8.0 -- An enhanced Interactive Python. Type '?' for help.
    
    In [1]: import dinopy as dp
    ---------------------------------------------------------------------------
    ValueError                                Traceback (most recent call last)
    <ipython-input-1-60b1ad065020> in <module>
    ----> 1 import dinopy as dp
    
    ~/miniconda3/envs/dino2/lib/python3.6/site-packages/dinopy/__init__.py in <module>
         14            'processors', 'definitions', 'exceptions', 'output_opener', 'nameline_parser', 'sam_reader',  'sam_writer', 'sambam']
         15 from .output_opener import OutputOpener
    ---> 16 from .fastq_reader import FastqReader
         17 from .fasta_reader import FastaReader
         18 from .fastq_writer import FastqWriter
    
    __init__.pxd in init dinopy.fastq_reader()
    
    ValueError: numpy.ufunc has the wrong size, try recompiling. Expected 192, got 216

   
This can be solved by updating the numpy version, for example using ``conda update numpy`` or ``pip install numpy --upgrade``.
A similar error is described `here <https://stackoverflow.com/q/53904157/2862719>`__.
