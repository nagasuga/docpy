from unittest import TestCase, skip

import docpy.parser
import docpy.renderer
from .samples import (
    sample, func_with_yaml, func_with_yaml_2, func_without_docstring)


class RenderTest(TestCase):
    @skip('WIP')
    def test_pass(self):
        doc_data = docpy.parser.parse(func_with_yaml)
        res = docpy.renderer.render_docstring(doc_data, template_path='tests/templates/func.html')
        with open('xxx.html', 'w') as f_obj:
            f_obj.write(res)

        #print()
        #print(res)

    def test_render(self):
        from jinja2.compiler import find_undeclared, Frame
        res = docpy.renderer.render(docstring_datas=[docpy.parser.parse(sample),
                                                     docpy.parser.parse(find_undeclared),
                                                     docpy.parser.parse(Frame),
                                                     docpy.parser.parse(func_with_yaml)],
                                    template_path='tests/templates/index.html',
                                    func_template='tests/templates/func.html',
                                    class_template='tests/templates/func.html')
        with open('xxx.html', 'w') as f_obj:
            f_obj.write(res)
