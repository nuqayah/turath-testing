import pytest,re
from playwright.sync_api import expect

def test_homepage_logo(page, base_url):
    """Test that the homepage loads with the logo."""
    page.goto(base_url)
    # Check if main logo is visible
    expect(page.locator("#logo-img")).to_be_visible()

def test_homepage_projects(page,base_url):
    """Test that the homepage projects load properly"""
    
    #check if the projects are visible
    projects = page.locator('#page-projects > ul > li')
    assert projects.count() > 0, "projects is not visible"
    
    #check if the projects routing is working properly
    for i in range(projects.count()):
        projects.nth(i).locator('a').click()
        page.wait_for_load_state('networkidle')
        expect(page).to_have_url(re.compile(rf"^{re.escape(base_url)}/projects/.+"))
        page.goto(base_url)
        
    
def test_homepage_donations(page, base_url):
    """Test that the homepage donations section loads properly"""
    
    # Check if the donations section is visible
    expect(page.locator('#support')).to_be_visible()
    
    # Check if the donations section has at least one donation option
    donation_options = page.locator('#support > a')
    assert donation_options.count() > 0, "No donation options are available"
    
        
def test_homepage_footer(page, base_url):
    """Test that the homepage footer loads properly"""
    
    # Check if the footer is visible
    expect(page.locator('footer')).to_be_visible()
    
    # Check if the footer has at least one link
    footer_links = page.locator('footer a')
    assert footer_links.count() > 0, "Footer has no links"
    
    # # Check if the footer links routing is working properly
    # for i in range(footer_links.count()):
    #     href = footer_links.nth(i).get_attribute("href")
    #     if href == base_url or href == "/" or href == base_url.rstrip("/"):
    #         continue  # Skip links that point to the base URL
    #     footer_links.nth(i).click()
    #     page.wait_for_load_state('networkidle')
    #     expect(page).to_have_url(re.compile(rf"^{re.escape(base_url)}(/.+)?$"))
    #     page.goto(base_url)
    
    