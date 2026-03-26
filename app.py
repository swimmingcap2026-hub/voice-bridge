
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 修正：精確指向語音插件監聽的本地埠口 (4000)
OPENCLAW_VOICE_URL = "http://127.0.0.1:4000/voice/webhook"

@app.route('/voice/webhook', methods=['POST'])
def handle_vapi_webhook():
    data = request.json
    print(f"--- 雲端橋樑收到訊號 ---")
    print(f"內容: {data}")
    
    # 轉發訊號給 Mac Mini 本地的語音插件
    try:
        response = requests.post(OPENCLAW_VOICE_URL, json=data, timeout=10)
        print(f"--- 成功轉發給 Mac Mini (狀態: {response.status_code}) ---")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        print(f"--- 轉發失敗: {e} ---")
        return jsonify({"status": "error", "message": "Failed to connect to Mac Mini local port 4000"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
