import re
from playwright.sync_api import Page, expect

url = "https://app.turath.io/book/25"

def test_book_page(page: Page):
    """Test that a random book page loads successfully."""
    page.goto(url)
    
    # Check if the URL matches the expected pattern
    page.wait_for_url(re.compile(rf".*/book/25"))
    expect(page).to_have_url(re.compile(rf".*/book/25"))
    
    # Check if the book is opened correctly
    expect(page.locator(".reader-cont")).to_be_visible()
    expect(page.locator("#toc")).to_be_visible()
    
    # Check if the TOC is containes items
    expect(page.get_by_role("button", name="المحتويات")).to_be_visible()
    expect(page.get_by_role("button", name="البحث")).to_be_visible()
    expect(page.get_by_role("button", name="المفضلة")).to_be_visible()
    expect(page.get_by_role("button", name="السجل")).to_be_visible()
    
    # Check if the book has pages
    pages = page.locator(".viewport > .page")
    pages.first.wait_for(state="visible")
    assert pages.count() > 0, "No pages found in the book"
    
def test_toc_search(page: Page):
    """Test that the table of contents is visible and contains items."""
    page.goto(url)
    
    #Check that test feature is working correctly
    page.get_by_role("button", name="البحث").click()
    page.locator(".toc-search").fill("الفصل")
    
    page.wait_for_timeout(1000)  # Wait for search results to appear
    
    #check that search results are highlighted and contain the expected text
    results = page.locator("mark")
    if results.count() > 0:
        for i in range(min(10,results.count())):
            expect(results.nth(i)).to_have_text(re.compile(r"الفصل"))
    

def test_toc_favourites(page: Page):
    """Test that the table of contents is visible and contains items."""
    page.goto(url)
    
    #Check that test feature is working correctly
    page.get_by_role("button", name="المفضلة").click()
    
    #Add the first page to favourites
    page.locator(".page").first.dblclick()
    
    # Check that the page is added to favourites
    page_no = page.locator(".page").first.locator('.page-no').text_content()
    favourites = page.locator(".favorites li")
    flag = False
    
    for i in range(favourites.count()):
        fav_text = favourites.nth(i).text_content()
        if page_no is not None and fav_text is not None and page_no in fav_text:
            flag = True
            break
    
    assert flag, "The current page is not added to favourites"