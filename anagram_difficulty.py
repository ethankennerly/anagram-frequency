"""
Tabulate length and frequency
See README.md
"""


from pandas import read_csv
from os.path import splitext


word_column = 'word'


def tabulate_file(word_list_path, word_frequency_path):
    list_frame = read_csv(word_list_path)
    list_frame[word_column] = list_frame[word_column].str.lower()
    frequency_frame = read_csv(word_frequency_path,
        delim_whitespace=True,
        header=None,
        names=[word_column, 'frequency'])
    list_frame[word_column + '_length'] = list_frame[word_column].str.len()
    list_frame = list_frame.merge(frequency_frame, on=word_column)
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
