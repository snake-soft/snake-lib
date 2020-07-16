
def intersection(*iterables):
    """ method to calculate intersection between two lists
    Tested with string, list, set
    If all iterables are of same type (should), it returns items of this type
    :param iterables: any object that can be iterated
    :returns: set of intersecting elements
    """
    types = {type(i) for i in iterables}
    intersected = set.intersection(*[set(iterable) for iterable in iterables])
    if len(types) is 1:  # all of same type
        output_type = types.pop()
        if output_type == str:
            return ''.join(intersected)
        elif output_type in (list, set):
            return output_type(intersected)

    return intersected
