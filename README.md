# anagram-frequency

I plotted log-log and small sample of first and second column.

English word distribution roughly follows a Zipf distribution.

<http://www.intmath.com/exponential-logarithmic-functions/7-graphs-log-semilog.php#zipf>

<https://en.wikipedia.org/wiki/Zipf%27s_law>

Here are samples of word frequency:

![en.txt.loglog.png](en.txt.loglog.png)

![en.txt.xlim\_446.png](en.txt.xlim_446.png)

![count\_1w.txt.loglog.png](count_1w.txt.loglog.png)

![count\_1w.txt.xlim\_326.png](count_1w.txt.xlim_326.png)

Words sorted shortest first, then most anagrams second.

## Estimating difficulty from length and frequency

A longer word has more permutations.

A rarer word is less likely to be considered.

The rarity has a Zipf distribution.

Permutations have a factorial distribution.

To estimate difficulty of solving an anagram, these metrics can be composited together.

Example usage from the command line:

        python anagram_difficulty.py sample_word_list.csv en.txt

That creates an output table sorted by estimate of difficulty from length and frequency.  Here is one sample:

[sample\_word\_list.difficulty.csv](sample_word_list.difficulty.csv)

This appends frequency as seen in the test file.

        >>> from anagram_difficulty import *
        >>> tabulate_file('test_word_list.csv', 'test_frequency.txt')
        'test_word_list.difficulty.csv'

For compatibility with the existing files as in this example file, `tabulate_file` expects header of `word` in the list file, but no header for frequency file.

Word frequency correlated to difficulty.  <http://journals.sagepub.com/doi/abs/10.1111/j.1467-9280.1996.tb00336.x>

However frequency has a heavily biased distribution.  So I caculated the logarithm of the frequency before standardizing.  Otherwise, long words that were also frequent would appear as easy, such as six-letter word "listen" among 3-letter words.

I applied the logarithm to word length also.

To dramatize length, I weighed length more than frequency.

        >>> frequency_weight < length_weight
        True

Although letter permutations is a factorial of length and permutations correlates to difficulty, I appended permutations column and scored by that.  Very long words have too many permutations to compute, so I discarded words over many letters long.  Yet permutations biased the long words too heavily.  So I scored by letter length instead.

To ensure that frequencies and permutations were standardized, I standardized both on the frequency file.  Otherwise there is a bias when the sample word list is not a representative sample of the word frequency list.

To standardize, standard scores were calculated, technically called z-scores.  <https://en.wikipedia.org/wiki/Standard_score>

Reversed z-score of frequency, so that ascending standard score corresponds to ascending difficulty.

Composited z-scores by summing them.  <http://jeromyanglim.blogspot.com/2009/03/calculating-composite-scores-of-ability.html>



# Tabulating

The main program reads cached table if it exists and revises weights.

        >>> from anagram_frequency import *
        >>> main()

It creates a list of single words,
sorted shortest first, most anagrams second.

        >>> words = read_first_words('test_word_list.txt')
        >>> table = to_table(words, 2, 3)
        >>> print(to_text(table))
        word_length,anagram_count,words
        3,3,ATE,EAT,TEA
        3,2,BAT,TAB
        4,2,RATE,TEAR
        5,4,ROUST,ROUTS,STOUR,TROUS
        5,2,PRICE,RECIP

Sort table by sum of word frequency percentiles
weighted with word length.

        >>> frequencies = read_first_words('test_frequency.txt')
        >>> len(frequencies)
        10
        >>> frequencies[0]
        'PRICE'
        >>> frequencies_1 = read_first_words('test_frequency_1.txt')
        >>> frequencies_list = [frequencies, frequencies_1]
        >>> table = sort_short_and_frequent(table, frequencies_list)
        >>> print(to_text(table))
        word_length,anagram_count,words_frequencies
        3,3,EAT,90,TEA,80,ATE,10
        3,2,TAB,60,BAT,50
        4,2,RATE,60,TEAR,30
        5,2,PRICE,50,RECIP,20
        5,4,STOUR,10,ROUST,0,ROUTS,0,TROUS,0

Extract first words.

        >>> print(to_first_word_text(table))
        EAT
        TAB
        RATE
        PRICE
        STOUR

First word in table:

        >>> table = [('word_length', 'words'), 
        ...     [3, 'ATE', 10, 'EAT', 5], 
        ...     [4, 'RATE', 5, 'TEAR', 2]]
        >>> print(to_first_word_text(table))
        ATE
        RATE

Optionally, exclude words from first appearance.  This is useful to not list a word that ruffles the feathers of prudes.

        >>> excludes = ['ATE', 'TEAR']
        >>> print(to_first_word_text(table, excludes))
        EAT
        RATE


Credits
=======

TWL06.txt tournament word list, and count\_1w.txt copied from Peter Norvig:   http://norvig.com/ngrams/
See their copyrights.

en.txt frequency word list compiled from open subtitles 2012 by Hermit Dave and is licensed:
"Creative Commons – Attribution / ShareAlike 3.0 license applies to the use of the word lists."
https://invokeit.wordpress.com/frequency-word-lists

Here are related algorithms to find anagrams:

<http://rosettacode.org/wiki/Anagrams#Python>

<http://stackoverflow.com/questions/6555046/how-can-i-speed-up-this-anagram-algorithm>

<http://interactivepython.org/runestone/static/pythonds/AlgorithmAnalysis/AnAnagramDetectionExample.html>

<http://codereview.stackexchange.com/questions/75023/optimizing-an-anagram-solver?newreg=4ad79b0c1ffc4775a3dd8af1559f3a79>

<https://blogs.msdn.microsoft.com/ericlippert/2009/02/04/a-nasality-talisman-for-the-sultana-analyst/>
