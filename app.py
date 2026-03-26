
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 這是 Mac Mini 目前對外的 Ngrok 隧道地址
MAC_MINI_URL = "https://unsourly-unincludable-tama.ngrok-free.dev/voice/webhook"

@app.route('/webhook/post', methods=['POST'])
def handle_vapi_webhook():
    data = request.json
    print(f"--- [Bridge] Forwarding signal to Mac Mini: {data} ---")
    
    try:
        # 直接同步轉發並等待 Mac Mini 的 OpenClaw 回應
        response = requests.post(MAC_MINI_URL, json=data, timeout=10)
        
        # 回傳 OpenClaw 的執行結果給 Vapi
        return jsonify(response.json()), response.status_code
    except Exception as e:
        print(f"--- [Bridge] Forwarding Error: {e} ---")
        return jsonify({"status": "error", "message": "Mac Mini is offline"}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
