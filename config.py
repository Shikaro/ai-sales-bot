import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ADMIN_ID = int(os.getenv("ADMIN_ID") or 0)
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "Shikaro").strip().lstrip("@")
WHATSAPP = os.getenv("WHATSAPP", "+79651665669").strip()
EMAIL = os.getenv("EMAIL", "S.Saplinov@gmail.com").strip()

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не задан в .env")
