""" functions for django forms """


def field_queryset_exclude(field, exclude_object):
    """ removes an element of a field queryset
    :param field: form field to remove object
    :param exclude_object: object to remove
    :returns: QuerySet(field.queryset without exclude)
    """
    queryset = field.queryset.exclude(pk=exclude_object.pk)
    field.queryset = queryset
    return queryset
