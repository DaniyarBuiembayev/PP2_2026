import json
import os

DEFAULT_SETTINGS = {
    "sound": True,
    "difficulty": "normal",   
    "car_color": "default"   
}

SETTINGS_FILE    = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, encoding="utf-8") as f:
                data = json.load(f)
                for key, val in DEFAULT_SETTINGS.items():
                    if key not in data:
                        data[key] = val
                return data
        except:
            pass
    return DEFAULT_SETTINGS.copy()


def save_settings(settings: dict):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)



def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return []


def save_leaderboard(leaderboard: list):
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(leaderboard, f, ensure_ascii=False, indent=2)


def add_score(username: str, score: int, distance: int):
    leaderboard = load_leaderboard()
    leaderboard.append({
        "name":     username,
        "score":    score,
        "distance": distance
    })
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]
    save_leaderboard(leaderboard)
    return leaderboard