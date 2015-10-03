import inspect
import re


def parse(func):
    """Returns parsed docstring in dict."""
    result = {
        'raw': {
            'docstring': func.__doc__,
        },
        'name': func.__name__,
        'params': parse_parameters(func),
    }
    docstring = parse_docstring(docstring=func.__doc__)
    result.update(docstring)
    return result


def parse_parameters(func):
    """Parse and returns a list of dict about the parameters of func."""
    params = []
    argspec = inspect.getargspec(func)
    kwargs_start_idx = len(argspec.args) - len(argspec.defaults)
    kwarg_idx = 0
    for idx, arg_name in enumerate(argspec.args):
        param = {'name': arg_name}
        if idx < kwargs_start_idx:
            param['type'] = 'arg'
        else:
            param['type'] = 'kwarg'
            param['default'] = argspec.defaults[kwarg_idx]
            kwarg_idx += 1

        params.append(param)
    return params


def parse_docstring(docstring):
    """Parse and return various information from the docstring."""
    result = {
        'summary': None,
        'description': None,
    }

    if not docstring:
        return result

    paragraphs = docstring.split('\n\n')
    summary = re.sub('[ ]*\n[ ]*', ' ', paragraphs[0]).strip()
    result['summary'] = summary

    description = None
    desc_paragraphs = []
    for paragraph in paragraphs[1:]:
        desc = re.sub('[ ]*\n[ ]*', ' ', paragraph).strip()
        desc_paragraphs.append(desc)

    if desc_paragraphs:
        description = '\n\n'.join(desc_paragraphs)
    result['description'] = description

    return result
