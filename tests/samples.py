def sample(arg1, arg2, kwargs1='one', kwargs2=None):
    """This is sample docstring that is long that will go multiline
    and continues here and ... on and on.

    This is the detail information about this function. This could be
    pretty long and span multiline/multi paragraph.

    Continuing the detail information about this function. Combine with
    the above paragraph for full explanation of what this function is.
    """
    pass


def func_with_yaml(arg1, arg2, kwargs1='one', kwargs2=None):
    """This is sample docstring that is long that will go multiline
    and continues here and ... on and on.

    This is the detail information about this function. This could be
    pretty long and span multiline/multi paragraph.

    Continuing the detail information about this function. Combine with
    the above paragraph for full explanation of what this function is.

    ---
    args:
        arg1:
            type: int
            description: test argument (first).
        arg2:
            type: string
            description: test argument (second).
        kwargs2:
            type: list
            description: list of testing things.
    date: 2015-10-10
    user:
        first: Jeff
        last: Nagasuga
    id: 12345
    """
    pass


def func_with_yaml_2(arg1, arg2, kwargs1='one', kwargs2=None):
    """This is sample docstring that is long that will go multiline
    and continues here and ... on and on.

    This is the detail information about this function. This could be
    pretty long and span multiline/multi paragraph.

    Continuing the detail information about this function. Combine with
    the above paragraph for full explanation of what this function is.

    ---
    args:
        arg1:
            type: int
            description: test argument (first).
        arg2:
            type: string
            description: test argument (second).
        kwargs2:
            type: list
            description: list of testing things.
        unknown_arg:  # unknown arg will be ignored
            type: list
            description: list of testing things.
    date: 2015-10-10
    user:
        first: Jeff
        last: Nagasuga
    id: 12345
    """
    pass


def func_without_docstring(arg1, arg2, kwargs1='one', kwargs2=None):
    pass


class SimpleClass(object):
    """Docstring for this class."""
    pass
