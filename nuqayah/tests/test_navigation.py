from playwright.sync_api import Page, expect

nav_links = {
    "عن نقاية": "/about",
    "المدونة": "/blog",
    "الوثائق": "/docs",
    "ساهم الآن!": "/support",
    "شعار نقاية": ""
}
    
nav_buttons = [
    "المشاريع",
    "افتح القائمة الرئيسية"
]

def test_navigation_links(page: Page, base_url: str):
    """Test that main navigation links are present and clickable."""
    page.goto(base_url)
    # Check for main navigation links
    for link_text, _ in nav_links.items():
        link = page.get_by_role("banner").get_by_role("link", name=link_text)
        expect(link).to_be_visible()        
    # Check for main navigation buttons
    for button_text in nav_buttons:
        expect(page.get_by_role("button", name=button_text)).to_be_visible()

def test_links_interaction(page: Page, base_url: str):
    """Test that navigation menu items are clickable and lead to correct pages."""
    # Test clicking on each navigation link
    for link_text, expected_path in nav_links.items():
        if len(expected_path) > 0:
            link = page.get_by_role("banner").get_by_role("link", name=link_text)
            link.click()
            expect(page).to_have_url(f"{base_url}{expected_path}")
            page.go_back() 

def test_buttons_interaction(page: Page):
    """Test that navigation buttons are present and clickable."""
    
    page.get_by_role("button", name="المشاريع").click()
    expect(page.locator("#popover-default")).to_be_visible()
    
    # main_content = page.locator(".container")
    # page.get_by_role("button", name="افتح القائمة الرئيسية").click()
    # # expect(page.locator("[data-state='open']")).to_be_visible()
    # assert page.locator(".container").text_content() == main_content.text_content()
    
    # print(page.locator(".container").text_content())
    # print(main_content.text_content())