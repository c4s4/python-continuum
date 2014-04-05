#!/usr/bin/env python
# encoding: UTF-8

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import unittest
import continuum

class Test(unittest.TestCase):

    def test(self):
        continuum.Continuum().main()


if __name__ == '__main__':
    unittest.main()

