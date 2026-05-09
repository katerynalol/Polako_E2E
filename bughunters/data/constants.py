import os
from dotenv import load_dotenv


load_dotenv()

BASE_URL = "https://stg-client.polakohedonist.club"
LANG = "ru"

URLS = {
    "home":           f"{BASE_URL}/{LANG}",
    "login":          f"{BASE_URL}/{LANG}",
    "personal_info":  f"{BASE_URL}/{LANG}/user/personal-information",
    "purchases":      f"{BASE_URL}/{LANG}/user/purchases",
    "events":         f"{BASE_URL}/{LANG}/events",
    "events_create":  f"{BASE_URL}/{LANG}/user/events/create",
    "events_list":    f"{BASE_URL}/{LANG}/user/events",
    "reports":        f"{BASE_URL}/{LANG}/user/reports",
}

TIMEOUTS = {
    "default":    30_000,
    "navigation": 60_000,
    "element":    10_000,
}

MANAGER_USER = {
    "email":    os.getenv("EMAIL"),
    "password": os.getenv("PASSWORD"),
}

NEW_USER = {
    "email":      "test_user_{}@example.com",
    "password":   "TestUser123!",
    "first_name": "Test",
    "last_name":  "User",
}

EVENT_DATA = {
    "title":       "Playwright Auto Event",
    "description": "Created by automation",
    "date":        "2027-01-15",
    "time":        "19:00",
    "location":    "Belgrade",
    "capacity":    "100",
}