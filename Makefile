setup-git:
	@echo "--> Installing git hooks"
	@pip install flake8
	@cd .git/hooks && ln -sf ../../hooks/* ./

test:
	@py.test -vv --tb=short

prepare:
	source .py3/bin/activate;rm -rf dist/;python setup.py sdist

test-release:
	source .py3/bin/activate;twine upload --repository testpypi dist/*

prod-release:
	source .py3/bin/activate;twine upload dist/*
