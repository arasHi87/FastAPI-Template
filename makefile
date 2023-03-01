APP = api

.PHONY: clean init

init: clean
	cp env-sample .env
	poetry env use python3.8 
	poetry install 

lint:
	poetry run flake8 ${APP}

analysis:
	poetry run bandit ${APP}

format:
	poetry run black ${APP}
	poetry run isort ${APP}

test:
	poetry run pytest -vv --cov-report=term-missing --cov=${APP}/endpoints ${APP}/tests

ci-bundle: analysis format lint test

clean:
	find . -type f -name '*.py[co]' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	rm -rf .hypothesis
	rm -rf .pytest_cache
	rm -rf .tox
	rm -f report.xml
	rm -f coverage.xml