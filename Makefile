# Makefile for project continuum
# See make-tools at https://github.com/c4s4/make-tools

# Parent makefiles at https://github.com/c4s4/make
include .make/help.mk
include .make/python.mk
include .make/git.mk
include ~/.make/make.mk

MAKE_ID=a28d5c443b96f004f271c371364dfb821954f198
PYTHON_MOD=continuum
PYTHON_PKG=continuum_ci
PYTHON_ENV=~/.env/email.env
PYTHON_ITG=. $(PYTHON_ENV) && RESULT=0 && venv/bin/continuum ../continuum.yml
