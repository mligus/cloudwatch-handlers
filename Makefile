clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . \( -name \*.pyc -o -name \*.pyo -o -name __pycache__ \) -prune -exec rm -rf {} +

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info
	rm -fr *.egg

clean-test:
	rm -fr coverage_html/
	rm -f .coverage*

clean: clean-pyc clean-build clean-test

init:
	pip install -r requirements.txt

lint:
	python setup.py flake8

test: clean
	py.test tests

wheel: clean
	python setup.py bdist_wheel

help:
	@echo "    clean"
	@echo "        Clean working directory from build and tests artifacts"
	@echo "    init"
	@echo "        Initialize development environment (pip, etc.)"
	@echo "    lint"
	@echo "        Run linter (flake8)"
	@echo "    test"
	@echo "        Run unit tests"
	@echo "    wheel"
	@echo "        Make wheel package"

.PHONY: clean init lint test wheel
