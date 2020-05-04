# Makefile for project continuum

VERSION=0.1.3
BUILD_DIR=build
NAME=continuum

YEL="\\033[93m"
END="\\033[0m"

help: # Print build file help
	@make-help

dist: clean # Generat distribution archive
	@echo "$(YEL)Generating distribution archive$(END)"
	mkdir $(BUILD_DIR)
	cp etc/setup.py $(BUILD_DIR)/setup.py
	sed -i 's/#VERSION#/$(VERSION)/g' $(BUILD_DIR)/setup.py
	cp etc/MANIFEST.in README.rst LICENSE $(BUILD_DIR)/
	mkdir $(BUILD_DIR)/$(NAME)
	cp src/*.py $(BUILD_DIR)/$(NAME)/
	cd $(BUILD_DIR) && python setup.py sdist -d .

upload: # Upload distribution archive
	@echo "$(YEL)Uploading distribution archive$(END)"
	cd $(BUILD_DIR) && python setup.py sdist -d . register upload

tag: # Tag release
	@echo "$(YEL)Tagging release$(END)"
	git tag -a $(VERSION) -m 'Release $(VERSION)'
	git push --tags

release: dist upload tag # Perform a release
	@echo "$(YEL)Performing release$(END)"

clean: # Clean generated files
	@echo "$(YEL)Cleaning generated files$(END)"
	rm -rf $(BUILD_DIR)
