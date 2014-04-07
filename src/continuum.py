#!/usr/bin/env python
# encoding: UTF-8

import os
import sys
import yaml
import mail
import shutil
import datetime
import subprocess


class Continuum(object):

    def __init__(self, config):
        with open(config) as stream:
            self.config = yaml.load(stream)
        self.datetime = str(datetime.datetime.now())[:19]

    def run(self):
        if not os.path.exists(self.config['directory']):
            os.mkdirs(self.config['directory'])
        builds = {}
        modules = self.config['modules']
        for module in sorted(modules.keys()):
            builds[module] = self.build(name=module,
                                        module=modules[module])
        self.send_report(builds)
    
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
            report['output'] = 'Error checking out project:\n'
            self.execute_with_output(command)
            shutil.rmtree(os.path.join(module_dir, '.git'))
            os.chdir(module_dir)
            report['output'] = 'Error building project:\n'
            report['output'] = self.execute_with_output(module['command'], shell=True)
            os.chdir(self.config['directory'])
            shutil.rmtree(module_dir)
            report['success'] = True
            print 'OK'
        except subprocess.CalledProcessError, e:
            report['success'] = False
            report['output'] += e.output
            print 'ERROR'
        finally:
            os.chdir(current_dir)
        return report
    
    def send_report(self, builds):
        success = True
        for build in builds.values():
            if not build['success']:
                success = False
        if not success:
            self.send_failure_email(builds)
        elif success and self.config['on_success']:
            self.send_success_email(builds)
    
    def send_failure_email(self, builds):
        print 'Sending failure email'
        subject = 'Build was a failure on %s' % self.datetime
        text = 'Build on %s:\n\n' % self.datetime
        for module in sorted(builds.keys()):
            status = 'OK' if builds[module]['success'] else 'ERROR'
            text += '%s: %s\n' % (module, status)
        text += '\nReports:\n\n'
        for module in sorted(builds.keys()):
            if not builds[module]['success']:
                text += '='*80 + '\n'
                text += module + '\n'
                text += '-'*80 + '\n'
                text += builds[module]['output'] + '\n'
                text += '-'*80 + '\n\n'
        self.send_email(subject=subject, text=text)
    
    def send_success_email(self, builds):
        print 'Sending success email'
        subject = 'Build was a success on %s' % self.datetime
        text = 'Build on %s:\n\n' % self.datetime
        for module in sorted(builds.keys()):
            text += '%s: OK\n' % module
        self.send_email(subject=subject, text=text)
    
    def send_email(self, subject, text):
        email_from = self.config['email_from']
        email_to = self.config['email']
        smtp_host = self.config['smtp_host']
        text += '\n\n--\nContinuum'
        mail.send(subject=subject, text=text, sender=email_from,
                  recipients=[email_to], smtp_host=smtp_host)
        
    @staticmethod
    def execute_with_output(command, stdin=None, shell=False):
        if stdin:
            return subprocess.check_output(command, stderr=subprocess.STDOUT, stdin=stdin, shell=shell)
        else:
            return subprocess.check_output(command, stderr=subprocess.STDOUT, shell=shell)

if __name__ == '__main__':
    for _config in sys.argv[1:]:
        Continuum(_config).run()
