.PHONY: install clean test retest coverage lint css

install:
	pip install -e .[test]

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

test:
	pytest

retest:
	pytest --lf

coverage:
	py.test --cov=localshop --cov-report=term-missing --nomigrations tests/

lint:
	flake8 src/ tests/

css:
	lessc --source-map --source-map-less-inline localshop/static/localshop/less/main.less localshop/static/localshop/css/main.css

