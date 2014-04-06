#!/usr/bin/env python
# encoding: UTF-8

import os
import sys
import yaml
import shutil
import subprocess


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
        print builds
    
    def build(self, name, module):
        print 'Building module %s...' % name,
        sys.stdout.flush()
        report = {'name': name}
        current_dir = os.getcwd()
        try:
            module_dir = os.path.join(self.config['directory'], name)
            os.chdir(self.config['directory'])
            if os.path.exists(module_dir):
                shutil.rmtree(module_dir)
            command = ['git', 'clone', module['url'], name]
            report['output'] = '## CHECKOUT ##\n'
            report['output'] += self.execute_with_output(command)
            shutil.rmtree(os.path.join(module_dir, '.git'))
            os.chdir(module_dir)
            report['output'] += '\n## BUILD ##\n'
            report['output'] += self.execute_with_output(module['command'], shell=True)
            os.chdir(self.config['directory'])
            shutil.rmtree(module_dir)
            report['error'] = False
            print 'OK'
        except subprocess.CalledProcessError, e:
            report['error'] = True
            report['output'] += e.output
            print 'ERROR'
        finally:
            os.chdir(current_dir)
        return report
        
    @staticmethod
    def execute_with_output(command, stdin=None, shell=False):
        if stdin:
            return subprocess.check_output(command, stderr=subprocess.STDOUT, stdin=stdin, shell=shell)
        else:
            return subprocess.check_output(command, stderr=subprocess.STDOUT, shell=shell)

if __name__ == '__main__':
    for _config in sys.argv[1:]:
        Continuum(_config).run()
