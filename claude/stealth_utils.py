# stealth_utils.py — Антидетект утилиты

import random
import time
import numpy as np
from claude.config import USER_AGENTS, VIEWPORTS, DELAY_BETWEEN_ACTIONS

def get_random_user_agent():
    """Случайный User-Agent"""
    return random.choice(USER_AGENTS)

def get_random_viewport():
    """Случайный размер окна"""
    return random.choice(VIEWPORTS)

def human_delay(min_sec=None, max_sec=None):
    """Задержка с нормальным распределением (как у человека)"""
    if min_sec is None:
        min_sec = DELAY_BETWEEN_ACTIONS[0]
    if max_sec is None:
        max_sec = DELAY_BETWEEN_ACTIONS[1]

    mean = (min_sec + max_sec) / 2
    std = (max_sec - min_sec) / 4
    delay = np.random.normal(mean, std)
    return max(min_sec, min(delay, max_sec))

def random_sleep(min_sec, max_sec):
    """Случайная пауза"""
    delay = human_delay(min_sec, max_sec)
    time.sleep(delay)
    return delay

def human_scroll(page, direction="down", steps=None):
    """Плавный скролл как человек"""
    if steps is None:
        steps = random.randint(3, 7)

    for _ in range(steps):
        scroll_amount = random.randint(200, 500)
        if direction == "up":
            scroll_amount = -scroll_amount

        page.mouse.wheel(0, scroll_amount)
        time.sleep(random.uniform(0.2, 0.6))

def human_mouse_move(page, x, y):
    """Движение мыши с человеческой траекторией"""
    # Текущая позиция (примерная)
    current_x = random.randint(100, 500)
    current_y = random.randint(100, 500)

    # Количество шагов
    steps = random.randint(5, 15)

    for i in range(steps):
        # Линейная интерполяция с небольшим шумом
        progress = (i + 1) / steps
        new_x = current_x + (x - current_x) * progress + random.randint(-5, 5)
        new_y = current_y + (y - current_y) * progress + random.randint(-5, 5)

        page.mouse.move(new_x, new_y)
        time.sleep(random.uniform(0.01, 0.05))

def apply_stealth(page):
    """Применить stealth настройки к странице"""
    # Скрыть webdriver
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });

        // Скрыть автоматизацию
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5]
        });

        // Скрыть языки
        Object.defineProperty(navigator, 'languages', {
            get: () => ['ru-RU', 'ru', 'en-US', 'en']
        });

        // Chrome runtime
        window.chrome = {
            runtime: {}
        };

        // Permissions
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
        );
    """)

def random_activity(page):
    """Случайная активность для имитации человека"""
    actions = [
        lambda: human_scroll(page, "down", random.randint(1, 3)),
        lambda: human_scroll(page, "up", random.randint(1, 2)),
        lambda: page.mouse.move(random.randint(100, 800), random.randint(100, 600)),
        lambda: time.sleep(random.uniform(0.5, 2)),
    ]

    # Выполнить 1-3 случайных действия
    for _ in range(random.randint(1, 3)):
        random.choice(actions)()
        time.sleep(random.uniform(0.3, 1))
