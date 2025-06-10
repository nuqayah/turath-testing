import pytest
from playwright.sync_api import expect

def test_project_section_visibility(page, base_url):
    """Test that the projects section is visible and contains expected content."""
    page.goto(base_url)
    
    # Check for project section
    project_section = page.get_by_text("المشاريع")
    expect(project_section).to_be_visible()
    
    # Check for some known projects
    known_projects = [
        "الباحث القرآني",
        "المقرئ",
        "التفسير التفاعلي",
        "الباحث الحديثي",
        "تراث",
        "تطبيق فائدة",
        "تكوين الراسخين",
        "القارئ",
        "المصحف المحفظ",
        "الباحث العلمي",
        "راوي"
    ]
    
    for project in known_projects:
        project_element = page.get_by_text(project)
        expect(project_element).to_be_visible()

def test_project_cards_interaction(page, base_url):
    """Test that project cards are interactive and contain expected elements."""
    page.goto(base_url)
    
    # Test a few project cards
    test_projects = [
        "الباحث القرآني",
        "المقرئ",
        "التفسير التفاعلي"
    ]
    
    for project_name in test_projects:
        # Find the project card
        project_card = page.get_by_text(project_name).first
        expect(project_card).to_be_visible()
        
        # Check if project has a logo
        project_logo = project_card.locator("xpath=..").get_by_role("img")
        expect(project_logo).to_be_visible()
        
        # Check if project has a description
        project_description = project_card.locator("xpath=..").get_by_role("paragraph")
        expect(project_description).to_be_visible() 