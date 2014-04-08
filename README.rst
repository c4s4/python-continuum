=========
CONTINUUM
=========

Continuum is a lightweight continuous integration tool: no web interface, no 
scheduler. It runs on command line and is triggered by cron.

Installation
============

You may install it using PIP, typing *pip install continuum*. This will install
the *continuum* script in you PATH. You may also call the *continuum.py* script
in the archive with python: *python continuum.py*.

While calling continuum, you must pass the configuration file name on the 
command line::

  continuum config.yml


Configuration
=============

Configuration file is a YAML one::

  directory:  /tmp
  smtp_host:  smtp.foo.com
  emaili_to:  foo@bar.com
  email_from: foo@bar.com
  on_success: false
  
  modules:
    continuum:
      url:     https://github.com/c4s4/continuum.git
      command: |
        set -e
        virtualenv env --no-site-packages 
        . env/bin/activate
        pip install -r etc/requirements.txt
        bee test
    module2:
      url:     https://github.com/foo/bar.git
      command:
        set -e
        commands to run the test

The first part indicates::

- directory: the directory where modules will be checked out.
- smtp_host: the hostname of your SMTP server.
- email_to:  the email of the recipient of the build report.
- email_from: the email address if the sender of the report.
- on_success: tells if continuum will send an email on success. If *false*, it
  will only send an email on build error.

The second one is the list of modules, with, for each module::

- url: the URL of the module that GIT will use to get the sources.
- command: the command to run tests, must return 0 on success and a different
  value on error (as any Unix script should).

Crontab
=======

This script is triggered using cron, with as configuration as follows::

  # run continuum at 4 every night
  0   4 * * *  me    continuum /home/me/etc/continuum.yml

Enjoy!

