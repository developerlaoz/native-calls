#!/usr/bin/env python
# Copyright (c) 2013 The Chromium Authors. All rights reserved.
# Copyright (c) 2014 Mohamed Eltuhamy. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import glob
import re
import unittest

from idl_lexer import IDLLexer
from idl_parser import IDLParser
from idl_cpp import CPPCompiler
from pycparser import parse_file, c_parser, c_ast, c_generator

class WebIDLCompiler(unittest.TestCase):

    def setUp(self):
        self.parser = IDLParser(IDLLexer(), mute_error=True)
        self.cparser = c_parser.CParser()
        self.compiler = CPPCompiler(self.parser);
        self.filenames = glob.glob('test_cpp/*.idl')

    def translate_to_c(self, string):
        # remove comments
        string = re.sub(r'(/\*(.|\n)*?\*/)|(//.*?\n)', '', string)
        ast = self.cparser.parse(string)
        generator = c_generator.CGenerator()
        return generator.visit(ast)




    def testOutput(self):
        for filename in self.filenames:
            compiledOutput = self.compiler.CompileFile(filename)
            expectedOutput = open(filename.replace('.idl','.h')).read()
            self.assertEqual(self.translate_to_c(compiledOutput), self.translate_to_c(expectedOutput), 'Expecting output in %s.' % filename)


if __name__ == '__main__':
    unittest.main(verbosity=2)
