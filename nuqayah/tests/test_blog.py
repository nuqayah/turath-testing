from playwright.sync_api import Page, expect

def test_blogs(page: Page, base_url: str):
    """Test that the blog section is visible and contains expected content."""
    page.goto(f"{base_url}/blog")
    
    # Check for blog title
    expect(page.get_by_role("paragraph").get_by_text("المدونة")).to_be_visible()
    
    blog_cards = page.locator(".grid").first.locator('article')
    
    assert blog_cards.count() > 0, "Blog section is not present or empty"
    
    for i in range(blog_cards.count()):
        card = blog_cards.nth(i)
        
        # Click on the card
        card.click()
        
        # Get the href of the first <a> in the card
        card_link = card.locator("a").first.get_attribute("href")
        assert card_link is not None, "Card link href is None"
        # Check if the URL is correct
        expect(page).to_have_url(f"{base_url}/{card_link}")
        
        # Go back to the blog page
        page.go_back()
        