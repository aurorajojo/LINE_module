import requests
import os
from config import GROQ_API_KEY, GROQ_API_URL

# 載入 system prompt 的函式
def load_system_prompt():
    # 定義 system_prompt.txt 的路徑
    prompt_path = os.path.join("prompt", "system_prompt.txt")
    
    # 如果檔案存在，讀取內容並去除前後空白
    if os.path.exists(prompt_path):
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    else:
        # 若找不到檔案，使用預設的系統提示字串作為備援
        return "你是一個親切且善於回應的聊天助手。"

# 呼叫 Groq LLM API 取得模型回應的函式
def generate_reply(user_input: str) -> str:
    # 先載入 system prompt
    system_prompt = load_system_prompt()

    # 設定 HTTP 請求標頭（包含 API 金鑰）
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # 組裝 POST 請求的內容
    payload = {
        "model": "llama-3.3-70b-versatile",  # 使用的模型名稱
        "messages": [
            {"role": "system", "content": system_prompt},  # 系統提示語
            {"role": "user", "content": user_input}        # 使用者輸入
        ],
        "temperature": 0.7,  # 影響回答的創意程度，越高越隨機
        "max_tokens": 1024   # 回應最大 token 數
    }

    # 發送 POST 請求到 Groq API
    response = requests.post(GROQ_API_URL, headers=headers, json=payload)

    # 若回應成功，解析並回傳模型產生的回答文字
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        # 若 API 呼叫失敗，回傳錯誤提示文字
        return "發生錯誤，請稍後再試。"
