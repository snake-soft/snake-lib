""" functions for django forms """


def field_queryset_exclude(field, exclude_object):
    """ removes an element of a field queryset
    :param field: form field to remove object
    :param exclude_object: object to remove or pk
    :returns: QuerySet(field.queryset without exclude)
    """
    if not isinstance(exclude_object, int):
        exclude_object = exclude_object.pk
    queryset = field.queryset.exclude(pk=exclude_object)
    field.queryset = queryset
    return queryset
