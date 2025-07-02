import cv2
import requests
import base64
import time

# ====== 設定 ======
COLAB_URL = "http://<Colabの公開URL>/predict"  # 後で置き換える
CAPTURE_INTERVAL = 3  # 秒に1回送信
CAMERA_INDEX = 0

# ====== カメラ初期化 ======
cap = cv2.VideoCapture(CAMERA_INDEX)
if not cap.isOpened():
    print("❌ カメラが開けません")
    exit(1)

print("📸 カメラ起動。Ctrl+Cで終了")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ フレーム取得失敗")
            continue

        # JPEGエンコード → Base64変換
        _, img_encoded = cv2.imencode('.jpg', frame)
        img_base64 = base64.b64encode(img_encoded).decode('utf-8')

        # POSTリクエスト送信
        response = requests.post(COLAB_URL, json={"image": img_base64})
        if response.status_code == 200:
            result = response.json()
            print(f"🧠 感情推論結果: {result.get('emotion')}")
        else:
            print(f"❌ 推論失敗: {response.status_code}")

        time.sleep(CAPTURE_INTERVAL)

except KeyboardInterrupt:
    print("\n🛑 停止されました")

finally:
    cap.release()
