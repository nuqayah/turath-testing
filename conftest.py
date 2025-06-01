import pytest
from playwright.sync_api import sync_playwright, Browser, Page

@pytest.fixture(scope="session")
def browser():
    """Create a browser instance that will be shared across all tests."""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture(scope="session")
def page(browser: Browser):
    """Create a single page for all tests in the session."""
    context = browser.new_context()
    page = context.new_page()
    yield page
    page.close()
    context.close()

@pytest.fixture(autouse=True)
def navigate_homepage(page: Page):
    """Automatically navigate to the homepage before each test."""
    page.goto("https://app.turath.io/")