"""
The MIT License

Copyright (c) 2010 FreshBooks

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import re
from smartytotwig.pyPEG import parse
from smartytotwig.pyPEG import keyword, _and, _not, ignore

OPTIONALLY = 0
ANY_NUMBER_OF = -1
AT_LEAST_ONE = -2

"""
Misc.
"""
def content():              return re.compile(r'[^{]+')

def comment():              return re.compile("{\*.*?\*}", re.S)

def literal():              return re.compile("{literal}.*?{/literal}", re.S)

def junk():                 return ANY_NUMBER_OF, [' ', '\n', '\t']

"""
Logical operators.
"""
def and_operator():         return [keyword('and'), '&&']

def or_operator():          return [keyword('or'), '||']

def equals_operator():      return ['==', keyword('eq')]

def ne_operator():          return ['!=', keyword('ne'), keyword('neq')]

def gt_operator():          return ['>', 'gt']

def lt_operator():          return ['<', 'gt']

def lte_operator():         return ['<=']

def gte_operator():         return ['>=']

def right_paren():          return junk, ')'

def left_paren():           return junk, '('

def operator():             return OPTIONALLY, ' ', [and_operator, equals_operator, gte_operator, lte_operator, lt_operator, gt_operator, ne_operator, or_operator]

"""
Smarty variables.
"""
def string():               return OPTIONALLY, ' ', [(re.compile(r'"'), ANY_NUMBER_OF, [re.compile(r'[^$`"\\]'), re.compile(r'\\.')], re.compile(r'"')), (re.compile(r'\''), ANY_NUMBER_OF, [re.compile(r'[^\'\\]'), re.compile(r'\\.')], re.compile(r'\''))]

def text():                 return AT_LEAST_ONE, [re.compile(r'[^$`"\\]'), re.compile(r'\\.')]

def variable_string():      return '"', AT_LEAST_ONE, [text, ('`', expression, '`'), ('$', expression)], '"'

def dollar():               return '$'

def not_operator():         return '!'

def at_operator():          return '@'

def symbol():               return ANY_NUMBER_OF, [' ', '\n', '\t'], OPTIONALLY, [not_operator, at_operator], OPTIONALLY, dollar, re.compile(r'[\w\-\+]+')

def array():                return symbol, "[", OPTIONALLY, expression, "]"

def modifier():             return [object_dereference, array, symbol, variable_string, string], AT_LEAST_ONE, modifier_right, OPTIONALLY, ' '

def expression():           return [modifier, object_dereference, array, symbol, string, variable_string]

def object_dereference():   return [array, symbol], '.', expression

def exp_no_modifier():      return [object_dereference, array, symbol, variable_string, string]

def modifier_right():       return ('|', symbol, ANY_NUMBER_OF, (':', exp_no_modifier),)

"""
Smarty statements.
"""
def else_statement():       return '{', keyword('else'), '}', ANY_NUMBER_OF, smarty_language

def foreachelse_statement():return '{', keyword('foreachelse'), '}', ANY_NUMBER_OF, smarty_language

def print_statement():      return '{', OPTIONALLY, 'e ', expression, '}'

def function_parameter():   return symbol, '=', expression, junk

def function_statement():   return '{', symbol, AT_LEAST_ONE, function_parameter, '}'

def for_from():             return junk, keyword('from'), '=', OPTIONALLY, ['"', '\''], expression, OPTIONALLY, ['"', '\''], junk

def for_item():             return junk, keyword('item'), '=', OPTIONALLY, ['"', '\''], symbol, OPTIONALLY, ['"', '\''], junk

def for_name():             return junk, keyword('name'), '=', OPTIONALLY, ['"', '\''], symbol, OPTIONALLY, ['"', '\''], junk

def for_key():              return junk, keyword('key'), '=', OPTIONALLY, ['"', '\''], symbol, OPTIONALLY, ['"', '\''], junk

def elseif_statement():     return '{', keyword('elseif'), ANY_NUMBER_OF, left_paren, expression, ANY_NUMBER_OF, right_paren, ANY_NUMBER_OF, (operator, ANY_NUMBER_OF, left_paren, expression, ANY_NUMBER_OF, right_paren), '}', ANY_NUMBER_OF, smarty_language

def if_statement():         return '{', keyword('if'), ANY_NUMBER_OF, left_paren, expression, ANY_NUMBER_OF, right_paren, ANY_NUMBER_OF, (operator, ANY_NUMBER_OF, left_paren, expression, ANY_NUMBER_OF, right_paren), '}', ANY_NUMBER_OF, smarty_language, ANY_NUMBER_OF, [else_statement, elseif_statement], '{/', keyword('if'), '}'

def for_statement():        return '{', keyword('foreach'), ANY_NUMBER_OF, [for_from, for_item, for_name, for_key], '}', ANY_NUMBER_OF, smarty_language, OPTIONALLY, foreachelse_statement, '{/', keyword('foreach'), '}'

"""
Finally, the actual language description.
"""
def smarty_language():      return AT_LEAST_ONE, [literal, if_statement, for_statement, function_statement, comment, print_statement, content]