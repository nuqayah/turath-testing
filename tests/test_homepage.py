import re
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
        expect(child).to_contain_text(re.compile(r"\w*تراث\w*"))
        

def test_book_navigation(page: Page):
    """Test the book navigation functionality."""
    # Click on the first book link
    first_book_link = page.locator(".viewport a").first
    first_book_link.click()
    
    #check if the URL has changed to the book page
    expect(page).to_have_url(re.compile(r".*/book/\d+"))