#!/usr/bin/env python
# encoding: UTF-8

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import unittest
from . import continuum
from io import StringIO


class Test(unittest.TestCase):

    TEST_DIR = os.path.dirname(__file__)
    CONFIG = os.path.join(TEST_DIR, '..', 'etc', 'continuum.yml')

    def test_continuum(self):
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            continuum.Continuum(self.CONFIG).run()
        finally:
            sys.stdout = old_stdout


if __name__ == '__main__':
    unittest.main()
