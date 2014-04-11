#!/usr/bin/env python
# encoding: UTF-8

import os
import sys
import yaml
#pylint: disable=W0403
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
        start_time = datetime.datetime.now()
        if not os.path.exists(self.config['directory']):
            os.mkdirs(self.config['directory'])
        builds = {}
        modules = self.config['modules']
        for module in sorted(modules.keys()):
            builds[module] = self.build(name=module,
                                        module=modules[module])
        duration = datetime.datetime.now() - start_time
        self.send_report(builds, duration)
    
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
            report['success'] = True
            print 'OK'
        except subprocess.CalledProcessError, e:
            report['success'] = False
            report['output'] += e.output
            print 'ERROR'
        finally:
            if os.path.exists(module_dir):
                shutil.rmtree(module_dir)
            os.chdir(current_dir)
        return report
    
    def send_report(self, builds, duration):
        success = True
        for build in builds.values():
            if not build['success']:
                success = False
        if not success:
            self.send_failure_email(builds, duration)
        elif success and self.config['on_success']:
            self.send_success_email(builds, duration)
    
    def send_failure_email(self, builds, duration):
        print 'Sending failure email'
        subject = 'Build was a failure on %s' % self.datetime
        text = 'Build on %s:\n\n' % self.datetime
        for module in sorted(builds.keys()):
            status = 'OK' if builds[module]['success'] else 'ERROR'
            text += '  %s: %s\n' % (module, status)
        text += '\nReports:\n\n'
        for module in sorted(builds.keys()):
            if not builds[module]['success']:
                text += '='*80 + '\n'
                text += module + '\n'
                text += '-'*80 + '\n'
                text += builds[module]['output'] + '\n'
                text += '-'*80 + '\n\n'
        self.send_email(subject=subject, text=text,
                        duration=duration)
    
    def send_success_email(self, builds, duration):
        print 'Sending success email'
        subject = 'Build was a success on %s' % self.datetime
        text = 'Build on %s:\n\n' % self.datetime
        for module in sorted(builds.keys()):
            text += '  %s: OK\n' % module
        self.send_email(subject=subject, text=text,
                        duration=duration)
    
    def send_email(self, subject, text, duration):
        email_from = self.config['email_from']
        email_to = self.config['email_to']
        smtp_host = self.config['smtp_host']
        text += '\nDone in %s' % duration
        text += '\n--\nContinuum'
        mail.send(subject=subject, text=text, sender=email_from,
                  recipients=[email_to], smtp_host=smtp_host)
        
    @staticmethod
    def execute_with_output(command, stdin=None, shell=False):
        if stdin:
            return subprocess.check_output(command, stderr=subprocess.STDOUT, stdin=stdin, shell=shell)
        else:
            return subprocess.check_output(command, stderr=subprocess.STDOUT, shell=shell)


def run():
    for config in sys.argv[1:]:
        Continuum(config).run()


if __name__ == '__main__':
    run()

