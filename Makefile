.PHONY: run
ARG ?= "default"
run:
	@echo "Running main.py"
	@python main.py

install:
	@pip install -r requirements.txt
	@pre-commit install

test:
	@echo "Running tests..."
	@python -m pytest test_main.py

commit:
	@echo "Committing changes..."
	@git add .
	@git commit

fmt:
	@echo "Formatting code..."
	@python -m black .

-v:
	@ echo "Creating virtual environment with variable name"
	@ python -m venv $(ARG)

activate:
	@ echo "Activating virtual environment"
	@ source $(ARG)/bin/activate

-V:
	@ echo "Creating virtual environment with variable name"
	@ pipenv shell
