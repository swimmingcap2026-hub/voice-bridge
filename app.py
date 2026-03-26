
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 修正：精確指向語音插件監聽的本地埠口 (58888)
# 當您剛剛重啟服務時，OpenClaw 自動為它分配了這個埠號
OPENCLAW_GATEWAY_URL = "http://127.0.0.1:58888/voice/webhook"

@app.route('/voice/webhook', methods=['POST'])
def handle_vapi_webhook():
    data = request.json
    print(f"--- 雲端橋樑收到訊號並轉發至 Mac Mini: 58888 ---")
    
    # 轉發訊號給 OpenClaw Gateway
    try:
        response = requests.post(OPENCLAW_GATEWAY_URL, json=data, timeout=10)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        print(f"--- 轉發失敗: {e} ---")
        return jsonify({"status": "error", "message": "Failed to connect to Mac Mini Tunnel"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
