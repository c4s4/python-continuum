=========
CONTINUUM
=========

Continuum is a lightweight continuous integration tool: no web interface, no scheduler. It runs on command line and is triggered by cron.

Installation
============

You can install it using PIP, typing *pip install continuum*. This will install the *continuum* script in you PATH. You may also download the archive, expand it and type in the created directory *sudo python setup.py install*.

While calling continuum, you must pass the configuration file name on the command line::

  continuum config.yml


Configuration
=============

Configuration is in YAML format::

  directory:  /tmp
  email:
    smtp_host: smtp.foo.com
    recipient: foo@bar.com
    sender:    foo@bar.com
    success:   false

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
      command: |
        set -e
        commands to run the test

The first part indicates:

- directory: the directory where modules will be checked out. Currently only GIT projects are supported.
- email: put *~* if you don't want any email.

If you wait to receive email reports, provide following fields:

- smtp_host: the hostname of your SMTP server.
- recipient:  the email of the recipient of the build report.
- sender: the email address if the sender of the report.
- success: tells if continuum should send an email on success. If *false*, it will only send an email on build error.

The second one is the list of modules, with, for each module:

- url: the URL of the module that GIT will use to get the sources.
- command: the command to run tests, must return 0 on success and a different value on error (as any Unix script should). Note the pipe character (that is *|*) after the *command:* declaration.

The most important thing to remember about editting YAML is that Tab characters are forbidden (and should be replaced with spaces to properly indent). Please see YAML specification (at http://www.yaml.org/spec/1.2/spec.html) for more details.

Crontab
=======

This script is triggered using cron, with as configuration as follows (in file */etc/crontab*)::

  # run continuum at 4 every night
  0   4 * * *  me    continuum /home/me/etc/continuum.yml

Please make sure that the PATH to continuum is defined in your cron configuration. You may add the right PATH at the beginning of your *crontab* file as following::

  PATH=/path/to/continuum:/rest/of/my/path

  # run continuum at 4 every night
  0   4 * * *  me    continuum /home/me/etc/continuum.yml

Releases
========

- **0.1.3** (*2020-04-05*): Project renamed continuum_ci and added makefile.
- **0.1.2** (*2014-04-15*): Fixed documentation.
- **0.1.1** (*2014-04-11*): Improved email reporting.
- **0.1.0** (*2014-04-08*): First public release.

Enjoy!
