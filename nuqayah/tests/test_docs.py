import re
from playwright.sync_api import Page, expect

def test_docs_page(page: Page, base_url: str):
    """Test that the docs page loads successfully and has expected content."""
    page.goto(f"{base_url}/docs")
    expect(page).to_have_url(f"{base_url}/docs")
    # Check for the docs heading
    expect(page.get_by_text("وثائق المشاريع")).to_be_visible()
    
    # Check that there are more than one <a> tags with href starting with "/docs/projects/"
    project_links = page.locator("a[href^='/docs/projects/']")
    assert project_links.count() > 1, "Expected more than one project link in docs page"
    
    # Check that each project link is routing correctly
    for i in range(project_links.count()):
        project_links.nth(i).click()
        expect(page).to_have_url(re.compile(rf"^{re.escape(base_url)}/docs/projects/.+"))
        page.go_back()
