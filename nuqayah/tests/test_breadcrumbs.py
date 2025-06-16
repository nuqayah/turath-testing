from playwright.sync_api import Page

def test_breadcrumbs_visible_on_blog(page: Page, base_url: str):
    """Test that breadcrumbs are visible after navigating to the blog page."""
    page.goto(f"{base_url}/blog")
    # Check that breadcrumbs are visible 
    assert page.locator("[aria-label='شريط العنوان'] ol > li").count() > 0 , "Breadcrumbs are not visible"
    