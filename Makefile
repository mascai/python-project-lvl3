install:
	poetry install

lint:
	poetry run flake8 page_loader

test:
	poetry run pytest

test-cov:
	poetry run pytest -vv --cov=page_loader --cov-report xml tests/
