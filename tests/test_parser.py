from datetime import date
from unittest import TestCase

import yaml

import docpy.parser
from .samples import sample, func_with_yaml, func_with_yaml_2


class ParseTest(TestCase):
    def test_simple(self):
        res = docpy.parser.parse(sample)
        self.assertEqual(res['name'], 'sample')
        exp_summary = ('This is sample docstring that is long that will go '
                       'multiline and continues here and ... on and on.')
        self.assertEqual(res['summary'], exp_summary)
        exp_desc = ('This is the detail information about this function. '
                    'This could be pretty long and span multiline/multi '
                    'paragraph.\n\nContinuing the detail information about '
                    'this function. Combine with the above paragraph for '
                    'full explanation of what this function is.')
        self.assertEqual(res['description'], exp_desc)
        exp_params = [{'_type': 'arg', '_name': 'arg1'},
                      {'_type': 'arg', '_name': 'arg2'},
                      {'_default': 'one', '_type': 'kwarg', '_name': 'kwargs1'},
                      {'_default': None, '_type': 'kwarg', '_name': 'kwargs2'}]
        self.assertEqual(res['params'], exp_params)

    def test_yaml(self):
        res = docpy.parser.parse(func_with_yaml)
        self.assertEqual(res['name'], 'func_with_yaml')
        exp_summary = ('This is sample docstring that is long that will go '
                       'multiline and continues here and ... on and on.')
        self.assertEqual(res['summary'], exp_summary)
        exp_desc = ('This is the detail information about this function. '
                    'This could be pretty long and span multiline/multi '
                    'paragraph.\n\nContinuing the detail information about '
                    'this function. Combine with the above paragraph for '
                    'full explanation of what this function is.')
        self.assertEqual(res['description'], exp_desc)
        exp_params = [{'_type': 'arg', '_name': 'arg1'},
                      {'_type': 'arg', '_name': 'arg2'},
                      {'_default': 'one', '_type': 'kwarg', '_name': 'kwargs1'},
                      {'_default': None, '_type': 'kwarg', '_name': 'kwargs2'}]
        self.assertEqual(res['params'], exp_params)
        exp_extra = {
            'date': date(2015, 10, 10),
            'user': {
                'first': 'Jeff',
                'last': 'Nagasuga',
            },
            'id': 12345,
            'args': {
                'arg1': {
                    'type': 'int',
                    'description': 'test argument (first).',
                },
                'arg2': {
                    'type': 'string',
                    'description': 'test argument (second).',
                },
                'kwargs2': {
                    'type': 'list',
                    'description': 'list of testing things.',
                },
            },
        }
        self.assertEqual(res['extra'], exp_extra)


class ParseDocstringTest(TestCase):
    @staticmethod
    def generate_docstring(summary=None, description=None, raw_yaml=None):
        docstring = ''
        if summary:
            docstring = """{}""".format(summary)
        if description:
            if docstring:
                docstring += '\n\n'
            docstring += '{}'.format(description)
        if raw_yaml:
            if docstring:
                docstring += '\n\n'
            docstring += '{}'.format(raw_yaml)
        return docstring

    def assert_parse(self, docstring, summary, description, yaml=None):
        res = docpy.parser.parse_docstring(docstring=docstring)
        self.assertEqual(res['summary'], summary)
        self.assertEqual(res['description'], description)
        if yaml is None:
            yaml = {}
        self.assertEqual(res['yaml'], yaml)

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

    def test_only_yaml(self):
        raw_yaml = """---
                      args:
                          arg1:
                              type: int
                              description: test argument (first).
                          arg2:
                              type: string
                              description: test argument (second).
                          kwarg2:
                              type: list
                              description: list of testing things.
                      date: 2015-10-10
                      user:
                          first: Jeff
                          last: Nagasuga
                      id: 12345
                   """
        docstring = self.generate_docstring(raw_yaml=raw_yaml)
        exp_yaml = yaml.load(raw_yaml, Loader=yaml.Loader)
        self.assert_parse(docstring, summary=None, description=None, yaml=exp_yaml)

    def test_simple_summary_with_yaml(self):
        summary = 'This is simple docstring.'
        raw_yaml = """---
                      args:
                          arg1:
                              type: int
                              description: test argument (first).
                          arg2:
                              type: string
                              description: test argument (second).
                          kwarg2:
                              type: list
                              description: list of testing things.
                      date: 2015-10-10
                      user:
                          first: Jeff
                          last: Nagasuga
                      id: 12345
                   """
        docstring = self.generate_docstring(summary=summary, raw_yaml=raw_yaml)
        exp_yaml = yaml.load(raw_yaml, Loader=yaml.Loader)
        self.assert_parse(docstring, summary=summary, description=None,
                          yaml=exp_yaml)

    def test_simple_summary_simple_description_with_yaml(self):
        summary = 'This is simple docstring.'
        description = 'This is simple description.'
        raw_yaml = """---
                      args:
                          arg1:
                              type: int
                              description: test argument (first).
                          arg2:
                              type: string
                              description: test argument (second).
                          kwarg2:
                              type: list
                              description: list of testing things.
                      date: 2015-10-10
                      user:
                          first: Jeff
                          last: Nagasuga
                      id: 12345
                   """
        docstring = self.generate_docstring(summary=summary,
                                            description=description,
                                            raw_yaml=raw_yaml)
        exp_yaml = yaml.load(raw_yaml, Loader=yaml.Loader)
        self.assert_parse(docstring, summary=summary, description=description,
                          yaml=exp_yaml)

    def test_simple_summary_multiparagraph_description_with_yaml(self):
        summary = 'This is simple docstring.'
        description = """This is simple description. This description will
                      span over multiple lines.

                      Also, this description will have multiple paragraphs
                      to make things a bit more interesting...
                      """
        raw_yaml = """---
                      args:
                          arg1:
                              type: int
                              description: test argument (first).
                          arg2:
                              type: string
                              description: test argument (second).
                          kwarg2:
                              type: list
                              description: list of testing things.
                      date: 2015-10-10
                      user:
                          first: Jeff
                          last: Nagasuga
                      id: 12345
                   """
        docstring = self.generate_docstring(summary=summary,
                                            description=description,
                                            raw_yaml=raw_yaml)
        exp_desc = ('This is simple description. This description will span '
                    'over multiple lines.\n\nAlso, this description will have '
                    'multiple paragraphs to make things a bit more '
                    'interesting...')
        exp_yaml = yaml.load(raw_yaml, Loader=yaml.Loader)
        self.assert_parse(docstring, summary=summary, description=exp_desc,
                          yaml=exp_yaml)
