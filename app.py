
from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# 指向 Mac Mini 本地監聽的地址
OPENCLAW_GATEWAY_URL = "http://127.0.0.1:18789/webhook"

logging.basicConfig(level=logging.INFO)

@app.route('/voice/webhook', methods=['POST'])
def handle_vapi_webhook():
    data = request.json
    logging.info(f"--- [Cloud Bridge] Received from Vapi: {data} ---")
    
    try:
        # 轉發指令給 OpenClaw，並等待結果 (timeout 設定長一點)
        response = requests.post(OPENCLAW_GATEWAY_URL, json=data, timeout=20)
        
        # 將 OpenClaw 的回覆，直接轉交給 Vapi
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"status": "error", "message": "Mac Mini failed to process"}), 500
            
    except Exception as e:
        logging.error(f"--- [Bridge] Tunnel Connection Failed: {e} ---")
        return jsonify({"status": "error", "message": "Bridge connection failed"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
