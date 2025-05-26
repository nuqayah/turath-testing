import re
from playwright.sync_api import Page, expect

def test_authors_search(page: Page):
    """Test the search functionality on the authors page."""
    # Navigate to the authors page
    page.get_by_role("button", name="مؤلفون").click()
    
    # Fill in the search box with a specific author name
    page.get_by_role("textbox", name="أدخل اسم المؤلف").fill("الواحدي")
    
    # Check if the results contain the expected author name
    expect(page.locator(".result").first).to_contain_text("الواحدي")
    


def test_author_navigation(page: Page):
    """Test the author navigation functionality."""
    # Navigate to the authors page
    page.get_by_role("button", name="مؤلفون").click()
    
    # Check if the authors list is visible
    assert page.locator(".row").count() > 0, "Authors list is not visible"
    
    # Click on the first author link
    first_author_link = page.get_by_role("link").first
    first_author_name = first_author_link.text_content()
    first_author_link.click()
    
    # Check if the URL has changed to the author's page
    page.wait_for_url(re.compile(r".*/author/\d+"))
    expect(page).to_have_url(re.compile(r".*/author/\d+"))
    
    #Check if the author name is displayed on the page
    assert page.get_by_role("link", name=first_author_name).count() > 0, f"Author link '{first_author_name}' is not visible"

    