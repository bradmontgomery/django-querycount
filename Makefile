PY_VER ?= 3.11
SHELL := /bin/bash

.PHONY: clean
clean:
	rm -Rf dist

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