
import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 這是您的主機 OpenClaw API 地址 (因為它是在您的 Mac 上)
OPENCLAW_GATEWAY_URL = "http://localhost:18789/voice/webhook"

@app.route('/voice/webhook', methods=['POST'])
def handle_vapi_webhook():
    data = request.json
    print(f"Received Vapi signal: {data}")
    
    # 轉發訊號給 OpenClaw Gateway
    try:
        response = requests.post(OPENCLAW_GATEWAY_URL, json=data, timeout=5)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        print(f"Error forwarding to OpenClaw: {e}")
        return jsonify({"status": "error", "message": "Failed to connect to Mac Mini"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
