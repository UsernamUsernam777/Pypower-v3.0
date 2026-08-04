from . import Iterable as _Iterable
from itertools import zip_longest as zip
def put_before_line(text, string):
    text = text.replace('\n', '\n{}')
    return text.format(text, *string*text.count('\n'))
def super_join(text, sep, after_how_many_letters):
    """Insert sep every after_how_many_letters characters in the string."""
    value = 0
    new = ''
    ran = range(after_how_many_letters, len(text)-1, after_how_many_letters)
    for i in text:
        new += i
        value += 1
        if value in ran:
            new += sep
    return new
def replace_many(text, old_iterable, new_iterable):
    """Replace each character in old_iterable with the matching one in new_iterable."""
    for i, e in zip(old_iterable, new_iterable, fillvalue=''):
        text = text.replace(i, e)
    return text
def between(text, c1, c2, first=True, last=True):
    """return string between two points"""
    result = []
    index = [_Iterable.indexes(text, c1), _Iterable.indexes(text, c2)]
    for i, e in zip(index[0], index[1]):
        if not first:
            i += 1
        if last:
            e += 1
        result.append(text[i:e])
    return result
def line_if_in(text, string):
    return [t for t in text.splitlines() if string in t]
