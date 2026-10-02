from collections.abc import Generator
import os

import pytest
from playwright.sync_api import APIRequestContext


API_BASE_URL = "http://api:8000"


@pytest.fixture
def scenario_state() -> dict:
    return {}


@pytest.fixture(scope="session")
def api(playwright) -> Generator[APIRequestContext, None, None]:
    token = os.environ["PAYMENT_API_TOKEN"]
    request_context = playwright.request.new_context(
        base_url=API_BASE_URL,
        extra_http_headers={"Authorization": f"Bearer {token}"},
    )
    yield request_context
    request_context.dispose()


@pytest.fixture
def unauthenticated_api(playwright) -> Generator[APIRequestContext, None, None]:
    request_context = playwright.request.new_context(base_url=API_BASE_URL)
    yield request_context
    request_context.dispose()


@pytest.fixture
def invalid_token_api(playwright) -> Generator[APIRequestContext, None, None]:
    token = os.environ["PAYMENT_API_TOKEN"]
    request_context = playwright.request.new_context(
        base_url=API_BASE_URL,
        extra_http_headers={"Authorization": f"Bearer {token}-invalid"},
    )
    yield request_context
    request_context.dispose()