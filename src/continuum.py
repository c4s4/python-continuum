#!/usr/bin/env python
# encoding: UTF-8

import os
import sys
import yaml


class Continuum(object):

    def __init__(self, config):
        with open(config) as stream:
            self.config = yaml.load(stream)

    def run(self):
        if not os.path.exists(self.config['directory']):
            os.mkdirs(self.config['directory'])
        builds = {}
        modules = self.config['modules']
        for module in modules.keys():
            builds[module] = self.build(name=module,
                                        module=modules[module])
    
    def build(self, name, module):
        url = module['url']
        command = module['command']
        report = {}
        current_dir = os.getcwd()
        try:
            os.chdir(self.config['directory'])
            self.execute_with_output("")
            report['error'] = False
        except Exception:
            report['error'] = True
        finally:
            os.chdir(current_dir)
        


if __name__ == '__main__':
    for _config in sys.argv[1:]:
        Continuum(_config).run()
