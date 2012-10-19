# simple makefile to simplify repetetive build env management tasks under posix

PYTHON ?= python
NOSETESTS ?= nosetests
CTAGS ?= ctags
PREFIX := `pwd`
VERSION := `grep "VERSION = " pyAMI/info.py | cut -d " " -f 3 | sed "s/'//g"`

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
	rm -f .installed.cfg

clean: clean-build clean-dist clean-buildout clean-pyc clean-ctags

bootstrap:
	$(PYTHON) bootstrap.py

buildout:
	./bin/buildout

deploy:
	bin/buildout-source-release -n pyAMI-$(VERSION) \
		https://lpsc.in2p3.fr/svn/AMI/trunk/AMIWebServiceClient/pyAMI \
		buildout-source.cfg

release:
	./bin/buildout -c buildout-release.cfg 

sdist: clean
	$(PYTHON) setup.py sdist

upload: clean
	$(PYTHON) setup.py sdist upload

register:
	$(PYTHON) setup.py register

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
