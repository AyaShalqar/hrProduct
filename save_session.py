from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Откроется LinkedIn
    page.goto("https://www.linkedin.com/login")

    print("👉 Войди в LinkedIn вручную и нажми Enter в терминале")
    input()

    # СОХРАНЯЕМ СЕССИЮ
    context.storage_state(path="storage_state.json")

    print("✅ Сессия сохранена в storage_state.json")

    browser.close()