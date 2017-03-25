"""
Plot first and second column.
"""


from pandas import read_csv


def plot(word_text_path):
    frame = read_csv(word_text_path, delim_whitespace=True)
    plot = frame.plot(kind='line', loglog=True)
    figure = plot.get_figure()
    png_path = '%s.png' % word_text_path
    figure.savefig(png_path)
    return png_path


def plots(text_paths):
    for text_path in text_paths:
        png_path = plot(text_path)
        print('Plotted to %r' % png_path)


if '__main__' == __name__:
    from sys import argv
    if 2 <= len(argv):
        text_paths = argv[1:]
    else:
        text_paths = ['en.txt', 'count_1w.txt']
    plots(text_paths)
