import pytest
from playwright.sync_api import sync_playwright, Browser
# from playwright.async_api import async_playwright

def pytest_addoption(parser):
    """Add command line options for website selection."""
    #pytest --website=<website_name(nuqayah or turath)>
    parser.addoption(
        "--website",
        action="store",
        default="nuqayah",
        help="Website to test: nuqayah or turath"
    )

@pytest.fixture(scope="session")
def base_url(request):
    """Return the base URL for the selected website."""
    website = request.config.getoption("--website")
    urls = {
        "nuqayah": "https://nuqayah.com",
        "turath": "https://app.turath.io"
    }
    if website not in urls:
        raise ValueError(f"Invalid website: {website}. Choose from: {', '.join(urls.keys())}")
    return urls[website]

@pytest.fixture(scope="session")
def browser():
    """Create a browser instance."""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture(scope="session")
def page(browser: Browser):
    """Create a new page for each test."""
    page = browser.new_page()
    yield page
    page.close()

@pytest.fixture(autouse=True)
def navigate_to_base_url(page, base_url):
    """Automatically navigate to base URL after each test."""
    yield
    page.goto(base_url)