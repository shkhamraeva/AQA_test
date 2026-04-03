from playwright.sync_api import sync_playwright

URL = "https://the-internet.herokuapp.com/"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(URL)

    assert "the-internet" in page.title().lower()

    h1_text = page.locator("h1").inner_text()
    print(f"✅ Сайт доступен. Заголовок: {h1_text}")

    browser.close()
