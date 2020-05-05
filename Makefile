# Makefile for project continuum
# See make-tools at https://github.com/c4s4/make-tools

# Parent makefiles at https://github.com/c4s4/make
include ~/.make/help.mk
include ~/.make/python.mk
include ~/.make/clean.mk
include ~/.make/git.mk

PYTHON_MOD=continuum

integ: dist # Run integration test
	@echo "$(YEL)Running integration test$(END)"
	@mkdir -p $(BUILD_DIR); \
	cd $(BUILD_DIR); \
	$(PYTHON) -m venv venv; \
	venv/bin/pip install --upgrade pip; \
	venv/bin/pip install ./continuum_ci-0.0.0.tar.gz; \
	venv/bin/continuum ../continuum.yml

pypi: clean # Test installation from Pypi
	@echo "$(YEL)Testing installation from Pypi$(END)"
	@mkdir -p $(BUILD_DIR); \
	cd $(BUILD_DIR); \
	$(PYTHON) -m venv venv; \
	venv/bin/pip install --upgrade pip; \
	venv/bin/pip install continuum_ci; \
	venv/bin/continuum ../continuum.yml

dist: clean # Generat distribution archive
	@echo "$(YEL)Generating distribution archive$(END)"
	mkdir -p $(BUILD_DIR)
	cp -r $(PYTHON_MOD) LICENSE MANIFEST.in README.rst setup.py $(BUILD_DIR)/
	sed -i 's/0.0.0/$(TAG)/g' $(BUILD_DIR)/setup.py
	cd $(BUILD_DIR) && $(PYTHON) setup.py sdist -d .

upload: dist # Upload distribution archive
	@echo "$(YEL)Uploading distribution archive$(END)"
	cd $(BUILD_DIR) && $(PYTHON) setup.py sdist -d . register upload

release: clean lint test integ tag upload # Release project on Pypi
	@echo "$(YEL)Released project on Pypi$(END)"
