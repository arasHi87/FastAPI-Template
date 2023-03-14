[![CI](https://github.com/arashi87/fastapi-template/actions/workflows/integration.yaml/badge.svg)](https://github.com/arashi87/fastapi-template/actions/workflows/integration.yaml)
[![CD](https://github.com/arashi87/fastapi-template/actions/workflows/release.yaml/badge.svg)](https://github.com/arashi87/fastapi-template/actions/workflows/release.yaml)
![Coverage](https://github.com/arashi87/fastapi-template/blob/master/coverage.svg)

# FastAPI Template

A simple fastapi template, using postgresql as database.

## Getting Started

This is an example of how you may give instructions on setting up your project locally. To get a local copy up and running follow these simple example steps.

### Prerequisites

- Python 3.8
- Poetry 1.1.12
- Docker 20.10.12
- Make 3.81

### Installation

1. Init environment, which will help you init poetry and install dependencies, it will also copy a new `.env` file.

```
make init
```

2. Install pre-commit hook, it will run `make ci-bundle` to ensure code quality when you commit.

```
poetry run pre-commit install
```

3. Run migrate command to use alembic upgrade database.

```
make migrate
```

4. Enter the environment and start developing

```
poetry shell
```

5. Start related components of API service

```
make service_up
```

6. run test to make sure project work correctly, this project use `pytest` and `pyytest-cov` for testing

```
make test
```

7. Start development API service, the service will run at `http://localhost:8000`

```
cd api && poetry run uvicorn app:APP --reload --host 0.0.0.0
```

### Formatting & Linting

1. This project uses `black`, `isort`, `flake8`, `pylint` for formatting and linting, you can customize these settings in the setup.cfg file.

```
make format
make lint
```

## Contribution

- arashi87 ([arasi27676271@gmail.com](arasi27676271@gmail.com))
