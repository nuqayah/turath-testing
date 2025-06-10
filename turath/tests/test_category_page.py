import re
from playwright.sync_api import Page, expect

def test_category_navigation(page: Page):
    """Test the category navigation functionality."""
    # Navigate to the categories page
    page.get_by_role("button", name="أقسام").click()
    # Check if the categories list is visible
    assert page.locator(".category-item").count() > 0, "Categories list is not visible"
    
    
    # Click on the first category link
    first_category_link = page.get_by_role("link").first
    first_category_name = first_category_link.text_content()
    first_category_link.click()
    
    # Check if the URL has changed to the category page
    page.wait_for_url(re.compile(r".*/category/\d+"))
    expect(page).to_have_url(re.compile(r".*/category/\d+"))
    expect(page.locator(".items-baseline > b")).to_be_visible()
  
    if first_category_name:
        cleaned_first_category_name = re.sub(r"[^\u0621-\u064Aa-zA-Z]+", "", first_category_name) 
        #Get the results info
        results_info = page.locator('.book-item:visible .info > div > a[href*="category"]')
        
        # Check if the results contain the expected category name
        if results_info.count() > 0:
            for i in range(results_info.count()):
                result = results_info.nth(i)
                expect(result).to_contain_text(re.compile(rf"\w*{re.escape(cleaned_first_category_name)}\w*"))