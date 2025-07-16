import pytest
from playwright.sync_api import Page
from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError

#fixture pro odmítnutí cookies
def reject_cookies(page: Page):
    try:
        page.wait_for_selector("#didomi-notice-learn-more-button", timeout = 5000)
        page.locator("#didomi-notice-learn-more-button").click()
        page.wait_for_selector("#btn-toggle-disagree", timeout=5000)
        page.locator("#btn-toggle-disagree").click()
    except TimeoutError:
        pass

#fixture pro browser - 3 různé enginy
@pytest.fixture(params=["chromium", "firefox", "webkit"])
def browser(request):
    with sync_playwright() as playwright:
        browser = getattr(playwright, request.param).launch()   #v případě potřeby .launch(headless=False, slow_mo=1000)                           
        yield browser
        browser.close()

@pytest.fixture()
def page(browser):
    page = browser.new_page()
    yield page
    page.close()

#fixture pro automatické otevření testované stránky a odmítnutí cookies před každým testem
@pytest.fixture(autouse=True)
def setup(page: Page):
    page.goto("https://www.cbdb.cz/")
    reject_cookies(page)

