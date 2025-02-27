.PHONY: install format lint test run

install:
	pip install -r requirements.txt

format:
	black .

lint:
	flake8 --max-line-length=100

test:
	pytest tests/

run:
	python pre_project/data_generator.py
