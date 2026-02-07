from playwright.sync_api import sync_playwright
import time
import random
from storage import load_profiles, save_profiles

def parse_profiles(page, url: str):
    page.goto(url, wait_until="domcontentloaded")
    page.wait_for_timeout(random.uniform(2500, 4000))

    # ⛔ логин / ограничения
    if page.locator("input[name='session_key']").count() > 0:
        raise Exception("Not logged in")

    if "checkpoint" in page.url:
        raise Exception("Checkpoint / restricted")

    # 🔽 ОБЯЗАТЕЛЬНЫЙ СКРОЛЛ
    page.mouse.wheel(0, 600)
    page.wait_for_timeout(random.uniform(800, 1200))

    # ждём main, а не h1
    page.wait_for_selector("main", timeout=15000)
    main = page.locator("main")

    data = {"url": url}

    # ✅ NAME
    try:
        data["name"] = main.locator("h1").first.inner_text().strip()
    except:
        data["name"] = None

    # ✅ HEADLINE
    try:
        data["headline"] = main.locator("div.text-body-medium").first.inner_text().strip()
    except:
        data["headline"] = None

    # ✅ LOCATION
    location = None
    try:
        smalls = main.locator("span.text-body-small")
        for i in range(min(smalls.count(), 10)):
            txt = smalls.nth(i).inner_text().strip()
            low = txt.lower()

            if not txt:
                continue
            if "контакт" in low or "connections" in low or "уров" in low:
                continue
            if "," in txt or len(txt) > 4:
                location = txt
                break
    except:
        pass

    data["location"] = location

    return data





def main():
    profiles = load_profiles()  
    print(f"📦 Загружено профилей из JSON: {len(profiles)}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="storage_state.json")
        page = context.new_page()

        for profile in profiles:
            if profile["status"] != "new":
                continue
            url = profile["url"]
            print(f"🔍 Парсим профиль: {url}")

            try :
                profile_data = parse_profiles(page, url)
                profile["data"] = profile_data
                profile["status"] = "parsed"
                print(f"✅ Успешно спарсили: {url}")
            except Exception as e:
                profile["status"] = "error"
                profile["error"] = str(e)
                print(f"❌ Ошибка при парсинге {url}: {e}")
                save_profiles(profiles)
                continue

            save_profiles(profiles)
            time.sleep(random.uniform(5, 8))
        
        browser.close()


if __name__ == "__main__":
    main()