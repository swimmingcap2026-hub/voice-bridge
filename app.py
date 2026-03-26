
import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 這是我們這次測試成功的隧道網址
OPENCLAW_GATEWAY_URL = "https://unsourly-unincludable-tama.ngrok-free.dev/voice/webhook"

@app.route('/voice/webhook', methods=['POST'])
def handle_vapi_webhook():
    data = request.json
    print(f"Received Vapi signal: {data}")
    
    # 將訊號轉發給您的 OpenClaw
    try:
        response = requests.post(OPENCLAW_GATEWAY_URL, json=data, timeout=10)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        print(f"Error forwarding to OpenClaw: {e}")
        return jsonify({"status": "error", "message": "Failed to connect to Mac Mini Tunnel"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
