# =============================
# ✅ 事前準備：ライブラリのインストール（最初の1回だけ）
# =============================
!pip install flask flask-ngrok opencv-python-headless -q
!pip install torch torchvision torchaudio -q
!git clone https://github.com/ultralytics/yolov5.git
%cd yolov5
!pip install -r requirements.txt -q
%cd ..

# =============================
# ✅ Flaskサーバ実装（/predict エンドポイント）
# =============================
from flask import Flask, request, jsonify
from flask_ngrok import run_with_ngrok
import torch
import base64
import numpy as np
import cv2
import io
from PIL import Image

# モデル読み込み（4クラスでfine-tune済みの.ptを指定）
MODEL_PATH = "/content/emotion_yolo.pt"  # ここを自身のモデルに合わせて変更
model = torch.hub.load("ultralytics/yolov5", "custom", path=MODEL_PATH)
model.conf = 0.5  # 信頼度しきい値

# クラス名（事前学習時の順番に合わせる）
EMOTION_LABELS = ['angry', 'happy', 'neutral', 'sad']

app = Flask(__name__)
run_with_ngrok(app)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        image_b64 = data['image']
        image_bytes = base64.b64decode(image_b64)
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # 推論
        results = model(img)
        df = results.pandas().xyxy[0]
        if df.empty:
            return jsonify({"emotion": "unknown"})

        # 最も信頼度が高い1件を返す
        top_row = df.iloc[0]
        label_idx = int(top_row['class'])
        emotion = EMOTION_LABELS[label_idx]
        return jsonify({"emotion": emotion})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =============================
# ✅ サーバ起動
# =============================
app.run()

'''
実行後に表示される ngrok URL をコピーしてローカルの send_image_to_colab.py に設定
COLAB_URL = "http://xxxx.ngrok.io/predict"
'''
