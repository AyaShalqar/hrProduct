import json
import os
import time
import random
from playwright.sync_api import sync_playwright
from PIL import Image

SCREENSHOTS_DIR = "screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)


def wait_full_load(page):
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_load_state("networkidle")
    time.sleep(3)


def scroll_until_loaded(page, max_attempts=20):
    """Скроллит до полной подгрузки LinkedIn"""
    last_height = 0
    attempts = 0

    while attempts < max_attempts:
        current_height = page.evaluate(
            "document.scrollingElement.scrollHeight"
        )

        if current_height == last_height:
            break

        page.evaluate(
            "window.scrollTo(0, document.scrollingElement.scrollHeight)"
        )

        time.sleep(random.uniform(2, 3))

        last_height = current_height
        attempts += 1


def capture_by_viewport(page, profile_name):
    screenshots = []

    viewport_height = page.viewport_size["height"]
    total_height = page.evaluate(
        "document.scrollingElement.scrollHeight"
    )

    position = 0
    index = 0

    while position < total_height:
        page.evaluate(f"window.scrollTo(0, {position})")
        time.sleep(1)

        path = f"{SCREENSHOTS_DIR}/{profile_name}_{index}.png"
        page.screenshot(path=path)
        screenshots.append(path)

        position += viewport_height
        index += 1

    return screenshots


def stitch_images(image_paths, output_path):
    images = [Image.open(p) for p in image_paths]

    total_height = sum(img.height for img in images)
    max_width = max(img.width for img in images)

    final_image = Image.new("RGB", (max_width, total_height))

    y = 0
    for img in images:
        final_image.paste(img, (0, y))
        y += img.height

    final_image.save(output_path)

    for p in image_paths:
        os.remove(p)


def process_profiles():
    with open("profiles.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--start-maximized"]
        )

        context = browser.new_context(
            storage_state="storage_state.json",
            viewport={"width": 1280, "height": 900}
        )

        page = context.new_page()

        for profile in data["profiles"]:
            if profile["status"] not in ["new", "error"]:
                continue

            try:
                print("Processing:", profile["url"])

                page.goto(profile["url"], timeout=60000)
                wait_full_load(page)

                # Проверка авторизации
                if "login" in page.url:
                    print("❌ Not authorized")
                    profile["status"] = "error"
                    continue

                # Прогружаем lazy load
                scroll_until_loaded(page)

                profile_name = profile["url"].strip("/").split("/")[-1]

                chunks = capture_by_viewport(page, profile_name)

                final_path = f"{SCREENSHOTS_DIR}/{profile_name}_full.png"
                stitch_images(chunks, final_path)

                profile["status"] = "done"
                print("✅ Done:", profile_name)

                time.sleep(random.uniform(3, 6))

            except Exception as e:
                print("❌ Error:", e)
                profile["status"] = "error"

        browser.close()

    with open("profiles.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    process_profiles()
