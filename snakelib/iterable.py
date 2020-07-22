from collections import defaultdict

def intersection(iterable1, iterable2):
    """ method to calculate intersection between two lists
    Tested with string, list, set
    If all iterables are of same type (should), it returns items of this type
    :param iterable1: any object that can be iterated
    :param iterable2: any object that can be iterated
    :returns: set of intersecting elements
    """
    return {elem for elem in iterable1 if elem in iterable2}
