from unittest import TestCase

import docpy.parser


def sample(arg1, arg2, kwargs1='one', kwargs2=None):
    """This is sample docstring.

    This is the detail information about this function. This could be
    pretty long and span multiline/multi paragraph.

    Continuing the detail information about this function. Combine with
    the above paragraph for full explanation of what this function is.
    """
    pass


def sample_2(arg1, arg2, kwargs1='one', kwargs2=None):
    """This is sample docstring that is long that will go multiline
    and continues here and ... on and on.

    This is the detail information about this function. This could be
    pretty long and span multiline/multi paragraph.

    Continuing the detail information about this function. Combine with
    the above paragraph for full explanation of what this function is.
    """
    pass


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
    def test_no_docstring(self):
        docstring = ''
        res = docpy.parser.parse_docstring(docstring=docstring)
        self.assertEqual(res['summary'], None)
        self.assertEqual(res['description'], None)

    def test_simple_summary(self):
        summary = 'This is simple docstring.'
        docstring = """%s""" % summary
        res = docpy.parser.parse_docstring(docstring=docstring)
        self.assertEqual(res['summary'], summary)
        self.assertEqual(res['description'], None)

    def test_multiline_summary(self):
        docstring = """This is sample docstring that is long that will go 
                    multiline and continues here and ... on and on.
                    """
        res = docpy.parser.parse_docstring(docstring=docstring)
        exp_summary = ('This is sample docstring that is long that will go '
                       'multiline and continues here and ... on and on.')
        self.assertEqual(res['summary'], exp_summary)
        self.assertEqual(res['description'], None)

    def test_simple_summary_simple_description(self):
        summary = 'This is simple docstring.'
        description = 'This is simple description.'
        docstring = """%s

                    %s""" % (summary, description)
        res = docpy.parser.parse_docstring(docstring=docstring)
        self.assertEqual(res['summary'], summary)
        self.assertEqual(res['description'], description)

    def test_simple_summary_multiline_description(self):
        summary = 'This is simple docstring.'
        description = """This is simple description. This description will
                      span over multiple lines."""
        docstring = """%s

                    %s""" % (summary, description)
        res = docpy.parser.parse_docstring(docstring=docstring)
        self.assertEqual(res['summary'], summary)
        exp_desc = ('This is simple description. This description will span '
                    'over multiple lines.')
        self.assertEqual(res['description'], exp_desc)

    def test_simple_summary_multiparagraph_description(self):
        summary = 'This is simple docstring.'
        description = """This is simple description. This description will
                      span over multiple lines.

                      Also, this description will have multiple paragraphs
                      to make things a bit more interesting...
                      """
        docstring = """%s

                    %s""" % (summary, description)
        res = docpy.parser.parse_docstring(docstring=docstring)
        self.assertEqual(res['summary'], summary)
        exp_desc = ('This is simple description. This description will span '
                    'over multiple lines.\n\nAlso, this description will have '
                    'multiple paragraphs to make things a bit more '
                    'interesting...')
        self.assertEqual(res['description'], exp_desc)

    def test_multiline_summary_multiparagraph_description(self):
        summary = """This is sample docstring that is long that will go 
                  multiline and continues here and ... on and on.
                  """
        description = """This is simple description. This description will
                      span over multiple lines.

                      Also, this description will have multiple paragraphs
                      to make things a bit more interesting...
                      """
        docstring = """%s

                    %s""" % (summary, description)
        res = docpy.parser.parse_docstring(docstring=docstring)
        exp_summary = ('This is sample docstring that is long that will go '
                       'multiline and continues here and ... on and on.')
        self.assertEqual(res['summary'], exp_summary)
        exp_desc = ('This is simple description. This description will span '
                    'over multiple lines.\n\nAlso, this description will have '
                    'multiple paragraphs to make things a bit more '
                    'interesting...')
        self.assertEqual(res['description'], exp_desc)
