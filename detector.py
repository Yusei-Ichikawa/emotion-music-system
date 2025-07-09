import cv2
from ultralytics import YOLO

# YOLOによる表情認識クラス
class FaceExpressionDetector:
    def __init__(self, model_path='best.pt'):
        # YOLOモデルのロード
        self.model = YOLO(model_path)
        # 感情ラベルと色の対応表（BGR）
        self.emotion_colors = {
            "Anger":    (0, 0, 255),      # 赤
            "Disgust":  (0, 128, 0),      # 濃い緑
            "Fear":     (128, 0, 128),    # 紫
            "Happy":    (0, 255, 255),    # 黄色
            "Sad":      (255, 255, 0),    # 水色
            "Surprise": (128, 255, 0),    # 黄緑
            "Neutral":  (128, 128, 128),  # グレー
            "Contempt": (255, 0, 0)       # 青
        }

    def detect_and_draw(self, frame):
        # 推論
        results = self.model(frame)
        predicted_expression = None
        # 検出があれば処理
        if len(results) > 0:
            result = results[0]
            boxes = result.boxes
            max_confidence = 0.0
            best_label = None

            for box in boxes:
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                label = result.names.get(cls, "")
                box_color = self.emotion_colors.get(label, (255, 255, 255)) # 未登録なら白

                # ラベル背景と文字描画
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 1.5
                thickness = 3
                (tw, th), baseline = cv2.getTextSize(label, font, font_scale, thickness)
                text_x = x1 + 1
                text_y = y1 + int(font_scale*22)
                # 背景色
                cv2.rectangle(frame, (x1, y1), (x1+tw, y1+th), box_color, -1)
                # バウンディングボックス
                cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
                # ラベル文字
                cv2.putText(frame, label, (text_x, text_y), font, font_scale, (0, 0, 0), thickness, cv2.LINE_AA)

                # 信頼度が最大のクラスを推論ラベルとする
                if conf > max_confidence:
                    max_confidence = conf
                    best_label = label

            if best_label:
                predicted_expression = best_label
        return frame, predicted_expression
