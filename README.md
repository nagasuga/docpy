[![Build Status](https://travis-ci.org/nagasuga/docpy.png?branch=master)](https://travis-ci.org/nagasuga/docpy)
[![Coverage Status](https://coveralls.io/repos/nagasuga/docpy/badge.png?branch=master&service=github)](https://coveralls.io/github/nagasuga/docpy?branch=master)


# docpy

Python documentation generator using docstrings


# Renderer

Allows the user to render a single function/class/file and returns a html documentation using a given template.

## Usage

1. Import

    import some_function
    import docpy.renderer

2. Render a function

    template_path = 'tests/templates/func.html'
    renderer = docpy.renderer.RenderEngine(template_path)
    res = renderer.render_docstring(docpy.parser.parse(some_function))

2. Render a file

    template_path = 'tests/templates/func.html'
    renderer = docpy.renderer.RenderEngine(template_path)
    res = renderer.render_file('tests/samples.py')
    renderer.template = 'tests/templates/index.html'
    res = renderer.render(context={'funcs': res})
    print(res)


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
    import docpy.parser
    data = docpy.parser.parse(sample)
    ```

3. Result

    ```
    {
        'description': 'This is the detail information about this function. Th...",
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
            {
                'name': 'arg1',
                'type': 'arg'
            },
            {
                'name': 'arg2',
                'type': 'arg'
            },
            {
                'default': 'one',
                'name': 'kwargs1',
                'type': 'kwarg'
            },
            {
                'default': None,
                'name': 'kwargs2',
                'type': 'kwarg'
            }
        ],
        'raw': {
            'docstring': 'This is sample docstring that is long that will go ...",
        },
        'summary': 'This is sample docstring that is long that will go multiline and continues here and ... on and on.'

    }
    ```


# TODO

* renderer.render_file should return html, not a list of docs
* rather than taking individual template paths, allow to set template dir which contains the "<object type>.html" to select the template dynamically
