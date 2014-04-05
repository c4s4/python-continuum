#!/usr/bin/env python
# encoding: UTF-8

import yaml


class Continuum(object):

    def __init__(self, config):
        with open(config) as stream:
            self.config = yaml.load(stream)

    def run(self):
        pass


if __name__ == '__main__':
    for config in sys.argv[1:]:
        Continuum(config).run()
