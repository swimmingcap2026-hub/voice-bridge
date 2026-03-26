
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 這是我們 Mac Mini 的公開 ngrok 隧道網址
OPENCLAW_GATEWAY_URL = "https://unsourly-unincludable-tama.ngrok-free.dev/voice/webhook"

@app.route('/voice/webhook', methods=['POST'])
def handle_vapi_webhook():
    data = request.json
    print(f"--- [Bridge] Received signal from Vapi: {data} ---")
    
    # 嘗試轉發請求到 Mac Mini
    try:
        response = requests.post(OPENCLAW_GATEWAY_URL, json=data, timeout=10)
        print(f"--- [Bridge] Forwarded to Mac Mini (Status: {response.status_code}) ---")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        error_msg = f"--- [Bridge] Forwarding Error: {e} ---"
        print(error_msg)
        return jsonify({"status": "error", "message": error_msg}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
