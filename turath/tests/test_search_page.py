import re
from playwright.sync_api import Page, expect

def test_filters(page: Page):
    """Test the filtering functionality on the search results."""
    
    results = page.locator(".search-results")
    
    # Navigate to the search page
    page.get_by_role("button", name="بحث").click()
    page.get_by_role("textbox", name="كلمات البحث").fill("أبي هريرة")
    page.get_by_role("button", name="تصفية البحث").click()
    
    # Check if results contain the expected text
    if results.count() > 0:
        for i in range(results.count()):
            expect(results.nth(i)).to_contain_text("أبي هريرة")
    
    # Apply book filters
    page.get_by_role("button", name="الكتاب").click()
    page.get_by_role("button", name="أسماء المدلسين").click()
    page.get_by_role("button", name="دروس للشيخ عطية سالم").click()
    page.get_by_role("button", name="عرض خيارات التصفية").click()
    
    # Check if the results are filtered properly
    results = page.locator(".search-results")
    if results.count() > 0:
        for i in range(results.count()):
            expect(results.nth(i)).to_have_text(re.compile(r"أسماء المدلسين|دروس للشيخ عطية سالم"))
    
    # Remove filters and perform another search
    page.get_by_role("button", name="إزالة التصفية").click()
    page.get_by_role("textbox", name="كلمات البحث").fill("الحديث")
    page.get_by_role("button", name="تصفية البحث").click()
    
    # Apply author filter
    page.get_by_role("button", name="المؤلف").click()
    page.get_by_role("button", name="الواحدي").click()
    page.get_by_role("button", name="البغوي، أبو محمد").click()
    page.get_by_role("button", name="عرض خيارات التصفية").click()
    
    # Check if the results are filtered properly
    if results.count() > 0:
        for i in range(results.count()):
            expect(results.nth(i)).to_have_text(re.compile(r"الواحدي|البغوي، أبو محمد"))
    
    # Remove filters and perform another search
    page.get_by_role("button", name="إزالة التصفية").click()
    page.get_by_role("textbox", name="كلمات البحث").fill("الاجماع")
    page.get_by_role("button", name="تصفية البحث").click()
    
    # Filter by date of death
    page.get_by_role("button", name="تاريخ الوفاة").click()
    page.get_by_role("textbox", name="البدأ").click()
    page.get_by_role("textbox", name="البدأ").fill("٢٠0")
    page.get_by_role("textbox", name="النهاية").click()
    page.get_by_role("textbox", name="النهاية").fill("٣٠0")
    
    # Check if the results are filtered properly  
    if results.count() > 0:
        for i in range(results.count()):
            expect(results.nth(i).locator(".book-link").first).to_have_text(re.compile(r"٢[٠-٩]{2}|٣٠٠"))