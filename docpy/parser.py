import inspect
import re
import sys
import textwrap
import yaml


def parse(obj):
    """Returns parsed docstring in dict."""

    type_name = type(obj).__name__
    obj_type = 'class' if type_name == 'type' else type_name

    result = {
        'raw': {
            'docstring': obj.__doc__,
        },
        'name': obj.__name__,
        'params': parse_parameters(obj),
        'type': obj_type,
    }
    docstring = parse_docstring(docstring=inspect.getdoc(obj))
    result['extra'] = docstring['yaml']
    del docstring['yaml']
    result.update(docstring)
    return result


def parse_docstring(docstring):
    """Parse and return various information from the docstring."""
    result = {
        'summary': '',
        'description': '',
        'yaml': {},
    }

    if not docstring:
        return result

    paragraphs = docstring.split('\n\n')

    description = ''
    desc_paragraphs = []
    found_yaml = False
    count = 0
    for paragraph in paragraphs:
        if re.match(r'^\s*---', paragraph):
            found_yaml = True
            break
        elif count == 0:
            summary = re.sub('[ ]*\n[ ]*', ' ', paragraphs[0]).strip()
            result['summary'] = summary
        else:
            desc = re.sub('[ ]*\n[ ]*', ' ', paragraph).strip()
            desc_paragraphs.append(desc)
        count += 1

    if found_yaml:
        raw_yaml = '\n'.join(paragraphs[count:])
        raw_yaml = ''
        for paragraph in paragraphs[count:]:
            raw_yaml += textwrap.dedent(paragraph) + '\n'
        indent_count = 0
        result['yaml'] = yaml.load(raw_yaml, Loader=yaml.Loader)

    if desc_paragraphs:
        description = '\n\n'.join(desc_paragraphs)
    result['description'] = description
    return result


def parse_parameters_py3(func):
    """Parse and returns a list of dict about the parameters of func."""
    params = []
    for parameter in inspect.signature(func).parameters.values():
        param = {
            'name': parameter.name,
            'type': 'arg' if parameter.default is parameter.empty else 'kwarg',
        }
        if parameter.default != parameter.empty:
            param['default'] = parameter.default
        params.append(param)
    return params


def parse_parameters_py2(obj):
    """Parse and returns a list of dict about the parameters of obj.

    This is for python <= 3.2"""
    params = []
    if inspect.isclass(obj):
        argspec = inspect.getargspec(obj.__init__) \
            if inspect.ismethod(obj.__init__) else None

        if not argspec:
            return params

        args = argspec.args[1:]  # skip "self"
    else:
        argspec = inspect.getargspec(obj)
        args = argspec.args

    kwargs_start_idx = len(args) - len(argspec.defaults or [])
    kwarg_idx = 0
    for idx, arg_name in enumerate(args):
        param = {'name': arg_name}
        if idx < kwargs_start_idx:
            param['type'] = 'arg'
        else:
            param['type'] = 'kwarg'
            param['default'] = argspec.defaults[kwarg_idx]
            kwarg_idx += 1

        params.append(param)
    return params


if sys.version_info < (3, 3):
    parse_parameters = parse_parameters_py2
else:
    parse_parameters = parse_parameters_py3
