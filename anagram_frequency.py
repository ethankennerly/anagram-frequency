"""
List of words, sorted shortest first, most anagrams second.

    >>> words = read('test_word_list.txt')
    >>> table = to_table(words, 2, 3)
    >>> print(to_text(table))
    word_length,anagram_count,words
    3,3,ATE,EAT,TEA
    3,2,BAT,TAB
    4,2,RATE,TEAR
"""


from collections import defaultdict


source_file = 'word_list_moby_crossword.flat.txt'
output_suffix = '.anagram.csv'
output_file = 'anagrams_words.csv'


def main():
    words = read(source_file)
    table = to_table(words)
    open(source_file + output_suffix, 'wb').write(to_text(table))
    open(output_file, 'wb').write(to_first_word_text(table))


def to_first_word_text(table):
    """
    >>> table = [('length', 'words'), 
    ...     [3, 'ATE', 'EAT'], 
    ...     [4, 'RATE', 'TEAR']]
    >>> print(to_first_word_text(table))
    ATE
    RATE
    """
    column = table[0].index('words')
    rows = [row[column] for row in table[1:]]
    text = '\n'.join(rows)
    return text

    
def to_table(words, anagram_count_min = 3, word_length_min = 3):
    length_anagrams = make_anagrams(words)
    total = len(length_anagrams)
    table = []
    for word_length in range(word_length_min, word_length_min + total):
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


def read(source_file):
    words = open(source_file).read().strip().split()
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


if '__main__' == __name__:
    main()
    import doctest
    doctest.testmod()
