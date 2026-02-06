from playwright.sync_api import sync_playwright 
import time
import random


def collect_profiles_links(page, stored_profiles: set):
    profile_cards_locator = page.locator("div[data-view-name='people-search-result']")

    no_new_profiles_rounds = 0
    MAX_NO_NEW_ROUNDS = 3
    MAX_SCROLLS = 20
    scroll_count = 0

    while scroll_count < MAX_SCROLLS and no_new_profiles_rounds < MAX_NO_NEW_ROUNDS:
        before_count = len(stored_profiles)
        cards_count = profile_cards_locator.count()

        for i in range(cards_count):
            card = profile_cards_locator.nth(i)
            link = card.locator("a[href*='/in/']")

            if link.count() == 0:
                continue

            href = link.first.get_attribute("href")

            if href and href not in stored_profiles:
                if not any(p["url"] == href for p in stored_profiles):
                    stored_profiles.append({
                        "url": href,
                        "status": "new"
                    })
                    print("➕ Новый профиль:", href)
                else:
                    print("⏭ Уже есть:", href)
                print("➕ Новый профиль:", href)
                time.sleep(random.uniform(0.3, 0.8))
            else:
                print("⏭ Уже есть:", href)

        after_count = len(stored_profiles)

        if after_count == before_count:
            no_new_profiles_rounds += 1
        else:
            no_new_profiles_rounds = 0

        page.mouse.wheel(0, random.randint(800, 1600))
        time.sleep(random.uniform(1.2, 2.5))
        scroll_count += 1

    print(f"\n✅ Всего в базе профилей: {len(stored_profiles)}")
