from unittest import TestCase

import docpy.parser
from .samples import sample


class ParseTest(TestCase):
    def test_simple(self):
        res = docpy.parser.parse(sample)
        self.assertEqual(res['name'], 'sample')
        self.assertEqual(res['summary'], 'This is sample docstring.')
        exp_desc = ('This is the detail information about this function. '
                    'This could be pretty long and span multiline/multi '
                    'paragraph.\n\nContinuing the detail information about '
                    'this function. Combine with the above paragraph for '
                    'full explanation of what this function is.')
        self.assertEqual(res['description'], exp_desc)
        exp_params = [{'type': 'arg', 'name': 'arg1'},
                      {'type': 'arg', 'name': 'arg2'},
                      {'default': 'one', 'type': 'kwarg', 'name': 'kwargs1'},
                      {'default': None, 'type': 'kwarg', 'name': 'kwargs2'}]
        self.assertEqual(res['params'], exp_params)


class ParseDocstringTest(TestCase):
    @staticmethod
    def generate_docstring(summary=None, description=None):
        docstring = ''
        if summary:
            docstring = """{}""".format(summary)
        if description:
            docstring += '\n\n{}'.format(description)
        return docstring

    def assert_parse(self, docstring, summary, description):
        res = docpy.parser.parse_docstring(docstring=docstring)
        self.assertEqual(res['summary'], summary)
        self.assertEqual(res['description'], description)

    def test_no_docstring(self):
        docstring = self.generate_docstring()
        self.assert_parse(docstring, summary=None, description=None)

    def test_simple_summary(self):
        summary = 'This is simple docstring.'
        docstring = self.generate_docstring(summary=summary)
        self.assert_parse(docstring, summary=summary, description=None)

    def test_multiline_summary(self):
        summary = """This is sample docstring that is long that will go 
                    multiline and continues here and ... on and on.
                    """
        docstring = self.generate_docstring(summary=summary)
        exp_summary = ('This is sample docstring that is long that will go '
                       'multiline and continues here and ... on and on.')
        self.assert_parse(docstring, summary=exp_summary, description=None)

    def test_simple_summary_simple_description(self):
        summary = 'This is simple docstring.'
        description = 'This is simple description.'
        docstring = self.generate_docstring(summary=summary,
                                            description=description)
        self.assert_parse(docstring, summary=summary, description=description)

    def test_simple_summary_multiline_description(self):
        summary = 'This is simple docstring.'
        description = """This is simple description. This description will
                      span over multiple lines."""
        docstring = self.generate_docstring(summary=summary,
                                            description=description)
        exp_desc = ('This is simple description. This description will span '
                    'over multiple lines.')
        self.assert_parse(docstring, summary=summary, description=exp_desc)

    def test_simple_summary_multiparagraph_description(self):
        summary = 'This is simple docstring.'
        description = """This is simple description. This description will
                      span over multiple lines.

                      Also, this description will have multiple paragraphs
                      to make things a bit more interesting...
                      """
        docstring = self.generate_docstring(summary=summary,
                                            description=description)
        exp_desc = ('This is simple description. This description will span '
                    'over multiple lines.\n\nAlso, this description will have '
                    'multiple paragraphs to make things a bit more '
                    'interesting...')
        self.assert_parse(docstring, summary=summary, description=exp_desc)

    def test_multiline_summary_multiparagraph_description(self):
        summary = """This is sample docstring that is long that will go 
                  multiline and continues here and ... on and on.
                  """
        description = """This is simple description. This description will
                      span over multiple lines.

                      Also, this description will have multiple paragraphs
                      to make things a bit more interesting...
                      """
        docstring = self.generate_docstring(summary=summary,
                                            description=description)
        exp_summary = ('This is sample docstring that is long that will go '
                       'multiline and continues here and ... on and on.')
        exp_desc = ('This is simple description. This description will span '
                    'over multiple lines.\n\nAlso, this description will have '
                    'multiple paragraphs to make things a bit more '
                    'interesting...')
        self.assert_parse(docstring, summary=exp_summary, description=exp_desc)
