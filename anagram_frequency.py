from collections import defaultdict
from os import path
from csv import reader


source_file = 'TWL06.txt'
output_suffix = '.anagram.csv'
output_file = 'anagram_words.txt'
excludes_file = 'excludes.txt'
frequency_files = ['count_1w.txt', 'en.txt']


def main():
    """
    If table does not exist, generate from frequencies.
    Sort by weights.
    """
    table_file = source_file + output_suffix
    if not path.exists(table_file):
        words = read_first_words(source_file)
        table = to_table(words)
        frequencies_list = [
            read_first_words(frequency_file)
            for frequency_file in frequency_files
        ]
        table = sort_short_and_frequent(table, frequencies_list)
        open(table_file, 'wb').write(to_text(table))
    else:
        table = read_csv(table_file)
        table = sort_weight(table)
        open(table_file, 'wb').write(to_text(table))
    excludes = read_first_words(excludes_file)
    output = to_first_word_text(table, excludes)
    open(output_file, 'wb').write(output)


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


def to_first_word_text(table, excludes = []):
    column = -1
    for index, fieldname in enumerate(table[0]):
        if fieldname.startswith('words'):
            column = index
            break
    rows = []
    for row in table[1:]:
        for item in row:
            if isinstance(item, str) and item not in excludes:
                rows.append(item)
                break
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
    """
    Converts words to upper case.
    """
    lines = open(source_file).read().strip().splitlines()
    words = [line.split()[0].upper() for line in lines]
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


def sort_short_and_frequent(table, frequencies_list):
    """
    Minimum frequency percentile from frequency lists.
    """
    frequency_counts = [len(frequencies) 
        for frequencies in frequencies_list]
    sorted_table = []
    for row in table[1:]:
        frequency_row = list(row[:2])
        frequency = []
        for word in row[2:]:
            percentile = 200
            for frequency_count, frequencies in \
            zip(frequency_counts, frequencies_list):
                if word in frequencies:
                    index = frequencies.index(word)
                    frequency_percentile = int(round(100 * float(
                        frequency_count - index) / frequency_count))
                    percentile = min(percentile, frequency_percentile)
            if 200 == percentile:
                percentile = 0
            frequency.append((-percentile, word))
        frequency.sort()
        for percentile, word in frequency:
            frequency_row.append(word)
            frequency_row.append(-percentile)
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
    """
    Sum a power of frequency.
    Word frequencies have a skew with a long tail toward infrequent.
    """
    weight = 500 * entry[0] ** 0.25
    for i in range(3, len(entry), 2):
        weight -= (entry[i] / 100.0) ** 4 * 100
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
    doctest.testfile('README.md')
