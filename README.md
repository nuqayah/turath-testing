# Multi-Website Test Suite

This repository contains automated tests for multiple websites using Playwright and pytest:

- Nuqayah (https://nuqayah.com)
- Turath (https://app.turath.io)

## Setup

1. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
.\venv\Scripts\activate  # On Windows
```

2. Install dependencies:

```bash
# Install main dependencies
pip install .

# Install development dependencies (optional)
pip install ".[dev]"
```

3. Install Playwright browsers:

```bash
playwright install
```

## Running Tests

To run tests for a specific website:

```bash
# For Nuqayah
pytest --website=nuqayah

# For Turath
pytest --website=turath
```

Additional options:

- Run with HTML report:

```bash
pytest --website=nuqayah --html=report.html
```

- Run in headed mode (to see the browser):

```bash
pytest --website=nuqayah --headed
```

- Run a specific test:

```bash
pytest --website=nuqayah test_nuqayah.py::test_homepage_title
```

## Project Structure

- `conftest.py`: Contains shared fixtures and configuration for all websites
  - Website selection via `--website` parameter
  - Browser and page management
  - Automatic base URL navigation
- `test_nuqayah.py`: Test cases for Nuqayah website
- `test_turath.py`: Test cases for Turath website
- `pyproject.toml`: Project configuration and dependencies

## Test Coverage

### Nuqayah Website

- Homepage title verification
- Navigation links
- Project section content
- Social media links
- Contact section

### Turath Website

- [TODO: Add specific test coverage for Turath]

## Development

To run all code quality checks:

## Notes

- Tests are written in Arabic to match the website's content
- The browser is configured to use Arabic locale
- Each test automatically returns to the base URL after completion
