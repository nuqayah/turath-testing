import re
import pytest
from playwright.sync_api import Page, expect

def test_homepage_title(page: Page):
    """Test that the homepage loads with the correct title."""
    expect(page).to_have_title("تراث")

def test_homepage_loaded(page: Page):
    """Test that the homepage loads successfully."""
    # Wait for the main content to be visible
    page.wait_for_selector("main")
    
    # Check if the main navigation is present
    expect(page.locator("nav")).to_be_visible()
    
    # Check if the search bar is present
    expect(page.get_by_role("textbox", name="أدخل اسم الكتاب")).to_be_visible()

def test_search_functionality(page: Page):
    """Test the basic search functionality."""
    # Type in the search box
    page.get_by_role("textbox", name="أدخل اسم الكتاب").fill("تراث")
    
    # Get all child elements of the .viewport container
    child_viewports = page.locator(".viewport > *").first
    
    for i in range(min(10, child_viewports.count())):
        child = child_viewports.nth(i)
        print(child.text_content())
        expect(child).to_contain_text(re.compile(r"\w*تراث\w*"))