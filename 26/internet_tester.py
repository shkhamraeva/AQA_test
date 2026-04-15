from pathlib import Path
from playwright.sync_api import sync_playwright,expect

URL = "https://the-internet.herokuapp.com/"

def navigate_to_example(page, example_name: str) -> str:
    page.locator(f"text={example_name}").click()
    return page.url

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=2000)
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


    page.goto(URL)
    navigate_to_example(page, "Inputs")
    input_number = page.locator("input[type='number']")
    input_number.fill("123")
    assert input_number.input_value() == "123"
    input_number.clear()
    input_number.fill("456")
    print(f"✅Введено: {input_number.input_value()}")


    page.goto(URL)
    page.get_by_role("link", name="Hovers").click()
    avatar = page.locator(".figure").first
    avatar.hover()
    tooltip = avatar.locator(".figcaption")
    expect(tooltip).to_be_visible()
    expect(tooltip).to_contain_text("name: user1")
    print(f"✅ Навели на изображение. Текст: name: user1")


    page.goto(URL)
    page.get_by_role("link", name="JavaScript Alerts").click()
    page.on("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Click for JS Alert").click()
    result = page.locator("#result")
    expect(result).to_have_text("You successfully clicked an alert")

    print(f"✅ Alert принят. Сообщение: You successfully clicked an alert")


    page.goto(URL)
    page.get_by_role("link", name="File Upload").click()
    test_file = Path("../test_upload.txt")
    test_file.write_text("Hello Playwright")
    page.locator("#file-upload").set_input_files(test_file)
    page.locator("#file-submit").click()
    uploaded = page.locator("#uploaded-files")
    expect(uploaded).to_have_text("test_upload.txt")

    print(f"✅ Файл загружен: test_upload.txt")

    page.goto(URL)
    page.get_by_role("link", name="Dynamic Loading").click()
    page.get_by_role("link", name="Example 1: Element on page that is hidden").click()
    page.get_by_role("button", name="Start").click()
    page.wait_for_selector("#finish h4")
    expect(page.locator("#finish h4")).to_have_text("Hello World!")

    print(f"✅ Элемент появился: Hello World!")

    browser.close()
