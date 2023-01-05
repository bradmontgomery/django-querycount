PY_VER ?= 3.11
SHELL := /bin/bash

# Minimal makefile for Sphinx documentation
# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = docs/_src
BUILDDIR      = docs

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
.PHONY: help Makefile
# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)


.PHONY: docs
docs:
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: clean
clean:
	rm -Rf dist django_querycount.egg-info

.PHONY: install
install:
	pip install --upgrade pip pip-tools pre-commit
	pip install -r requirements.txt
	pre-commit install

.PHONY: compile
compile:
	pip install --upgrade pip pip-tools pre-commit
	pip-compile -rU --no-emit-index-url -o requirements.txt requirements.in
	pre-commit autoupdate

.PHONY: build
build:
	python -m build

.PHONY: upload
upload:
	python -m twine upload --repository pypi dist/*