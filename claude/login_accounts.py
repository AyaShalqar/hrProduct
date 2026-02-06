# # login_accounts.py — Скрипт для сохранения сессий аккаунтов

# """
# Запусти этот скрипт для каждого аккаунта.
# Он откроет браузер, ты залогинишься вручную, и сессия сохранится.

# Использование:
#     python login_accounts.py account1
#     python login_accounts.py account2
#     python login_accounts.py account3
# """

# import sys
# import os
# from playwright.sync_api import sync_playwright

# def login_and_save(account_name):
#     os.makedirs("accounts", exist_ok=True)
#     storage_file = f"accounts/{account_name}_storage.json"

#     print("=" * 60)
#     print(f"🔐 СОХРАНЕНИЕ СЕССИИ: {account_name}")
#     print("=" * 60)
#     print()
#     print("1. Откроется браузер")
#     print("2. Залогинься в LinkedIn вручную")
#     print("3. После успешного входа нажми Enter в терминале")
#     print()
#     print("=" * 60)

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()

#         page.goto("https://www.linkedin.com/login")

#         input("\n✋ После логина нажми Enter для сохранения сессии...")

#         # Проверить что залогинились
#         if "feed" in page.url or "mynetwork" in page.url or "in/" in page.url:
#             context.storage_state(path=storage_file)
#             print(f"\n✅ Сессия сохранена: {storage_file}")
#         else:
#             # Попробовать сохранить в любом случае
#             context.storage_state(path=storage_file)
#             print(f"\n⚠️ Возможно не залогинен, но сессия сохранена: {storage_file}")

#         browser.close()

#     print("\n📋 Добавь в config.py:")
#     print(f'    "{storage_file}",')

# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Использование: python login_accounts.py <account_name>")
#         print("Пример: python login_accounts.py account1")
#         sys.exit(1)

#     account_name = sys.argv[1]
#     login_and_save(account_name)
