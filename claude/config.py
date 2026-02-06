# # config.py — Настройки парсера

# # ==================== АККАУНТЫ ====================
# # Файлы с сохранёнными сессиями (создать через login_accounts.py)
# ACCOUNTS = [
#     "accounts/account1_storage.json",
#     "accounts/account2_storage.json",
#     "accounts/account3_storage.json",
#     # Добавить больше аккаунтов для 10k/день
# ]

# # ==================== ПРОКСИ ====================
# # Формат: "http://user:pass@ip:port" или "http://ip:port"
# # ОБЯЗАТЕЛЬНО для 10k/день — без прокси забанят
# PROXIES = [
#     # "http://user:pass@proxy1.com:8080",
#     # "http://user:pass@proxy2.com:8080",
#     # Рекомендуется 5-10 резидентных прокси
# ]

# # ==================== ПОИСКОВЫЕ ЗАПРОСЫ ====================
# # Разбиваем на сегменты для безопасности
# SEARCH_SEGMENTS = [
#     {"query": "frontend developer", "location": "Казахстан"},
#     {"query": "frontend", "location": "Алматы"},
#     {"query": "frontend", "location": "Астана"},
#     {"query": "react developer", "location": "Казахстан"},
#     {"query": "vue developer", "location": "Казахстан"},
#     {"query": "javascript developer", "location": "Казахстан"},
#     # Добавить больше сегментов
# ]

# # ==================== ЛИМИТЫ ====================
# # Лимиты на аккаунт за сессию
# MAX_PAGES_PER_ACCOUNT = 100          # Страниц на аккаунт
# MAX_PROFILES_PER_ACCOUNT = 1000      # Профилей на аккаунт
# PROFILES_BEFORE_SWITCH = 200         # Профилей до смены аккаунта
# PROFILES_BEFORE_PROXY_SWITCH = 50    # Профилей до смены прокси

# # ==================== ЗАДЕРЖКИ (секунды) ====================
# DELAY_BETWEEN_PAGES = (8, 15)        # Между страницами
# DELAY_BETWEEN_ACTIONS = (1, 3)       # Между действиями
# DELAY_LONG_BREAK = (180, 300)        # Длинный перерыв (3-5 мин)
# DELAY_ACCOUNT_SWITCH = (300, 600)    # При смене аккаунта (5-10 мин)
# LONG_BREAK_CHANCE = 0.1              # 10% шанс длинного перерыва
# PROFILES_BEFORE_BREAK = (80, 120)    # Профилей до перерыва

# # ==================== ФАЙЛЫ ====================
# DATA_DIR = "data"
# PROFILES_FILE = "data/profiles.json"
# PROGRESS_FILE = "data/progress.json"
# ERRORS_LOG = "data/errors.log"

# # ==================== USER AGENTS ====================
# USER_AGENTS = [
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
# ]

# # ==================== VIEWPORTS ====================
# VIEWPORTS = [
#     {"width": 1920, "height": 1080},
#     {"width": 1366, "height": 768},
#     {"width": 1536, "height": 864},
#     {"width": 1440, "height": 900},
#     {"width": 1680, "height": 1050},
# ]
