from playwright.sync_api import sync_playwright,expect

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

    page.goto(URL)
    current_url = navigate_to_example(page, "Checkboxes")
    checkboxes = page.locator("input[type='checkbox']")

    checkbox1 = checkboxes.first
    checkbox2 = checkboxes.nth(1)

    print(f"Checkbox 1: {checkbox1.is_checked()}")
    print(f"Checkbox 2: {checkbox2.is_checked()}")

    checkbox1.check()
    checkbox2.uncheck()

    print(f"✅ Checkbox 1: checked={checkbox1.is_checked()}")
    print(f"✅ Checkbox 2: checked={checkbox2.is_checked()}")

    page.goto(URL)
    navigate_to_example(page, "Dropdown")
    dropdown = page.locator("#dropdown")
    expect(dropdown).to_have_value("")

    dropdown.select_option(label="Option 1")
    expect(dropdown).to_have_value("1")

    dropdown.select_option(value="2")
    expect(dropdown).to_have_value("2")

    selected_text = page.locator("#dropdown option:checked").inner_text()
    print(f"✅ Выбрано: {selected_text}")

    browser.close()
