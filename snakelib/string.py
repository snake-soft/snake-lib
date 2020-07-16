import string as string_class

def remove_bad_chars(string, bad_chars_string, case_sensitive=True):
    """
    :param string: string to remove chars
    :param bad_chars_string: chars to remove
    :returns: string - bad chars
    """
    if case_sensitive:
        remove = {ord(i):None for i in bad_chars_string}
    else:
        upper = {ord(i):None for i in bad_chars_string.upper()}
        lower = {ord(i):None for i in bad_chars_string.lower()}
        remove = {**upper, **lower}
    return string.translate(remove)
