# anagram-frequency
Words sorted shortest first, then most anagrams second.

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
        'price'
        >>> table = sort_short_and_frequent(table, frequencies)
        >>> print(to_text(table))
        word_length,anagram_count,words_frequencies
        3,3,EAT,90,TEA,80,ATE,40
        3,2,TAB,60,BAT,50
        4,2,RATE,70,TEAR,30
        5,2,PRICE,100,RECIP,20
        5,4,STOUR,10,ROUST,0,ROUTS,0,TROUS,0

Extract first words.

        >>> print(to_first_word_text(table))
        EAT
        TAB
        RATE
        PRICE
        STOUR


Credits
=======

TWL06.txt tournament word list, and count\_1w.txt copied from Peter Norvig:   http://norvig.com/ngrams/
See their copyrights.

en.txt frequency word list compiled from open subtitles 2012 by Hermit Dave and is licensed:
"Creative Commons – Attribution / ShareAlike 3.0 license applies to the use of the word lists."
https://invokeit.wordpress.com/frequency-word-lists

Here are related algorithms to find anagrams:

http://rosettacode.org/wiki/Anagrams#Python

http://stackoverflow.com/questions/6555046/how-can-i-speed-up-this-anagram-algorithm

http://interactivepython.org/runestone/static/pythonds/AlgorithmAnalysis/AnAnagramDetectionExample.html

http://codereview.stackexchange.com/questions/75023/optimizing-an-anagram-solver?newreg=4ad79b0c1ffc4775a3dd8af1559f3a79

https://blogs.msdn.microsoft.com/ericlippert/2009/02/04/a-nasality-talisman-for-the-sultana-analyst/
