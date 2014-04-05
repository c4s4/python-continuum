#!/usr/bin/env python
# encoding: UTF-8

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import unittest
import continuum

class Test(unittest.TestCase):

    TEST_DIR = os.path.dirname(__file__)
    CONFIG = os.path.join(TEST_DIR, 'config.yml')

    def test(self):
        continuum.Continuum(self.CONFIG).run()


if __name__ == '__main__':
    unittest.main()

