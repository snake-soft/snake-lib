
def intersection(lst1, lst2):
    """ method to calculate intersection between two lists
    :param lst1: first list to user
    :param lst2: second list to user
    :yields: intersecting list elements
    """
    for element in lst1:
        if element in lst2:
            yield element
