# storage.py — Сохранение и загрузка данных

import json
import os
from datetime import datetime
from claude.config import DATA_DIR, PROFILES_FILE, PROGRESS_FILE, ERRORS_LOG

def ensure_dirs():
    """Создать необходимые директории"""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs("accounts", exist_ok=True)

def load_profiles():
    """Загрузить собранные профили"""
    try:
        with open(PROFILES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_profiles(profiles):
    """Сохранить профили"""
    ensure_dirs()
    with open(PROFILES_FILE, "w", encoding="utf-8") as f:
        json.dump(profiles, f, ensure_ascii=False, indent=2)

def add_profiles(new_profiles):
    """Добавить новые профили (без дубликатов)"""
    existing = load_profiles()
    existing_urls = {p["url"] if isinstance(p, dict) else p for p in existing}

    added = 0
    for profile in new_profiles:
        url = profile["url"] if isinstance(profile, dict) else profile
        if url not in existing_urls:
            existing.append(profile)
            existing_urls.add(url)
            added += 1

    save_profiles(existing)
    return added

def load_progress():
    """Загрузить прогресс"""
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "completed_segments": [],
            "current_segment_index": 0,
            "current_page": 1,
            "total_profiles": 0,
            "current_account_index": 0,
            "profiles_this_account": 0,
            "profiles_this_proxy": 0,
            "current_proxy_index": 0,
            "last_run": None,
            "bans_detected": 0,
            "started_at": datetime.now().isoformat()
        }

def save_progress(progress):
    """Сохранить прогресс"""
    ensure_dirs()
    progress["last_run"] = datetime.now().isoformat()
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2)

def log_error(error_type, message, details=None):
    """Записать ошибку в лог"""
    ensure_dirs()
    timestamp = datetime.now().isoformat()
    log_entry = f"[{timestamp}] [{error_type}] {message}"
    if details:
        log_entry += f" | Details: {details}"
    log_entry += "\n"

    with open(ERRORS_LOG, "a", encoding="utf-8") as f:
        f.write(log_entry)

def get_stats():
    """Получить статистику"""
    profiles = load_profiles()
    progress = load_progress()

    return {
        "total_profiles": len(profiles),
        "completed_segments": len(progress.get("completed_segments", [])),
        "current_page": progress.get("current_page", 1),
        "bans_detected": progress.get("bans_detected", 0),
        "last_run": progress.get("last_run"),
        "started_at": progress.get("started_at")
    }

def reset_progress():
    """Сбросить прогресс (профили сохраняются)"""
    progress = {
        "completed_segments": [],
        "current_segment_index": 0,
        "current_page": 1,
        "total_profiles": len(load_profiles()),
        "current_account_index": 0,
        "profiles_this_account": 0,
        "profiles_this_proxy": 0,
        "current_proxy_index": 0,
        "last_run": None,
        "bans_detected": 0,
        "started_at": datetime.now().isoformat()
    }
    save_progress(progress)
    return progress
