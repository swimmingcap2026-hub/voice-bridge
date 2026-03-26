
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 確保這就是您 Mac Mini 的真實 Ngrok 公開隧道網址
OPENCLAW_GATEWAY_URL = "https://unsourly-unincludable-tama.ngrok-free.dev/voice/webhook"

@app.route('/voice/webhook', methods=['POST'])
def handle_vapi_webhook():
    data = request.json
    print(f"Bridge received signal: {data}")
    
    try:
        # 轉發請求到 Mac Mini
        response = requests.post(OPENCLAW_GATEWAY_URL, json=data, timeout=10)
        
        # 如果 Mac 回傳 JSON，我們就回傳 JSON；如果 Mac 回傳空值，我們回傳一個預設成功
        if response.text.strip():
            return jsonify(response.json()), response.status_code
        else:
            return jsonify({"status": "ok", "message": "Mac Mini received signal"}), 200
            
    except Exception as e:
        print(f"Error forwarding to OpenClaw Mac: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
