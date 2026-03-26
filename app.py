
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 使用您當前 Mac Mini 的公開 Ngrok 隧道 (這必須對應 Vapi Dashboard 的設定)
OPENCLAW_GATEWAY_URL = "https://unsourly-unincludable-tama.ngrok-free.dev/voice/webhook"

@app.route('/voice/webhook', methods=['POST'])
def handle_vapi_webhook():
    data = request.json
    print(f"--- [Bridge] Received from Vapi: {data} ---")
    try:
        response = requests.post(OPENCLAW_GATEWAY_URL, json=data, timeout=10)
        return jsonify({"status": "forwarded", "code": response.status_code}), response.status_code
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
