from collections.abc import Generator

import pytest
from playwright.sync_api import APIRequestContext


# Configure the base URL for all tests.
@pytest.fixture(scope="session")
def api(playwright) -> Generator[APIRequestContext, None, None]:
    request_context = playwright.request.new_context(base_url="http://api:8000")
    yield request_context
    request_context.dispose()