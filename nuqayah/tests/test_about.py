from playwright.sync_api import Page, expect

def test_FAQ(page: Page, base_url: str):
    """Test that the about page loads successfully and has expected content."""
    page.goto(f"{base_url}/about")
    expect(page).to_have_url(f"{base_url}/about")
    
    # Check for the logo image
    expect(page.locator("#logo-img")).to_be_visible()
    
    # check for the FAQ section
    expect(page.locator("#faq")).to_be_visible()
    
    # check if the FAQ section has items
    assert page.locator("[data-melt-accordion-item]").count() > 0, "FAQ section is not present or empty"


def test_stats(page: Page, base_url: str):
    """Test that the about page contains a team or contributors section if present."""
    page.goto(f"{base_url}/about")
    # check for the title of stats section
    expect(page.get_by_text("الإحصائيات")).to_be_visible()
    
    # check if the stats section is visible
    expect(page.locator(".layercake-container")).to_be_visible()

def test_contact(page: Page, base_url: str):
    """Test that the contact section is present and contains expected elements."""
    page.goto(f"{base_url}/about")
    
    # Check for contact title
    expect(page.locator("span").filter(has_text="تواصل معنا")).to_be_visible()
    
    # Check for contact section
    expect(page.locator("#contact")).to_be_visible()