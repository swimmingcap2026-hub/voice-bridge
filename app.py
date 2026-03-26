
from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# 指向您 Mac 的真實 Ngrok 隧道
OPENCLAW_GATEWAY_URL = "https://unsourly-unincludable-tama.ngrok-free.dev/voice/webhook"

logging.basicConfig(level=logging.INFO)

@app.route('/voice/webhook', methods=['POST'])
def handle_vapi_webhook():
    data = request.json
    logging.info(f"--- [Bridge] Forwarding signal to Mac ---")
    
    try:
        # 轉發請求
        response = requests.post(OPENCLAW_GATEWAY_URL, json=data, timeout=10)
        
        # 關鍵除錯：如果無法解析 JSON，印出原始內容
        try:
            return jsonify(response.json()), response.status_code
        except ValueError:
            logging.error(f"--- [Bridge] Mac returned non-JSON: {response.text} ---")
            return jsonify({"status": "error", "message": "Mac returned malformed data"}), 500
            
    except Exception as e:
        logging.error(f"--- [Bridge] Connection Error: {e} ---")
        return jsonify({"status": "error", "message": "Bridge connection failed"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
