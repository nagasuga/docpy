[![Build Status](https://travis-ci.org/nagasuga/docpy.png?branch=master)](https://travis-ci.org/nagasuga/docpy)


# docpy

Python documentation generator using docstrings


# Parser

1. Have a sample function with docstring to parse the information for documentation.

```
def sample(arg1, arg2, kwargs1='one', kwargs2=None):
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
```

2. Use docpy parser to extract information

```
import pprint
import docpy.parser
pprint.pprint(docpy.parser.parse(sample))
```

3. Result

```
{
    'description': 'This is the detail information about this function. ...',
    'extra': {
        'args': {
            'arg1': {
                'description': 'test argument (first).',
                'type': 'int'
            },
            'arg2': {
                'description': 'test argument (second).',
                'type': 'string'
            },
            'kwargs2': {
                'description': 'list of testing things.',
                'type': 'list'
            }
        },
        'date': datetime.date(2015, 10, 10),
        'id': 12345,
        'user': {
            'first': 'Jeff',
            'last': 'Nagasuga'
        }
    },
    'name': 'sample',
    'params': [
        {'_name': 'arg1', '_type': 'arg'},
        {'_name': 'arg2', '_type': 'arg'},
        {'_default': 'one', '_name': 'kwargs1', '_type': 'kwarg'},
        {'_default': None, '_name': 'kwargs2', '_type': 'kwarg'}
    ],
    'raw': {
        'docstring': 'This is sample docstring that is long that will ...',
        'summary': 'This is sample docstring that is long that will go multiline and continues here and ... on and on.'
}
```
