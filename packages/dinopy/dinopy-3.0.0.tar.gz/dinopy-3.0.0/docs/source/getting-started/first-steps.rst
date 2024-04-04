.. role:: py(code)
   :language: python
.. _first-steps:

=======================
First Steps with dinopy
=======================

Installation
============

There are three ways to install dinopy:

  * With pip: ``$ pip install dinopy``
  * With conda: ``$ conda install -c bioconda dinopy``
  * From the source code: ``$ python setup.py install``

Using the Library
=================

Depending on your use-cases, different parts of dinopy might be of interest to you.
For this tutorial, we'll be interested in parsing FASTA files, so let's start
by importing the dinopy main module and create a FastaReader for a given file
located at ``"foobar.fasta"`` ::

    import dinopy
    
    far = dinopy.FastaReader("foobar.fasta")

Having done that, let's simply count its bigrams by reading the whole genome
and then using the `dinopy.processors.qgrams`-processor to generate bi-grams::

    counts = {}
    for bigram in dinopy.qgrams(far.genome().sequence, 2):
        counts[bigram] = counts.get(bigram, 0) + 1

Or even more pythonic::

    from collections import Counter
    counts = Counter(dinopy.qgrams(far.genome().sequence, 2))

.. note::

    1.
        `genome` is a named tuple consisting of the elements ``sequence``
        (which contains the genome data) and ``info`` (which is a collection of
        named tuples of the following structure: ``(name, length, interval)``,
        where ``interval`` is a ``(start_index, end_index)`` tuple).
        
        That means that you can both use tuple-unpacking, as in :code:`seq, info = far.genome()`
        and member-like access, as in :code:`seq = far.genome().sequence`.
        
    2.
        `genome` reads the complete genome to memory. If you do not
        want this (because it might not fit into memory) supply `chromosomes`
        or even `lines` instead, as this will provide an iterator over each chromosome
        (or line, respectively) in the file.
        However, you will also have to enable 'qgram-wrapping' to achieve the same result::

            dinopy.qgrams(fasta_parser.reads(), 2, wrap=True)

        The above expression is then equivalent to :code:`dinopy.qgrams(far.genome()['sequence'], 2)`
        but does not read the whole genome to memory.

.. note::

    `qgrams` accepts a multitude of different shape representations,
    most commonly integers (as used above) or strings consisting of "#" (care)
    and "\_" (don't care).
    For more information on shapes, see :mod:`dinopy.shape` and :mod:`dinopy.shaping`.


To write reads to disk in FASTQ format you can use the FastqWriter class.
All writer classes of dinopy use with-environments, to ensure the output file is
closed properly in case something goes wrong.

Lets suppose we want to synthesize reads to test an algorithm. We want to use the genome
that we read in using the FastaReader in the above example and have a function
``random_read`` in the module ``helper`` which randomly generates a read from a sequence::

    import dinopy
    from helper import random_read

    far = dinopy.FastaReader("foobar.fasta")
    genome = far.genome()
    with dinopy.FastqWriter("foobar_reads.fastq") as fqw:
        for _ in range(10000):
            seq, name, quality = random_read(genome.sequence)
            fqw.write(seq, name, quality)

Note that the output file will automatically be closed once you leave the environment.
In case you would like to have direct control over the opening and closing of the file,
or you need a variable amount of writers, you can directly use the :meth:`~dinopy.fastq_writer.FastqWriter.open` and :meth:`~dinopy.fastq_writer.FastqWriter.close`
methods of the FASTQ Writer. Our code from above would then look like this::

    import dinopy
    from helper import random_read

    far = dinopy.FastaReader("foobar.fasta")
    genome = far.genome()
    
    fqw = dinopy.FastqWriter("foobar_reads.fastq")
    fqw.open()
    for _ in range(10000):
        seq, name, quality = random_read(genome.sequence)
        fqw.write(seq, name, quality)
    fqw.close()

And that's basically it. If you wish to read Fastq files, simply replace
*Fasta* with *Fastq* (:mod:`dinopy.fastq_reader`).
Similarly, if you wish to *write* files, replace *Reader*
with *Writer* (:mod:`dinopy.fasta_writer` and :mod:`dinopy.fastq_writer`).


