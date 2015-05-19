.PHONY: clean

install:
	pip install -r .

clean:
	find . -type f -name '*.pyc' -delete


css:
	lessc --source-map --source-map-less-inline localshop/static/localshop/less/main.less localshop/static/localshop/css/main.css
	
