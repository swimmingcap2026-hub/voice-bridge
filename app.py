
from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# 綁定您的 Mac Mini 隧道
OPENCLAW_GATEWAY_URL = "http://127.0.0.1:18789/webhook"

logging.basicConfig(level=logging.INFO)

@app.route('/voice/webhook', methods=['POST'])
def handle_vapi_webhook():
    data = request.json
    logging.info(f"--- [Bridge] Vapi Data: {data} ---")
    
    # 判斷是否為工具呼叫指令
    if data and 'toolCalls' in data:
        logging.info("--- [Bridge] Detected Tool Call, forwarding... ---")
        try:
            # 將完整的工具呼叫資訊轉發給 OpenClaw
            response = requests.post(OPENCLAW_GATEWAY_URL, json=data, timeout=10)
            return jsonify({"status": "tool_forwarded"}), response.status_code
        except Exception as e:
            logging.error(f"--- [Bridge] Forwarding Error: {e} ---")
            return jsonify({"status": "error", "message": str(e)}), 500
    
    # 一般對話訊號轉發
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
