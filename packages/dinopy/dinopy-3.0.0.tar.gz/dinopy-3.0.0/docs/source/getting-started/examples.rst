.. role:: py(code)
   :language: python
.. _examples:

=========================
Examples
=========================


* Example: Operation on all 5-grams of a FASTA file::

        import dinopy
        from dinopy import qgrams

        far = dinopy.FastaReader("ecoli.fasta")
        sequence, info = far.genome()
        for qgram in qgrams(sequence, 5):
            print(qgram)


* Example: Perform an analysis on each read of a file::

        import dinopy
        import numpy as np

        fqr = dinopy.FastqReader("ecoli_reads.fastq")
        for sequence, name, quality_values in fqr.reads(quality_values=True):
            qvs = np.frombuffer(quality_values)
            if np.mean(qvs) > arbitrary_threshold:
                important_analysis(sequence)
            else:
                low_quality(sequence)


* Example: Work on all lines of a zipped FASTQ file::

        import dinopy
        import numpy as np

        fqr = dinopy.FastqReader("ecoli_reads.fastq.gz")
        for line_type, line_value in fqr.lines():
            if line_type == "name":
                print("Found a read with the name", line_value)
            elif line_type == "quality values":
                print("with the mean quality value", np.mean(np.frombuffer(line_value, dtype=np.uint8)))


* Example: Create a 5-gram counter for all reads of a FASTA file::

        import dinopy
        from collections import Counter

        fp = dinopy.FastaReader("ecoli.fasta")
        counts = Counter(dinopy.qgrams(fp.reads(), 5))


* Example: Create a naïve 4-gram index for a genome::

        import dinopy

        far = dinopy.FastaReader("ecoli.fasta")
        index = {}
        for i, qgram in enumerate(dinopy.qgrams(far.genome().sequence, 4, encoding=dinopy.two_bit)):
            if qgram in index:
                index[qgram].append(i)
            else:
                index[qgram] = [i]

* Example: Read a genome, write a genome::

        import dinopy

        far = dinopy.FastaReader("ecoli.fasta")
        with dinopy.FastaWriter("baz.fasta") as faw:
            faw.write_genome(far.genome())

* Example: Calculate suffix array for a given sequence::

        import dinopy

        seq = "mississippi"
        sar = dinopy.processors.suffix_array(seq)  # [11, 10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]


* Example: Count unique gapped-qgram occurences of a given sequence [#]_::

        import dinopy
        from dinopy import qgrams, reverse_complement, FastaReader, two_bit
        from collections import Counter
        from itertools import islice

        q = 16
        shape = '#' * q
        shapes = [shape[:i] + '_' + shape[i:] for i in range(1, q)]  # shapes for 16-grams with 1 gap

        far = FastaReader("human_g1k_v37.fasta.gz")
        iterator = far.lines(skip_name_lines=True)
        iterator = islice(iterator, 500, 500 + 100000)  # skip first few hundred lines of "NNNN...". Note that you could also use filter(lambda x: b'N' not in x, ...)
        seq_fwd = b''.join(list(iterator))  # for this example, we'll keep the data in memory
        seq_rev = reverse_complement(seq_fwd)

        for shape in shapes:
            counts = Counter(qgrams(seq_fwd, shape, encoding=two_bit, dtype=bytes))  # make sure to explicitly specify dtype for better performance
            counts += Counter(qgrams(seq_rev, list(reversed(shape)), encoding=two_bit, dtype=bytes))
            num_unique = sum([1 for v in counts.values() if v == 1])
            print("{}: {}".format(shape, num_unique))



.. rubric:: Footnotes

.. [#] This is actually interesting. 17-qgrams with exactly 1 gap have got as many bits as 16-grams -- 32 bit --
        i.e. still fit in a 32bit integer but they've got more unique occurrences than solid 16-grams, which means mapping
        to a reference is clearer. (Experiments show that 18-grams with 2 gaps, ..., (16+n)-qgrams with n-gaps have
        increasingly more unique occurrences; of course, the shape itself is of importance, too.)
