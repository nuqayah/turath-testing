import pytest
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

@pytest.fixture(scope="session")
def browser():
    """Create a browser instance that will be shared across all tests."""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def context(browser: Browser):
    """Create a new browser context for each test."""
    context = browser.new_context()
    yield context
    context.close()

@pytest.fixture(scope="function")
def page(context: BrowserContext):
    """Create a new page for each test."""
    page = context.new_page()
    page.goto("https://app.turath.io/")
    yield page
    page.close()
