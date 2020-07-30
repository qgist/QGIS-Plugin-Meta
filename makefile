
black:
	black .

clean:
	coverage erase
	make clean_py
	find src/ tests/ -name '*.htm' -exec rm -f {} +
	find src/ tests/ -name '*.html' -exec rm -f {} +
	find src/ tests/ -name '*.so' -exec rm -f {} +
	find src/ tests/ -name 'octave-workspace' -exec rm -f {} +
	-rm -r build/*
	-rm -r dist/*
	-rm -r src/*.egg-info

clean_py:
	find src/ tests/ -name '*.pyc' -exec rm -f {} +
	find src/ tests/ -name '*.pyo' -exec rm -f {} +
	find src/ tests/ -name '*~' -exec rm -f {} +
	find src/ tests/ -name '__pycache__' -exec rm -fr {} +

release:
	make clean
	python setup.py sdist bdist_wheel
	python setup.py sdist
	gpg --detach-sign -a dist/qgspluginmeta*.whl
	gpg --detach-sign -a dist/qgspluginmeta*.tar.gz

install:
	pip install -vU pip setuptools
	pip install -v -e .[dev]

upload:
	for filename in $$(ls dist/*.tar.gz dist/*.whl) ; do \
		twine upload $$filename $$filename.asc ; \
	done

test:
	make clean_py
	pytest --cov=qgspluginmeta --cov-config=setup.cfg
	coverage combine ; coverage html

testdata:
	-rm -r tests/data/*
	python makefile.py testdata
