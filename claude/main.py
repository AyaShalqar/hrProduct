# #!/usr/bin/env python3
# # main.py — Точка входа

# """
# LinkedIn Profile Collector
# ==========================

# Для 10,000 профилей в день нужно:
# 1. 3-5 аккаунтов LinkedIn
# 2. 5-10 резидентных прокси
# 3. Запуск на нескольких машинах параллельно

# Подготовка:
# -----------
# 1. pip install playwright numpy
# 2. playwright install chromium
# 3. python login_accounts.py account1
# 4. python login_accounts.py account2
# 5. Настроить config.py (аккаунты, прокси, сегменты)

# Запуск:
# -------
# python main.py              # Собрать 10,000 профилей
# python main.py --max 5000   # Собрать 5,000 профилей
# python main.py --stats      # Показать статистику
# python main.py --reset      # Сбросить прогресс
# """

# import argparse
# from collector import LinkedInCollector
# from storage import get_stats, reset_progress, load_profiles

# def show_stats():
#     """Показать статистику"""
#     stats = get_stats()
#     profiles = load_profiles()

#     print("=" * 60)
#     print("📊 СТАТИСТИКА")
#     print("=" * 60)
#     print(f"Всего профилей:      {stats['total_profiles']}")
#     print(f"Сегментов пройдено:  {stats['completed_segments']}")
#     print(f"Банов обнаружено:    {stats['bans_detected']}")
#     print(f"Последний запуск:    {stats['last_run'] or 'никогда'}")
#     print(f"Начат:               {stats['started_at'] or 'никогда'}")
#     print("=" * 60)

#     if profiles:
#         print("\nПоследние 5 профилей:")
#         for p in profiles[-5:]:
#             url = p["url"] if isinstance(p, dict) else p
#             print(f"  • {url}")

# def main():
#     parser = argparse.ArgumentParser(description="LinkedIn Profile Collector")
#     parser.add_argument("--max", type=int, default=10000, help="Максимум профилей")
#     parser.add_argument("--stats", action="store_true", help="Показать статистику")
#     parser.add_argument("--reset", action="store_true", help="Сбросить прогресс")

#     args = parser.parse_args()

#     if args.stats:
#         show_stats()
#         return

#     if args.reset:
#         confirm = input("⚠️ Сбросить прогресс? Профили сохранятся. (y/n): ")
#         if confirm.lower() == "y":
#             reset_progress()
#             print("✅ Прогресс сброшен")
#         return

#     # Запуск коллектора
#     collector = LinkedInCollector()
#     collector.run(max_profiles=args.max)

# if __name__ == "__main__":
#     main()
