
from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# 這是修正後的關鍵：指向 Mac Mini 本地語音插件真正監聽的 58888 埠口
OPENCLAW_VOICE_PLUGIN_URL = "http://127.0.0.1:58888/voice/webhook"

logging.basicConfig(level=logging.INFO)

@app.route('/voice/webhook', methods=['POST'])
def handle_vapi_webhook():
    data = request.json
    logging.info(f"--- [Bridge] Forwarding signal to Mac Mini Port 58888 ---")
    
    try:
        # 轉發請求到 Mac Mini
        response = requests.post(OPENCLAW_VOICE_PLUGIN_URL, json=data, timeout=5)
        # 確保回傳正確的 JSON 給 Vapi
        return jsonify(response.json()), response.status_code
    except Exception as e:
        logging.error(f"--- [Bridge] Forwarding Error: {e} ---")
        return jsonify({"status": "error", "message": "Failed to connect to Mac Mini Port 58888"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
