from pandas import read_csv
from os.path import splitext


def tabulate_file(word_list_path, word_frequency_path):
    list_frame = read_csv(word_list_path)
    frequency_frame = read_csv(word_frequency_path, delim_whitespace=True)
    output_path = splitext(word_list_path)[0] + '.difficulty.csv'
    list_frame.to_csv(output_path, index = False)
    return output_path


if '__main__' == __name__:
    from sys import argv
    if 2 <= len(argv):
        text_paths = argv[1:]
    else:
        text_paths = ['sample_word_list.csv', 'en.txt']
    print(tabulate_file(*text_paths))
