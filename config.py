from linebot.v3.messaging import Configuration
import os

# === LINE Bot 基本設定 ===
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")

# 建立 LINE SDK 所需的 Configuration 物件
LINE_CONFIGURATION = Configuration(access_token=CHANNEL_ACCESS_TOKEN)

# === Groq API 設定 ===
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"