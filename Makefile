# Makefile for project continuum
# See make-tools at https://github.com/c4s4/make-tools

# Parent makefiles at https://github.com/c4s4/make
include ~/.make/Python.mk

PYTHON_MOD=continuum
PYTHON_PKG=continuum_ci
PYTHON_ENV=~/.env/email.env
PYTHON_ITG=. $(PYTHON_ENV) && RESULT=0 && venv/bin/continuum ../continuum.yml
