# simple makefile to simplify repetetive build env management tasks under posix

PYTHON ?= python
NOSETESTS ?= nosetests
CTAGS ?= ctags
PREFIX := `pwd`
VERSION := `cat version.txt`

all: clean test

clean-pyc:
	find pyAMI -name "*.pyc" | xargs rm -f

clean-build:
	rm -rf build
	rm -rf pyAMI.egg-info

clean-dist:
	rm -rf dist

clean-ctags:
	rm -f tags

clean-buildout:
	rm -rf bin
	rm -rf eggs
	rm -rf parts
	rm -rf develop-eggs 
	rm -rf downloads
	rm -rf lib
	rm -rf cache
	rm -rf pyAMI-*
	rm -f .installed.cfg

clean: clean-build clean-dist clean-buildout clean-pyc clean-ctags

bs: bootstrap # just a shortcut
bootstrap: clean-buildout
	mkdir cache
	$(PYTHON) bootstrap.py

bo: buildout # just a shortcut
buildout:
	./bin/buildout

bundle: sdist bootstrap
	./bin/buildout -c release.cfg
	mkdir pyAMI-$(VERSION)
	cp bootstrap.py pyAMI-$(VERSION)/
	cp install.cfg pyAMI-$(VERSION)/buildout.cfg
	cat versions.cfg >> pyAMI-$(VERSION)/buildout.cfg
	echo "pyAMI = $(VERSION)" >> pyAMI-$(VERSION)/buildout.cfg
	cp -r cache pyAMI-$(VERSION)/
	cp dist/pyAMI-$(VERSION).tar.gz pyAMI-$(VERSION)/cache/dist
	cp Makefile.install pyAMI-$(VERSION)/Makefile
	rm -rf pyAMI-4.0.4/cache/dist/setuptools*
	tar -cvzf pyAMI-$(VERSION)-bundle.tar.gz pyAMI-$(VERSION)/

sdist: clean
	$(PYTHON) setup.py sdist --release

upload: clean
	$(PYTHON) setup.py sdist upload --release

register:
	$(PYTHON) setup.py register --release

install:
	$(PYTHON) setup.py install

install-user:
	$(PYTHON) setup.py install --user

install-afs:
	./install_afs.sh

test-code:
	$(NOSETESTS) -s pyAMI

test-doc:
	$(NOSETESTS) -s --with-doctest --doctest-tests --doctest-extension=rst \
	--doctest-extension=inc --doctest-fixtures=_fixture docs/

test-coverage:
	rm -rf coverage .coverage
	$(NOSETESTS) -s --with-coverage --cover-html --cover-html-dir=coverage \
	--cover-package=pyAMI pyAMI

test: test-code test-doc

trailing-spaces:
	find pyAMI -name "*.py" | xargs perl -pi -e 's/[ \t]*$$//'

ctags:
	# make tags for symbol based navigation in emacs and vim
	# Install with: sudo apt-get install exuberant-ctags
	$(CTAGS) -R *

doc:
	make -C docs/ html

docs-update-end: doc
	# update Noel's mirror of the pyAMI docs
	rm -rf ~/remote/cern/projects/pyAMI/*
	cp -r ./docs/_build/html/* ~/remote/cern/projects/pyAMI/

clean-docs:
	make -C docs/ clean
