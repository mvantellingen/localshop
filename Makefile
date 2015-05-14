.PHONY: clean

install:
	pip install -r .

clean:
	find . -type f -name '*.pyc' -delete
