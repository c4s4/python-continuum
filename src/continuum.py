#!/usr/bin/env python
# encoding: UTF-8

import sys
import yaml


class Continuum(object):

    def __init__(self, config):
        with open(config) as stream:
            self.config = yaml.load(stream)

    def run(self):
        pass


if __name__ == '__main__':
    for _config in sys.argv[1:]:
        Continuum(_config).run()
