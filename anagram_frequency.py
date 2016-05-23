"""
The main program reads cached table if it exists and revises weights.

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

TWL06.txt tournament word list, and count_1w.txt copied from Peter Norvig:   http://norvig.com/ngrams/
"""


from collections import defaultdict
from os import path
from csv import reader


source_file = 'TWL06.txt'
output_suffix = '.anagram.csv'
output_file = 'anagram_words.txt'
frequency_file = 'count_1w.txt'


def main():
    """
    If table does not exist, generate from frequencies.
    Sort by weights.
    """
    table_file = source_file + output_suffix
    if not path.exists(table_file):
        words = read_first_words(source_file)
        table = to_table(words)
        frequencies = read_first_words(frequency_file)
        table = sort_short_and_frequent(table, frequencies)
        open(table_file, 'wb').write(to_text(table))
    else:
        table = read_csv(table_file)
        table = sort_weight(table)
        open(table_file, 'wb').write(to_text(table))
    open(output_file, 'wb').write(to_first_word_text(table))


def read_csv(table_file):
    """
    A robust version would be:
    http://stackoverflow.com/questions/11665628/read-data-from-csv-file-and-transform-to-correct-data-type
    """
    with open(table_file, 'rb') as file:
        reads = reader(file)
        table = []
        for row in reads:
            trow = []
            for column in row:
                if column.isdigit():
                    trow.append(int(column))
                else:
                    trow.append(column)
            table.append(trow)
    return table


def to_first_word_text(table):
    """
    >>> table = [('word_length', 'words'), 
    ...     [3, 'ATE', 'EAT'], 
    ...     [4, 'RATE', 'TEAR']]
    >>> print(to_first_word_text(table))
    ATE
    RATE
    """
    column = -1
    for index, fieldname in enumerate(table[0]):
        if fieldname.startswith('words'):
            column = index
            break
    rows = [row[column] for row in table[1:]]
    text = '\n'.join(rows)
    return text

    
def to_table(words, anagram_count_min = 3, word_length_min = 3,
        word_length_max = 10):
    length_anagrams = make_anagrams(words)
    total = len(length_anagrams)
    table = []
    length_max = min(word_length_min + total, word_length_max + 1)
    for word_length in range(word_length_min, length_max):
        if word_length in length_anagrams:
            anagrams = length_anagrams[word_length]
            rows = []
            for anagram in anagrams.values():
                anagram_length = len(anagram)
                if anagram_count_min <= anagram_length:
                    row = [word_length, anagram_length] + anagram
                    rows.append(row)
            rows.sort(_compare_0_1_reversed)
            table.extend(rows)
    table.insert(0, ('word_length', 'anagram_count', 'words'))
    return table


def read_first_words(source_file):
    lines = open(source_file).read().strip().splitlines()
    words = [line.split()[0] for line in lines]
    return words


def to_text(table):
    lines = [','.join([str(i) for i in line])
        for line in table]
    text = '\n'.join(lines)
    return text


def _compare_0_1_reversed(a, b):
    if a[0] < b[0]:
        return -1
    elif b[0] < a[0]:
        return 1
    elif b[1] < a[1]:
        return -1
    elif a[1] < b[1]:
        return 1
    elif a[2] < b[2]:
        return -1
    elif b[2] < a[2]:
        return 1
    else:
        return 0
        

def make_anagrams(words):
    keys = []
    lengths = defaultdict(defaultdict)
    words.sort()
    for word in words:
        sorted_letters = ''.join(sorted(word))
        word_length = len(word)
        if word_length not in lengths:
            lengths[word_length] = defaultdict(list)
        lengths[word_length][sorted_letters].append(word)
    return lengths


def sort_short_and_frequent(table, frequencies):
    frequencies = [word.lower() for word in frequencies]
    frequency_count = len(frequencies)
    sorted_table = []
    for row in table[1:]:
        frequency_row = list(row[:2])
        frequency = []
        for word in row[2:]:
            lower = word.lower()
            if lower in frequencies:
                index = frequencies.index(lower)
                percent = int(100 * float(frequency_count - index) / frequency_count)
            else:
                percent = 0
            frequency.append((-percent, word))
        frequency.sort()
        for percent, word in frequency:
            frequency_row.append(word)
            frequency_row.append(-percent)
        sorted_table.append(frequency_row)
    sorted_table.sort(_compare_length_frequency_sum)
    header = list(table[0])
    header[-1] = 'words_frequencies'
    sorted_table.insert(0, header)
    return sorted_table


def sort_weight(table):
    rows = table[1:]
    rows.sort(_compare_length_frequency_sum)
    return [table[0]] + rows


def _weight(entry):
    weight = 500 * entry[0] ** 0.25
    for i in range(3, len(entry), 2):
        weight -= entry[i]
    return weight


def _compare_length_frequency_sum(a, b):
    a_weight = _weight(a)
    b_weight = _weight(b)
    if a_weight < b_weight:
        return -1
    elif b_weight < a_weight:
        return 1
    else:
        return 0


if '__main__' == __name__:
    import sys
    if len(sys.argv) <= 1:
        main()
    import doctest
    doctest.testmod()
