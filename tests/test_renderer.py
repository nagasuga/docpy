import inspect
from unittest import TestCase, skip

import docpy.parser
import docpy.renderer
from .samples import (
    sample, func_with_yaml, func_with_yaml_2, func_without_docstring)


class ImportFileTest(TestCase):
    def test_non_existing_file(self):
        self.assertRaises(ImportError, docpy.renderer.import_file,
                          file_path='docpy/xxxx.py')

    def test_existing_file(self):
        res = docpy.renderer.import_file('tests/samples.py')
        self.assertTrue(inspect.ismodule(res))
        self.assertEqual(
            set([x[0] for x in inspect.getmembers(res) \
                if inspect.isfunction(x[1]) or inspect.isclass(x[1])]),
            set(['func_with_yaml', 'func_with_yaml_2',
                 'func_without_docstring', 'sample', 'SimpleClass',
                 'ClassWithInit']))


class RenderEngineTest(TestCase):
    @skip('WIP')
    def test_render_docstring(self):
        from jinja2.compiler import find_undeclared, Frame
        renderer = docpy.renderer.RenderEngine('tests/templates/func.html')
        res = renderer.render_docstring(docpy.parser.parse(func_with_yaml))

    @skip('WIP')
    def test_render_file(self):
        renderer = docpy.renderer.RenderEngine('tests/templates/func.html')
        res = renderer.render_file('tests/samples.py')
        print(res)

        renderer.template = 'tests/templates/index.html'
        res = renderer.render(context={'funcs': res})
        f_obj = open('xxx.html', 'w')
        f_obj.write(res)
        f_obj.close()
