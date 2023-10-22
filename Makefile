.PHONY: install

install:
	pip install pre-commit
	pre-commit install

test:
	python -m pytest test_main.py

commit:
	git add .
	git commit

fmt:
	python -m black .
