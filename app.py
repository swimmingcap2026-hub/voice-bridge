
from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# 修正：精確對接 OpenClaw 插件監聽的 58888 埠口
# 這裡發送給本地隧道，隧道會將請求轉發給您的 Mac Mini
OPENCLAW_GATEWAY_URL = "https://unsourly-unincludable-tama.ngrok-free.dev/voice/webhook"

logging.basicConfig(level=logging.INFO)

@app.route('/voice/webhook', methods=['POST'])
def handle_vapi_webhook():
    data = request.json
    logging.info(f"--- [Bridge] Received signal: {data} ---")
    
    try:
        # 轉發請求到 Ngrok 隧道，路徑為語音插件監聽點
        # 注意：我們需要確信隧道是轉發到本地 58888
        response = requests.post(OPENCLAW_GATEWAY_URL, json=data, timeout=10)
        logging.info(f"--- [Bridge] Forwarded to Mac Tunnel (Status: {response.status_code}) ---")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        error_msg = f"--- [Bridge] Forwarding Error: {e} ---"
        logging.error(error_msg)
        return jsonify({"status": "error", "message": error_msg}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
