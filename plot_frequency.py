"""
See plot_frequency.md
"""


from pandas import read_csv


def plot(word_text_path):
    frame = read_csv(word_text_path, delim_whitespace=True)
    plot = frame.plot(kind='line', loglog=True)
    png_path = save(plot, '%s.loglog' % word_text_path)
    print('Plotted to %r' % png_path)
    fraction = 1.0 / 2.0 ** 10
    xmax = int(round(len(frame) * fraction))
    xlim = (0, xmax)
    plot = frame.plot(kind='line',
        xlim = xlim)
    png_path = save(plot, '%s.xlim_%s' % (
        word_text_path, xmax))
    print('Plotted to %r' % png_path)
    return png_path


def save(plot, base_path):
    figure = plot.get_figure()
    png_path = '%s.png' % base_path
    figure.savefig(png_path)
    return png_path


def plots(text_paths):
    for text_path in text_paths:
        png_path = plot(text_path)


if '__main__' == __name__:
    from sys import argv
    if 2 <= len(argv):
        text_paths = argv[1:]
    else:
        text_paths = ['en.txt', 'count_1w.txt']
    plots(text_paths)
