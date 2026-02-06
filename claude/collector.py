# # collector.py — Основная логика сбора профилей

# import random
# import time
# from datetime import datetime
# from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# from config import (
#     ACCOUNTS, PROXIES, SEARCH_SEGMENTS,
#     MAX_PAGES_PER_ACCOUNT, PROFILES_BEFORE_SWITCH,
#     PROFILES_BEFORE_PROXY_SWITCH, DELAY_BETWEEN_PAGES,
#     DELAY_LONG_BREAK, DELAY_ACCOUNT_SWITCH, LONG_BREAK_CHANCE,
#     PROFILES_BEFORE_BREAK
# )
# from stealth_utils import (
#     get_random_user_agent, get_random_viewport,
#     random_sleep, human_scroll, apply_stealth, random_activity
# )
# from storage import (
#     load_progress, save_progress, add_profiles, log_error, get_stats
# )


# class LinkedInCollector:
#     def __init__(self):
#         self.progress = load_progress()
#         self.playwright = None
#         self.browser = None
#         self.context = None
#         self.page = None
#         self.profiles_since_break = 0

#     def get_current_account(self):
#         """Получить текущий аккаунт"""
#         if not ACCOUNTS:
#             raise ValueError("Нет аккаунтов в config.py!")
#         index = self.progress["current_account_index"] % len(ACCOUNTS)
#         return ACCOUNTS[index]

#     def get_current_proxy(self):
#         """Получить текущий прокси"""
#         if not PROXIES:
#             return None
#         index = self.progress["current_proxy_index"] % len(PROXIES)
#         return PROXIES[index]

#     def switch_account(self):
#         """Переключить на следующий аккаунт"""
#         self.progress["current_account_index"] += 1
#         self.progress["profiles_this_account"] = 0
#         save_progress(self.progress)

#         print(f"\n🔄 Смена аккаунта на: {self.get_current_account()}")
#         print(f"⏳ Пауза {DELAY_ACCOUNT_SWITCH[0]//60}-{DELAY_ACCOUNT_SWITCH[1]//60} мин...")
#         random_sleep(DELAY_ACCOUNT_SWITCH[0], DELAY_ACCOUNT_SWITCH[1])

#     def switch_proxy(self):
#         """Переключить на следующий прокси"""
#         if not PROXIES:
#             return

#         self.progress["current_proxy_index"] += 1
#         self.progress["profiles_this_proxy"] = 0
#         save_progress(self.progress)

#         print(f"🔄 Смена прокси на: {self.get_current_proxy()}")

#     def create_browser(self):
#         """Создать браузер с текущими настройками"""
#         if self.browser:
#             try:
#                 self.browser.close()
#             except:
#                 pass

#         proxy = self.get_current_proxy()
#         launch_options = {"headless": False}

#         if proxy:
#             launch_options["proxy"] = {"server": proxy}

#         self.browser = self.playwright.chromium.launch(**launch_options)

#         # Создать контекст с рандомными параметрами
#         account_file = self.get_current_account()
#         viewport = get_random_viewport()
#         user_agent = get_random_user_agent()

#         try:
#             self.context = self.browser.new_context(
#                 storage_state=account_file,
#                 viewport=viewport,
#                 user_agent=user_agent
#             )
#         except FileNotFoundError:
#             print(f"❌ Файл аккаунта не найден: {account_file}")
#             print("Запусти login_accounts.py для создания сессий")
#             raise

#         self.page = self.context.new_page()
#         apply_stealth(self.page)

#         print(f"✅ Браузер создан | Аккаунт: {account_file} | Прокси: {proxy or 'нет'}")

#     def check_for_ban(self):
#         """Проверка на бан/капчу"""
#         try:
#             # Капча
#             if self.page.locator("text=security verification").is_visible(timeout=1000):
#                 return "CAPTCHA"

#             if self.page.locator("text=Let's do a quick security check").is_visible(timeout=1000):
#                 return "CAPTCHA"

#             # Ограничение поиска
#             if self.page.locator("text=reached the commercial use limit").is_visible(timeout=1000):
#                 return "COMMERCIAL_LIMIT"

#             if self.page.locator("text=You've reached the search limit").is_visible(timeout=1000):
#                 return "SEARCH_LIMIT"

#             # Challenge
#             if "challenge" in self.page.url:
#                 return "CHALLENGE"

#             # Unusual activity
#             if self.page.locator("text=unusual activity").is_visible(timeout=1000):
#                 return "SUSPICIOUS"

#         except PlaywrightTimeout:
#             pass
#         except Exception as e:
#             log_error("BAN_CHECK", str(e))

#         return None

#     def handle_ban(self, ban_type):
#         """Обработка бана"""
#         print(f"\n⚠️ ОБНАРУЖЕН БАН: {ban_type}")
#         log_error("BAN", ban_type, {"account": self.get_current_account()})

#         self.progress["bans_detected"] += 1
#         save_progress(self.progress)

#         if ban_type in ["CAPTCHA", "CHALLENGE", "SUSPICIOUS"]:
#             # Нужно решить капчу вручную или сменить аккаунт
#             print("🛑 Требуется ручное вмешательство или смена аккаунта")
#             self.switch_account()
#             return "switch_account"

#         elif ban_type in ["SEARCH_LIMIT", "COMMERCIAL_LIMIT"]:
#             # Лимит поиска — ждать или сменить аккаунт
#             print("🛑 Достигнут лимит поиска")
#             self.switch_account()
#             return "switch_account"

#         return "continue"

#     def collect_profiles_from_page(self):
#         """Собрать профили с текущей страницы"""
#         profiles = []

#         try:
#             # Скролл для загрузки всех профилей
#             human_scroll(self.page, "down", random.randint(3, 5))
#             random_sleep(1, 2)
#             human_scroll(self.page, "down", random.randint(2, 4))
#             random_sleep(1, 2)

#             # Найти все ссылки на профили
#             links = self.page.locator('a[href*="/in/"]').all()

#             seen_urls = set()
#             for link in links:
#                 try:
#                     href = link.get_attribute("href")
#                     if href and "/in/" in href and href not in seen_urls:
#                         # Очистить URL
#                         url = href.split("?")[0]
#                         if not url.endswith("/"):
#                             url += "/"

#                         if url not in seen_urls:
#                             seen_urls.add(url)
#                             profiles.append({
#                                 "url": url,
#                                 "collected_at": datetime.now().isoformat()
#                             })
#                 except:
#                     continue

#         except Exception as e:
#             log_error("COLLECT", str(e))

#         return profiles

#     def go_to_next_page(self):
#         """Перейти на следующую страницу"""
#         try:
#             next_button = self.page.get_by_test_id("pagination-controls-next-button-visible")
#             next_button.scroll_into_view_if_needed()
#             random_sleep(1, 2)

#             if next_button.is_visible() and next_button.is_enabled():
#                 # Случайная активность перед кликом
#                 if random.random() < 0.3:
#                     random_activity(self.page)

#                 next_button.click()
#                 self.page.wait_for_load_state("domcontentloaded")
#                 random_sleep(2, 4)
#                 return True
#             else:
#                 return False

#         except Exception as e:
#             log_error("NEXT_PAGE", str(e))
#             return False

#     def search_segment(self, segment):
#         """Выполнить поиск по сегменту"""
#         query = segment["query"]
#         location = segment["location"]

#         print(f"\n🔍 Поиск: '{query}' в '{location}'")

#         try:
#             # Открыть страницу поиска
#             self.page.goto("https://www.linkedin.com/search/results/people/")
#             random_sleep(3, 5)

#             # Проверка на бан
#             ban = self.check_for_ban()
#             if ban:
#                 return self.handle_ban(ban)

#             # Открыть фильтры
#             self.page.click("button:has-text('Все фильтры')")
#             random_sleep(1, 2)

#             # Выбрать локацию
#             location_checkbox = self.page.locator("div[role='checkbox']").filter(has_text=location)
#             for i in range(location_checkbox.count()):
#                 text = location_checkbox.nth(i).inner_text()
#                 if text == location:
#                     location_checkbox.nth(i).click()
#                     random_sleep(1, 2)
#                     break

#             # Применить фильтры
#             submit_btn = self.page.locator('button[data-view-name="search-filter-all-filters-submit"]')
#             submit_btn.wait_for(state="visible")
#             random_sleep(0.5, 1)
#             submit_btn.click()
#             random_sleep(2, 3)

#             # Ввести поисковый запрос
#             search_input = self.page.locator("input[data-testid='typeahead-input']")
#             search_input.click()
#             random_sleep(0.5, 1)

#             # Печатать как человек (по символам)
#             for char in query:
#                 search_input.type(char, delay=random.randint(50, 150))

#             random_sleep(0.5, 1)
#             search_input.press("Enter")
#             random_sleep(3, 5)

#             return "success"

#         except Exception as e:
#             log_error("SEARCH", str(e), segment)
#             return "error"

#     def maybe_take_break(self):
#         """Возможно сделать перерыв"""
#         # Длинный перерыв с некоторой вероятностью
#         if random.random() < LONG_BREAK_CHANCE:
#             print(f"\n☕ Случайный перерыв...")
#             random_sleep(DELAY_LONG_BREAK[0], DELAY_LONG_BREAK[1])
#             return

#         # Перерыв после N профилей
#         break_threshold = random.randint(PROFILES_BEFORE_BREAK[0], PROFILES_BEFORE_BREAK[1])
#         if self.profiles_since_break >= break_threshold:
#             print(f"\n☕ Перерыв после {self.profiles_since_break} профилей...")
#             random_sleep(DELAY_LONG_BREAK[0], DELAY_LONG_BREAK[1])
#             self.profiles_since_break = 0

#     def maybe_switch_proxy(self):
#         """Возможно сменить прокси"""
#         if not PROXIES:
#             return False

#         if self.progress["profiles_this_proxy"] >= PROFILES_BEFORE_PROXY_SWITCH:
#             self.switch_proxy()
#             return True
#         return False

#     def maybe_switch_account(self):
#         """Возможно сменить аккаунт"""
#         if self.progress["profiles_this_account"] >= PROFILES_BEFORE_SWITCH:
#             self.switch_account()
#             return True
#         return False

#     def run(self, max_profiles=10000):
#         """Основной цикл сбора"""
#         print("=" * 60)
#         print("🚀 ЗАПУСК LINKEDIN COLLECTOR")
#         print("=" * 60)

#         stats = get_stats()
#         print(f"📊 Уже собрано: {stats['total_profiles']} профилей")
#         print(f"🎯 Цель: {max_profiles} профилей")
#         print("=" * 60)

#         with sync_playwright() as p:
#             self.playwright = p

#             try:
#                 self.create_browser()

#                 # Основной цикл по сегментам
#                 while self.progress["total_profiles"] < max_profiles:

#                     # Проверить нужно ли сменить аккаунт/прокси
#                     if self.maybe_switch_account():
#                         self.create_browser()

#                     if self.maybe_switch_proxy():
#                         self.create_browser()

#                     # Получить текущий сегмент
#                     segment_index = self.progress["current_segment_index"]
#                     if segment_index >= len(SEARCH_SEGMENTS):
#                         # Все сегменты пройдены, начать сначала
#                         segment_index = 0
#                         self.progress["current_segment_index"] = 0

#                     segment = SEARCH_SEGMENTS[segment_index]

#                     # Выполнить поиск
#                     result = self.search_segment(segment)

#                     if result == "switch_account":
#                         self.create_browser()
#                         continue
#                     elif result == "error":
#                         random_sleep(30, 60)
#                         continue

#                     # Сбор страниц
#                     page_num = 1
#                     while page_num <= MAX_PAGES_PER_ACCOUNT:

#                         # Проверка на бан
#                         ban = self.check_for_ban()
#                         if ban:
#                             result = self.handle_ban(ban)
#                             if result == "switch_account":
#                                 self.create_browser()
#                                 break

#                         # Собрать профили
#                         profiles = self.collect_profiles_from_page()
#                         added = add_profiles(profiles)

#                         # Обновить счётчики
#                         self.progress["total_profiles"] += added
#                         self.progress["profiles_this_account"] += added
#                         self.progress["profiles_this_proxy"] += added
#                         self.progress["current_page"] = page_num
#                         self.profiles_since_break += added
#                         save_progress(self.progress)

#                         print(f"📄 Страница {page_num} | +{added} профилей | Всего: {self.progress['total_profiles']}")

#                         # Проверить достигнута ли цель
#                         if self.progress["total_profiles"] >= max_profiles:
#                             print(f"\n🎉 ЦЕЛЬ ДОСТИГНУТА: {max_profiles} профилей!")
#                             return

#                         # Возможно сделать перерыв
#                         self.maybe_take_break()

#                         # Проверить лимиты
#                         if self.maybe_switch_account():
#                             self.create_browser()
#                             break

#                         if self.maybe_switch_proxy():
#                             self.create_browser()
#                             break

#                         # Перейти на следующую страницу
#                         random_sleep(DELAY_BETWEEN_PAGES[0], DELAY_BETWEEN_PAGES[1])

#                         if not self.go_to_next_page():
#                             print("📍 Конец результатов поиска")
#                             break

#                         page_num += 1

#                     # Сегмент завершён
#                     self.progress["completed_segments"].append(segment)
#                     self.progress["current_segment_index"] += 1
#                     self.progress["current_page"] = 1
#                     save_progress(self.progress)

#                     print(f"\n✅ Сегмент '{segment['query']}' завершён")
#                     random_sleep(60, 120)  # Пауза между сегментами

#             except KeyboardInterrupt:
#                 print("\n\n⚠️ Остановлено пользователем")
#                 save_progress(self.progress)

#             except Exception as e:
#                 print(f"\n❌ Ошибка: {e}")
#                 log_error("FATAL", str(e))
#                 save_progress(self.progress)

#             finally:
#                 if self.browser:
#                     self.browser.close()

#         # Финальная статистика
#         stats = get_stats()
#         print("\n" + "=" * 60)
#         print("📊 ИТОГОВАЯ СТАТИСТИКА")
#         print("=" * 60)
#         print(f"Всего собрано: {stats['total_profiles']} профилей")
#         print(f"Сегментов пройдено: {stats['completed_segments']}")
#         print(f"Банов обнаружено: {stats['bans_detected']}")
#         print("=" * 60)
