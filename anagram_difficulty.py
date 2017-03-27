"""
Tabulate length and frequency
See README.md
"""


from math import factorial
from numpy import log
from os.path import splitext
from pandas import read_csv
from scipy.stats import zscore


# Was 0.875; 0.75; 0.5
length_weight = 0.75
frequency_weight = 1.0 - length_weight
word_length_max = 10

word_column = 'word'
frequency_column = 'frequency'
score_suffix = '_score'
length_column = word_column + '_length'
permutation_column = word_column + '_permutation'
frequency_score = frequency_column + score_suffix
permutation_score = permutation_column + score_suffix
length_score = length_column + score_suffix
raw_columns = [length_column, frequency_column]
composite_column = '_'.join(raw_columns) + score_suffix


def tabulate_file(word_list_path, word_frequency_path):
    list_frame = read_csv(word_list_path)
    list_frame[word_column] = list_frame[word_column].str.lower()
    frequency_frame = read_csv(word_frequency_path,
        delim_whitespace=True,
        header=None,
        names=[word_column, frequency_column])
    score_frame(frequency_frame)
    list_frame = list_frame.merge(frequency_frame, on=word_column)
    list_frame.sort_values(composite_column, inplace=True)
    list_frame = list_frame.round(3)
    output_path = splitext(word_list_path)[0] + '.difficulty.csv'
    list_frame.to_csv(output_path, index = False)
    return output_path


def score_frame(list_frame):
    list_frame.dropna(inplace=True)
    list_frame[length_column] = list_frame[word_column].str.len().astype(int)
    too_long = list_frame[list_frame[length_column] > word_length_max]
    if len(too_long):
        print('Dropping %r words longer than %r\n%r\n...\n%r' % (
            len(too_long), word_length_max,
            too_long.head(), too_long.tail()))
    list_frame.drop(too_long.index, inplace=True)
    list_frame[permutation_column] = list_frame[length_column].apply(factorial)
    score_columns = []
    for raw_column in raw_columns:
        score_column = raw_column + score_suffix
        score_columns.append(score_column)
        list_frame[score_column] = zscore(log(list_frame[raw_column]))
    list_frame[frequency_score] = -list_frame[frequency_score]
    list_frame[composite_column] = list_frame[length_score] * length_weight \
        + list_frame[frequency_score] * frequency_weight


if '__main__' == __name__:
    from sys import argv
    if 2 <= len(argv):
        text_paths = argv[1:]
        print(tabulate_file(*text_paths))
    else:
        print(__doc__)
    import doctest
    doctest.testfile('README.md')
