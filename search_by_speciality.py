from playwright.sync_api import sync_playwright
import time
import random 
from storage import load_profiles, save_profiles
from profile_links import collect_profiles_links

SPECIALITY = "frontend"
LOCATION = "Казахстан"

with sync_playwright() as p:
    stored_profiles = load_profiles()
    print(f"📦 Загружено профилей из JSON: {len(stored_profiles)}")

    browser = p.chromium.launch(headless=False)
    context = browser.new_context(storage_state="storage_state.json")
    page = context.new_page()

    # 1️⃣ Открываем People search
    page.goto("https://www.linkedin.com/search/results/people/")
    page.wait_for_timeout(5000)



    # 3️⃣ Нажимаем All filters
    page.click("button:has-text('Все фильтры')")
    page.wait_for_timeout(1000)

    # 4️⃣ Ищем input локации
    location_checkbox = page.locator("div[role='checkbox']").filter(has_text=LOCATION)

    for i in range(location_checkbox.count()):
        text = location_checkbox.nth(i).inner_text()
        if text == LOCATION:
            location_checkbox.nth(i).click()
            print (f"✅ Фильтр применён: {SPECIALITY} + {LOCATION}")
            page.wait_for_timeout(3000)
            break



    submit_btn = page.locator('button[data-view-name="search-filter-all-filters-submit"]')
    submit_btn.wait_for(state="visible")
    page.wait_for_timeout(1000)
    submit_btn.click()

    page.wait_for_timeout(1000)

    search_input = page.locator("input[data-testid='typeahead-input']")
    search_input.click()
    search_input.fill(SPECIALITY)
    search_input.press("Enter")


    page.wait_for_timeout(1000)

    page_number = 1

    while True:
        print(f"Страница {page_number}")
        collect_profiles_links(page, stored_profiles)
        save_profiles(stored_profiles)

        next_button = page.get_by_test_id("pagination-controls-next-button-visible")
        next_button.scroll_into_view_if_needed()
        page.wait_for_timeout(2000)

        if next_button.is_visible() and next_button.is_enabled():
            print("Переходим на следующую страницу...")
            next_button.click()
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(3000)
            page_number += 1
            time.sleep(random.uniform(2, 4))
        else:
            print("Это была последняя страница результатов.")
            break

    browser.close()

