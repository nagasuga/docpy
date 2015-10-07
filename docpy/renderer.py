import inspect
import os

from jinja2 import Environment, FileSystemLoader

from . import parser


def import_file(file_path):
    if file_path.endswith('.py'):
        file_path = file_path[:-3]
    path = '.'.join(file_path.split('/'))
    return __import__(path, fromlist=['*'])


class RenderEngine(object):
    """Render engine to convert python to documentation."""

    def __init__(self, template_path=None):
        self._template = None
        self.template = template_path if template_path else None

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, template_path):
        tmpl_split = template_path.split('/')
        template_dir = os.path.join(*tmpl_split[:-1])
        template_file = tmpl_split[-1]
        env = Environment(loader=FileSystemLoader(template_dir))
        self._template = env.get_template(template_file)

    def render_docstring(self, docstring_data):
        """Uses the docstring_data (list) generated from the parser to render
        html (string) of the given function/class."""

        for param in docstring_data['params']:
            if param['name'] in docstring_data['extra'].get('args', {}):
                param['extra'] = docstring_data['extra']['args'][param['name']]
                del docstring_data['extra']['args'][param['name']]

        docstring_data['description'] = docstring_data['description']\
            .replace('\n', '<br />')
        return self.render(context={'func': docstring_data})

    def render_file(self, file_path):
        """Renders html (string) of the given file with all the def/class
        contained."""

        module = import_file(file_path)
        funcs = [x[1] for x in inspect.getmembers(module) \
            if inspect.isfunction(x[1]) or inspect.isclass(x[1])]
        return [self.render_docstring(parser.parse(func)) for func in funcs]

    def render(self, context):
        """Render the template to html (string) passing context (dict) to
        the template."""
        return self.template.render(**context)
