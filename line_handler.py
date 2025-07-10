from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)

# 從 config.py 取得 Channel Secret 和 Access Token
from config import CHANNEL_SECRET, CHANNEL_ACCESS_TOKEN

# 從自訂服務模組呼叫 Groq 模型產生回覆文字
from services.groq_llm import generate_reply

# 建立 LINE WebhookHandler 用來處理 webhook 請求的簽章驗證及事件分發
handler = WebhookHandler(CHANNEL_SECRET)

# 建立 LINE Messaging API 的設定物件（包含 Access Token）
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)

# 當收到「文字訊息事件」時會觸發此函式
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event: MessageEvent):
    # 取得使用者傳來的文字並去除頭尾空白
    user_input = event.message.text.strip()

    # 呼叫 Groq AI 模型產生回應文字
    reply_text = generate_reply(user_input)

    # 使用 ApiClient 以設定好的 Access Token 連線 LINE API
    with ApiClient(configuration) as api_client:
        # 建立 MessagingApi 用來發送訊息
        line_bot_api = MessagingApi(api_client)

        # 呼叫 reply_message 送出回覆
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,  # 用來指定回覆對象
                messages=[TextMessage(text=reply_text)]  # 封裝文字訊息格式
            )
        )
