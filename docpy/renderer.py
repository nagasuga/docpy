import os

from jinja2 import Environment, FileSystemLoader


def render(docstring_datas, template_path, func_template, class_template):
    tmpl_split = template_path.split('/')
    tmpl_dir = os.path.join(*tmpl_split[:-1])
    env = Environment(loader=FileSystemLoader(tmpl_dir))
    tmpl = env.get_template(tmpl_split[-1])

    func_htmls = []
    for docstring_data in docstring_datas:
        func_htmls.append(render_docstring(docstring_data, func_template))
    return tmpl.render(funcs=func_htmls)


def render_docstring(docstring_data, template_path):
    """Uses the docstring_data (list) generated from the parser to render
    html (string) of the given function/class."""

    tmpl_split = template_path.split('/')
    tmpl_dir = os.path.join(*tmpl_split[:-1])
    env = Environment(loader=FileSystemLoader(tmpl_dir))
    tmpl = env.get_template(tmpl_split[-1])

    for param in docstring_data['params']:
        if param['name'] in docstring_data['extra'].get('args', {}):
            param['extra'] = docstring_data['extra']['args'][param['name']]
            del docstring_data['extra']['args'][param['name']]

    docstring_data['description'] = docstring_data['description'].replace('\n', '<br />')
    return tmpl.render(func=docstring_data)
