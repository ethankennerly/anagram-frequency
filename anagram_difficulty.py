"""
Tabulate length and frequency
See README.md
"""

from numpy import number
from pandas import read_csv
from scipy.stats import zscore
from os.path import splitext




def tabulate_file(word_list_path, word_frequency_path,
        word_column = 'word',
        frequency_column = 'frequency'):
    score_suffix = '_score'
    list_frame = read_csv(word_list_path)
    list_frame[word_column] = list_frame[word_column].str.lower()
    frequency_frame = read_csv(word_frequency_path,
        delim_whitespace=True,
        header=None,
        names=[word_column, frequency_column])
    length_column = word_column + '_length'
    list_frame[length_column] = list_frame[word_column].str.len()
    list_frame = list_frame.merge(frequency_frame, on=word_column)
    raw_columns = [length_column, frequency_column]
    score_columns = []
    for raw_column in raw_columns:
        score_column = raw_column + score_suffix
        score_columns.append(score_column)
        list_frame[score_column] = zscore(list_frame[raw_column])
    frequency_score = frequency_column + score_suffix
    list_frame[frequency_score] = -list_frame[frequency_score]
    composite_column = '%s_%s%s' % (length_column, frequency_column, score_suffix)
    list_frame[composite_column] = list_frame[score_columns].sum(axis=1)
    list_frame.sort_values(composite_column, inplace=True)
    output_path = splitext(word_list_path)[0] + '.difficulty.csv'
    list_frame.to_csv(output_path, index = False)
    return output_path


if '__main__' == __name__:
    from sys import argv
    if 2 <= len(argv):
        text_paths = argv[1:]
        print(tabulate_file(*text_paths))
    else:
        print(__doc__)
    import doctest
    doctest.testfile('README.md')
