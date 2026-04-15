from pathlib import Path
from playwright.sync_api import sync_playwright, expect


def run_full_test():
    results = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=2000)
        page = browser.new_page()

        page.goto("https://the-internet.herokuapp.com/login")

        page.locator("#username").fill("tomsmith")
        page.locator("#password").fill("SuperSecretPassword!")
        page.locator("button[type='submit']").click()

        success_msg = page.locator("#flash")
        expect(success_msg).to_contain_text("You logged into a secure area!")

        page.screenshot(path="auth_success.png")
        results["form_auth"] = True


        page.goto("https://the-internet.herokuapp.com/checkboxes")
        checkboxes = page.locator("input[type='checkbox']")
        checkboxes.nth(0).check()
        checkboxes.nth(1).uncheck()

        page.screenshot(path="checkboxes_success.png")
        results["checkboxes"] = True


        page.goto("https://the-internet.herokuapp.com/dropdown")
        dropdown = page.locator("#dropdown")
        dropdown.select_option("2")

        expect(dropdown).to_have_value("2")

        page.screenshot(path="dropdown_success.png")
        results["dropdown"] = True

        page.goto("https://the-internet.herokuapp.com/inputs")
        input_field = page.locator("input")
        input_field.fill("999")
        expect(input_field).to_have_value("999")

        page.screenshot(path="inputs_success.png")
        results["inputs"] = True

        page.goto("https://the-internet.herokuapp.com/hovers")

        image_first = page.locator(".figure").first
        image_first.hover()

        caption = image_first.locator(".figcaption")
        expect(caption).to_be_visible()

        page.screenshot(path="hovers_success.png")
        results["hovers"] = True

        browser.close()

if __name__ == "__main__":
    run_full_test()
    print("📊 ОТЧЁТ:")
    print("✅ Form Authentication")
    print("✅ Checkboxes")
    print("✅ Dropdown")
    print("✅ Inputs")
    print("✅ Hovers")
    print("Все тесты пройдены!")