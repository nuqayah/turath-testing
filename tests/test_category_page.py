import re
from playwright.sync_api import Page, expect

def test_category_navigation(page: Page):
    """Test the category navigation functionality."""
    # Navigate to the categories page
    page.get_by_role("button", name="أقسام").click()
    
    # Check if the categories list is visible
    assert page.locator(".category-item").count() > 0, "Categories list is not visible"
    
      # Check if the URL has changed to the category page
    page.wait_for_url(re.compile(r".*/category/\d+"))
    expect(page).to_have_url(re.compile(r".*/category/\d+"))
    
    
    # Click on the first category link
    # first_category_link = page.get_by_role("link").first
    # first_category_name = first_category_link.text_content()
    # first_category_link.click()
    # if first_category_name:
    #     cleaned_first_category_name = re.sub(r"[^\u0621-\u064Aa-zA-Z]+", "", first_category_name) 
        
        
        # assert page.get_by_role("link", name=cleaned_first_category_name).count() > 0, f"Category link '{cleaned_first_category_name}' is not visible"
        
        #Get the results info
        # results_info = page.locator("div").filter(has_text=re.compile(rf"\w*{re.escape(cleaned_first_category_name)}\w*")).get_by_role("link")
        
        # print(f"Results count: {results_info.count()}")
    
        # # Check if the results contain the expected category name
        # if results_info.count() > 0:
        #     for i in range(min(10,results_info.count())):
        #         result = results_info.nth(i)
        #         print(result.text_content())
        #         expect(result).to_contain_text(re.compile(rf"\w*{re.escape(cleaned_first_category_name)}\w*"))