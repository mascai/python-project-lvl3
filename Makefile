install:
	poetry install

lint:
	poetry run flake8 page_loader

test:
	poetry run pytest

test-cov:
	poetry run pytest --cov=page-loader tests  --cov-report xml
