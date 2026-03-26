
from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# 修復：這是您的 Mac Mini 真實隧道網址，這是唯一直達您電腦的路徑
OPENCLAW_GATEWAY_URL = "https://unsourly-unincludable-tama.ngrok-free.dev/voice/webhook"

logging.basicConfig(level=logging.INFO)

@app.route('/voice/webhook', methods=['POST'])
def handle_vapi_webhook():
    data = request.json
    logging.info(f"--- [Bridge] Forwarding signal to Mac Mini Tunnel ---")
    
    try:
        # 轉發給您 Mac Mini 的 Ngrok 隧道
        response = requests.post(OPENCLAW_GATEWAY_URL, json=data, timeout=10)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        logging.error(f"--- [Bridge] Forwarding Error: {e} ---")
        return jsonify({"status": "error", "message": "Failed to connect to Mac Mini Tunnel"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
