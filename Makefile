module := minihtml
version := $(shell sed -nre 's/^__version__ = "(.*)"/\1/p' src/$(module)/__init__.py)
sdist := dist/$(module)-$(version).tar.gz
wheel := dist/$(module)-$(version)-py3-none-any.whl

all: requirements.txt test

init:
	pip install --upgrade pip wheel pip-tools
	pip install -e .
	pip install -r requirements.txt

test:
	pytest -vv tests
	python -m doctest README.md

requirements.txt:
	pip-compile

upgrade-deps:
	pip-compile --upgrade
	pip install -r requirements.txt

build:
	rm -rf build dist
	python setup.py sdist
	python setup.py bdist_wheel

test-sdist:
	rm -rf venv-sdist
	python3 -m venv venv-sdist
	./venv-sdist/bin/pip --disable-pip-version-check install $(sdist)
	./venv-sdist/bin/python -c 'import $(module); print(f"{$(module).__version__ = }")'

test-wheel:
	rm -rf venv-wheel
	python3 -m venv venv-wheel
	./venv-sdist/bin/pip --disable-pip-version-check install $(wheel)
	./venv-sdist/bin/python -c 'import $(module); print(f"{$(module).__version__ = }")'

release: build test-sdist test-wheel
	@echo

clean:
	rm -rf build dist venv-sdist venv-wheel

.PHONY: all build init release test test-sdist test-wheel upgrade-deps
