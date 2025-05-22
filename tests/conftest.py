import pytest
from playwright.sync_api import sync_playwright

# Launch Playwright once per session
@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def request_context(playwright_instance):
    context = playwright_instance.request.new_context()
    yield context
    context.dispose()

# Launch browser once per session
@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(headless=False)
    yield browser
    browser.close()

# Create a new page per test function
@pytest.fixture(scope="function")
def page(browser):
    page = browser.new_page()
    yield page
    page.close()

