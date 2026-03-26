
from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# 指向 Mac Mini 的隧道網址
OPENCLAW_GATEWAY_URL = "https://unsourly-unincludable-tama.ngrok-free.dev/voice/webhook"

logging.basicConfig(level=logging.INFO)

@app.route('/voice/webhook', methods=['POST'])
def handle_vapi_webhook():
    data = request.json
    logging.info(f"--- [Bridge] Received: {data} ---")
    
    try:
        # 轉發指令並強制給予回應
        response = requests.post(OPENCLAW_GATEWAY_URL, json=data, timeout=5)
        logging.info(f"--- [Bridge] Mac Response: {response.text} ---")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        logging.error(f"--- [Bridge] Tunnel Connection Failed: {e} ---")
        # 回傳一個「模擬成功」的 JSON，避免 AI 被斷開
        return jsonify({"status": "error", "message": "Bridge failed, but alive"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
