import inspect

from jinja2 import Environment, FileSystemLoader

from . import parser


def import_file(file_path):
    if file_path.endswith('.py'):
        file_path = file_path[:-3]
    path = '.'.join(file_path.split('/'))
    return __import__(path, fromlist=['*'])


class RenderEngine(object):
    """Render engine to convert python to documentation."""

    def __init__(self, template_dir):
        self.template_dir = template_dir

    def get_template(self, obj_type):
        env = Environment(loader=FileSystemLoader(self.template_dir))
        return env.get_template('{}.html'.format(obj_type))

    def render_docstring(self, docstring_data):
        """Uses the docstring_data (list) generated from the parser to render
        html (string) of the given function/class."""

        for param in docstring_data['params']:
            if param['name'] in docstring_data['extra'].get('args', {}):
                param['extra'] = docstring_data['extra']['args'][param['name']]
                del docstring_data['extra']['args'][param['name']]

        docstring_data['description'] = docstring_data['description']\
            .replace('\n', '<br />')

        template = self.get_template(obj_type=docstring_data['type'])
        return template.render(obj_data=docstring_data)

    def render_file(self, file_path):
        """Renders html (string) of the given file with all the def/class
        contained."""

        obj_datas = []
        module = import_file(file_path)
        for _, obj in inspect.getmembers(module):
            if inspect.isclass(obj) or inspect.isfunction(obj):
                obj_datas.append(self.render_docstring(parser.parse(obj)))
        template = self.get_template(obj_type=type(module).__name__)
        return template.render(obj_datas=obj_datas)
