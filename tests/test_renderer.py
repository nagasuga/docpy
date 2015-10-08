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
    def test_render_docstring(self):
        renderer = docpy.renderer.RenderEngine('templates')
        res = renderer.render_docstring(docpy.parser.parse(func_with_yaml))
        self.assertIsInstance(res, str)

    def test_render_file(self):
        renderer = docpy.renderer.RenderEngine('templates')
        res = renderer.render_file('tests/samples.py')
        self.assertIsInstance(res, str)
