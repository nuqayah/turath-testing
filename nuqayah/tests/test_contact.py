from playwright.sync_api import Page, expect

def test_contact_section_visibility(page: Page, base_url: str):
    """Test that the contact section is present and contains expected elements."""
    page.goto(f"{base_url}/about")
    
    # Check for contact section
    contact_section = page.locator("span").filter(has_text="تواصل معنا")
    expect(contact_section).to_be_visible()
    
    # Check for email contact
    email_link = page.get_by_text("nuqayah@gmail.com")
    expect(email_link).to_be_visible()
    # Check for telegram contact
    expect(page.get_by_role("link", name="راسلنا على التليجرام")).to_be_visible()
    
    # Check for contact form fields
    expect(page.get_by_role("textbox", name="email@example.com")).to_be_visible()
    expect(page.get_by_role("textbox", name="الاسم")).to_be_visible()
    expect(page.get_by_role("textbox", name="الرسالة")).to_be_visible()
