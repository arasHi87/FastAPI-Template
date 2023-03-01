from typing import Generator

import pytest
from app import APP
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(APP) as tc:
        yield tc
