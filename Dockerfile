FROM python:3.8.12-slim

WORKDIR /api/

COPY ./api/ /api/
COPY poetry.lock /api/poetry.lock
COPY pyproject.toml /api/pyproject.toml 

RUN pip3 install -U pip setuptools && \
    pip3 install poetry && \
    poetry install

CMD ["poetry", "run", "uvicorn", "--port", "8000", "--host", "0.0.0.0","--log-level", "error", "app:APP"]