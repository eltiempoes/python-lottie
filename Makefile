PYTHON=python3
SETUP=setup.py
PACKAGE_NAME=$(shell $(PYTHON) $(SETUP) --name)
VERSION=$(shell $(PYTHON) $(SETUP) --version)

dist/$(PACKAGE_NAME)-$(VERSION).tar.gz: $(SETUP)
	$(PYTHON) $(SETUP) sdist

.PHONY: upload docs

upload: dist/$(PACKAGE_NAME)-$(VERSION).tar.gz
	$(PYTHON) -m twine upload dist/$(PACKAGE_NAME)-$(VERSION).tar.gz

docs:
	$(PYTHON) docs/dox_examples.py
	$(PYTHON) docs/dox_lottie.py
	doxygen docs/Doxyfile
