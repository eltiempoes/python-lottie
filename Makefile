PYTHON=python3
SETUP=setup.py
PACKAGE_NAME=$(shell $(PYTHON) $(SETUP) --name)
VERSION=$(shell $(PYTHON) $(SETUP) --version)
SRC=$(shell find lib -type f -name '*.py')
OBJECTS=$(shell find lib/tgs/objects -type f -name '*.py')

.SUFFIXES:

.PHONY: upload docs clean_pyc

dist/$(PACKAGE_NAME)-$(VERSION).tar.gz: $(SETUP)
	$(PYTHON) $(SETUP) sdist

upload: dist/$(PACKAGE_NAME)-$(VERSION).tar.gz
	$(PYTHON) -m twine upload dist/$(PACKAGE_NAME)-$(VERSION).tar.gz

docs: docs/html/index.html

docs/Doxyfile: docs/Doxyfile.in setup.py
	m4 -P -DM4_NAME="$(PACKAGE_NAME)" -DM4_VERSION="$(VERSION)" -DM4_DESCRIPTION="$(shell $(PYTHON) $(SETUP) --description)" $< >$@

docs/dox/lottie.dox: docs/dox_lottie.py
docs/dox/lottie.dox: $(OBJECTS)
	$(PYTHON) docs/dox_lottie.py

docs/dox/examples/%.dox: examples/%.py docs/dox_examples.py
	$(PYTHON) docs/dox_examples.py $*

docs/html/index.html: docs/Doxyfile
docs/html/index.html: $(foreach file,$(wildcard examples/*.py), docs/dox/examples/$(basename $(notdir $(file))).dox)
docs/html/index.html: docs/dox/lottie.dox
docs/html/index.html: docs/dox/scripts.dox
docs/html/index.html: $(SRC)
	doxygen docs/Doxyfile

dist/tgs-inkscape.zip: $(wildcard inkscape/*)
	zip --junk-paths $@ $^

docs/dox/scripts.dox: docs/dox_scripts.py
docs/dox/scripts.dox: $(wildcard bin/*.py)
	$(PYTHON) docs/dox_scripts.py

clean_pyc:
	find lib -name '*.pyc' -delete
	find lib -name '__pycache__' -exec rm -rf {} \;
