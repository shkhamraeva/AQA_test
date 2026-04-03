from playwright.sync_api import sync_playwright

URL = "https://the-internet.herokuapp.com/"

def navigate_to_example(page, example_name: str) -> str:
    page.locator(f"text={example_name}").click()
    return page.url

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(URL)

    h1_text = page.locator("h1").inner_text()
    assert "the-internet" in h1_text.lower()
    print(f"✅ Сайт доступен. Заголовок: {h1_text}")

    current_url = navigate_to_example(page, "Form Authentication")

    assert "/login" in current_url, "Не тот URL"
    print(f"Перешли в: Form Authentication | URL: {current_url}")

    page.locator("#username").fill("tomsmith")
    page.locator("#password").fill("SuperSecretPassword!")

    page.get_by_role("button", name="Login").click()
    assert "/secure" in page.url, "Не тот URL"
    print(f"✅ Успешный вход! URL: {page.url}")

    page.get_by_role("link", name="Logout").click()
    assert "/login" in page.url
    print(f"✅ Успешный выход! URL: {page.url}")

    browser.close()
