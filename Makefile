BIN = .venv/bin

.PHONY: install
install:
	pyenv install -s
	pyenv local
	python -m venv .venv
	$(BIN)/pip install -e .[test]

.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

.PHONY: test
test:
	$(BIN)/pytest

.PHONY: retest
retest:
	$(BIN)/pytest --lf

.PHONY: coverage
coverage:
	$(BIN)/pytest --cov=localshop --cov-report=term-missing --nomigrations tests/

.PHONY: lint
lint:
	$(BIN)/flake8 src/ tests/

.PHONY: css
css:
	lessc --source-map --source-map-less-inline localshop/static/localshop/less/main.less localshop/static/localshop/css/main.css

