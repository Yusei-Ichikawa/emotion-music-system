import cv2
from ultralytics import YOLO

# YOLOによる表情認識クラス
class FaceExpressionDetector:
    def __init__(self, model_path='best.pt'):
        # YOLOモデルのロード
        self.model = YOLO(model_path)
        # 感情ラベルと色の対応表（BGR）
        self.emotion_colors = {
            "Anger":    (0, 0, 255),      # 怒り: 赤
            "Disgust":  (0, 128, 0),      # 嫌悪: 濃い緑
            "Fear":     (128, 0, 128),    # 恐れ: 紫
            "Happy":    (0, 255, 255),    # 喜び: 黄色
            "Sad":      (255, 255, 0),    # 悲しみ; 水色
            "Surprise": (128, 255, 0),    # 驚き: 黄緑
            "Neutral":  (128, 128, 128),  # 中立: グレー
            "Contempt": (255, 0, 0)       # 軽蔑: 青
        }

    def detect_and_draw(self, frame):
        # 推論
        results = self.model(frame, conf=0.5)
        predicted_expressions = []
        # 検出があれば処理
        if len(results) > 0:
            result = results[0]
            boxes = result.boxes

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
                (tw, th), baseline = cv2.getTextSize(f"{label} {conf*100:.1f}", font, font_scale, thickness)
                text_x = x1 + 1
                text_y = y1 + int(font_scale*22)
                # 背景色
                cv2.rectangle(frame, (x1, y1), (x1+tw+1, y1+th+2), box_color, -1)
                # バウンディングボックス
                cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 4)
                # ラベル文字
                cv2.putText(frame, f"{label} {conf*100:.1f}", (text_x, text_y), font, font_scale, (0, 0, 0), thickness, cv2.LINE_AA)

                # 全ての検出された表情ラベルを保存
                predicted_expressions.append(label)

        return frame, predicted_expressions
