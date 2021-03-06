#!/usr/bin/env python
# encoding: UTF-8

import os
import sys
import unittest
from io import StringIO
import continuum.continuum


class Test(unittest.TestCase):

    TEST_DIR = os.path.dirname(__file__)
    CONFIG = os.path.join(TEST_DIR, '..', 'continuum.yml')

    def test_continuum_success(self):
        os.environ['RESULT'] = "0"
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            continuum.Continuum(self.CONFIG).run()
        finally:
            sys.stdout = old_stdout

    def test_continuum_failure(self):
        os.environ['RESULT'] = "1"
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            continuum.Continuum(self.CONFIG).run()
        finally:
            sys.stdout = old_stdout


if __name__ == '__main__':
    unittest.main()
