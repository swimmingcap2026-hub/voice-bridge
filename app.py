
from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# 使用您當前 Mac Mini 的公開 Ngrok 隧道 (這必須保持開啟)
OPENCLAW_GATEWAY_URL = "https://unsourly-unincludable-tama.ngrok-free.dev/voice/webhook"

logging.basicConfig(level=logging.INFO)

@app.route('/voice/webhook', methods=['POST'])
def handle_vapi_webhook():
    data = request.json
    logging.info(f"--- [Cloud Bridge] Received from Vapi: {data} ---")
    
    try:
        # 嘗試連接 Mac Mini 的隧道
        response = requests.post(OPENCLAW_GATEWAY_URL, json=data, timeout=5)
        logging.info(f"--- [Cloud Bridge] Forwarded to Mac Mini (Status: {response.status_code}) ---")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        error_msg = f"--- [Cloud Bridge] Forwarding Error: {e} ---"
        logging.error(error_msg)
        return jsonify({"status": "error", "message": error_msg}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
