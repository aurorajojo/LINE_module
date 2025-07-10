from flask import Flask, request, abort
from line_handler import handler  # 從 line_handler.py 匯入 handler
from linebot.v3.exceptions import InvalidSignatureError

# 建立 Flask 應用
app = Flask(__name__)

# 測試用路由，確認服務是否啟動
@app.route("/", methods=["GET"])
def home():
    return {"message": "LINE Bot is running."}

# LINE webhook 的主要接收路由，接收 POST 請求
@app.route("/callback", methods=["POST"])
def callback():
    # 取出 HTTP header 中的 X-Line-Signature 用於驗證
    signature = request.headers.get("X-Line-Signature")

    # 取出 HTTP Request 的原始內容（文字格式）
    body = request.get_data(as_text=True)

    try:
        # 交給 handler 進行簽章驗證並處理事件
        handler.handle(body, signature)
    except InvalidSignatureError:
        # 驗證失敗回傳 400 Bad Request
        abort(400)

    # 成功後回傳簡單字串給 LINE 伺服器
    return "OK"


# 如果直接執行此檔案，啟動 Flask 伺服器，監聽本地 5000 port
if __name__ == "__main__":
    app.run(port=5000)
