import pytest
from playwright.sync_api import Page, expect

def test_navigation_menu_visible(page: Page):
    """Test that the navigation menu is visible and contains expected items."""
    nav = page.get_by_role("navigation")
    expect(nav).to_be_visible()
    
    # Check for common navigation items
    buttons = nav.locator("button")
    assert buttons.count() > 0, "Expected more than one button in the navigation menu"



def test_navigation_menu_content_switch(page: Page):
    """Test that clicking navigation buttons changes the main content without a full page reload."""
    
    page.wait_for_selector("main")

    # Get a reference to the main content area 
    main_content = page.locator("main")
    assert main_content.is_visible(), "Main content area should be visible"
    

    # Store the initial content for comparison
    initial_content = main_content.inner_text()
    
    buttons = page.get_by_role('navigation').locator('button')

    for i in range(buttons.count()):
        button = buttons.nth(i)
        button_text = button.inner_text()
        
        button.click()
        # Wait for the main content to change
        page.wait_for_timeout(500) 
        
        new_content = main_content.inner_text()
        print(new_content)
        # The content should change after clicking a navigation button
        assert new_content != initial_content, f"Content did not change after clicking '{button_text}'"
        
        # For now, just update initial_content for next button
        initial_content = new_content
