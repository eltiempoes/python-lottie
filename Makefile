PYTHON=python3
SETUP=setup.py
PACKAGE_NAME:=$(shell $(PYTHON) $(SETUP) --name)
VERSION_SUF:=$(shell git rev-parse --short HEAD)
VERSION_BASE:=$(shell $(PYTHON) $(SETUP) --version)
VERSION=$(VERSION_BASE)$(if $(VERSION_SUF),+dev$(VERSION_SUF),)
SRC:=$(shell find lib -type f -name '*.py')
OBJECTS:=$(shell find lib/tgs/objects -type f -name '*.py')
SCRIPTS:=$(wildcard bin/*.py)

.SUFFIXES:

.PHONY: all upload docs clean_pyc pypi blender inkscape release dist distclean synfig


all: pypi blender inkscape synfig

dist: all

distclean:
	rm dist/*

release:
	make all upload VERSION_SUF=

dist/$(PACKAGE_NAME)-$(VERSION).tar.gz: $(SETUP) $(SRC) $(SCRIPTS)
	VERSION_OVERRIDE="$(VERSION)" $(PYTHON) $(SETUP) sdist

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

docs/dox/downloads.dox: docs/dox_download.py setup.py
	$(PYTHON) docs/dox_download.py --version-base $(VERSION_BASE) --version-suf $(VERSION_SUF) --version $(VERSION)

docs/html/index.html: docs/Doxyfile
docs/html/index.html: $(foreach file,$(wildcard examples/*.py), docs/dox/examples/$(basename $(notdir $(file))).dox)
docs/html/index.html: docs/dox/lottie.dox
docs/html/index.html: docs/dox/scripts.dox
docs/html/index.html: docs/dox/downloads.dox
docs/html/index.html: $(SRC)
	doxygen docs/Doxyfile

dist/$(PACKAGE_NAME)-inkscape-$(VERSION).zip: $(wildcard addons/inkscape/*)
	zip --junk-paths $@ $^
	echo "Upload at https://inkscape.org/~mattia.basaglia/%E2%98%85tgslottie-importexport"

docs/dox/scripts.dox: docs/dox_scripts.py
docs/dox/scripts.dox: $(SCRIPTS)
	$(PYTHON) docs/dox_scripts.py

clean_pyc:
	find lib -name '*.pyc' -delete
	find lib -name '__pycache__' -exec rm -rf {} \;


dist/$(PACKAGE_NAME)-blender-$(VERSION).zip: $(wildcard addons/blender/tgs_io/*.py) $(SRC)
	cd addons/blender && find -L -name '*.py' | xargs zip --filesync ../../$@

dist/$(PACKAGE_NAME)-synfig-$(VERSION).zip: $(wildcard addons/synfig/*)
	cd addons/synfig && find -L -type f -not -name "*.pyc" | xargs zip --filesync ../../$@

pypi: dist/$(PACKAGE_NAME)-$(VERSION).tar.gz

inkscape: dist/$(PACKAGE_NAME)-inkscape-$(VERSION).zip

blender: dist/$(PACKAGE_NAME)-blender-$(VERSION).zip

synfig: dist/$(PACKAGE_NAME)-synfig-$(VERSION).zip
