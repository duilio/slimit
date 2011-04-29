###############################################################################
#
# Copyright (c) 2011 Ruslan Spivak
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

__author__ = 'Ruslan Spivak <ruslan.spivak@gmail.com>'

import unittest
import difflib
import pprint

from slimit.lexer import Lexer


# The structure and some test cases are taken
# from https://bitbucket.org/ned/jslex
class LexerTestCase(unittest.TestCase):

    def _get_lexer(self):
        lexer = Lexer()
        lexer.build()
        return lexer

    def assertListEqual(self, first, second):
        """Assert that two lists are equal.

        Prints differences on error.
        This method is similar to that of Python 2.7 'assertListEqual'
        """
        if first != second:
            message = '\n'.join(
                difflib.ndiff(pprint.pformat(first).splitlines(),
                              pprint.pformat(second).splitlines())
                )
            self.fail('Lists differ:\n' + message)

    TEST_CASES = [
        # Identifiers
        ('i my_variable_name c17 _dummy $str $ _ CamelCase',
         ['ID i', 'ID my_variable_name', 'ID c17',
          'ID _dummy', 'ID $str', 'ID $', 'ID _', 'ID CamelCase']
         ),
        (ur'\u03c0 \u03c0_tail var\ua67c',
         [ur'ID \u03c0', ur'ID \u03c0_tail', ur'ID var\ua67c']),
        ]


def make_test_function(input, expected):

    def test_func(self):
        lexer = self._get_lexer()
        lexer.input(input)
        result = ['%s %s' % (token.type, token.value) for token in lexer]
        self.assertListEqual(result, expected)

    return test_func

for index, (input, expected) in enumerate(LexerTestCase.TEST_CASES):
    func = make_test_function(input, expected)
    setattr(LexerTestCase, 'test_case_%d' % index, func)
