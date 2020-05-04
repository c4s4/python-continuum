# Makefile for project continuum
# See make-tools at https://github.com/c4s4/make-tools

# Parent makefiles at https://github.com/c4s4/make
include ~/.make/color.mk
include ~/.make/help.mk
include ~/.make/clean.mk
include ~/.make/git.mk

VERSION=0.1.4
NAME=continuum
DIR=$(shell pwd)
VENV=$(DIR)/venv
PYTHON=$(VENV)/bin/python

.PHONY: venv
venv: # Create virtual environment
	@echo "$(YEL)Creating virtual environment$(END)"
	rm -rf $(VENV)
	python -m venv $(VENV)

libs: venv # Install libraries
	@echo "$(YEL)Installing libraries$(END)"
	$(VENV)/bin/pip install -r etc/requirements.txt

.PHONY: test
test: # Run tests
	@echo "$(YEL)Running tests$(END)"
	$(PYTHON) -m $(NAME).test_$(NAME)

dist: clean # Generat distribution archive
	@echo "$(YEL)Generating distribution archive$(END)"
	mkdir $(BUILD_DIR)
	cp etc/setup.py $(BUILD_DIR)/setup.py
	sed -i 's/#VERSION#/$(VERSION)/g' $(BUILD_DIR)/setup.py
	cp etc/MANIFEST.in README.rst LICENSE $(BUILD_DIR)/
	cp -r $(NAME) $(BUILD_DIR)
	cd $(BUILD_DIR) && $(PYTHON) setup.py sdist -d .

upload: # Upload distribution archive
	@echo "$(YEL)Uploading distribution archive$(END)"
	cd $(BUILD_DIR) && $(PYTHON) setup.py sdist -d . register upload

tag: # Tag release
	@echo "$(YEL)Tagging release$(END)"
	git tag -a $(VERSION) -m 'Release $(VERSION)'
	git push --tags

publish: dist upload tag # Publish archive on Pypi
	@echo "$(YEL)Published archive on Pypi$(END)"
