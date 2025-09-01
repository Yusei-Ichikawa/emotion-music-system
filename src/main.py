import cv2
from detector import FaceExpressionDetector
# from music_player import MusicPlayer

from collections import deque, Counter

import test

# 推論用クラスと音楽再生クラスを初期化
detector = FaceExpressionDetector('../best.pt')
# music = MusicPlayer('../music')

# Webカメラからビデオキャプチャ開始（0 = default camera）
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 560)

prev_expression = None
# stable_count = 0
threshold_frames = 90  # 3秒程度(30fps想定)
expression_history = deque(maxlen=threshold_frames)

current_playing_expression = ""  # 初期状態は中立

test.start_music()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 顔表情検出＋描画＋ラベル取得
    frame, predicted_expression = detector.detect_and_draw(frame)

    # ===過去数秒間の多数決===
    # 検出された表情を履歴に追加（Noneは除外）
    if predicted_expression is not None:
        expression_history.append(predicted_expression)

    # 履歴が閾値フレーム数に達したら、最頻の表情に基づいて音楽を再生
    if len(expression_history) == threshold_frames:
        tuple_history = [tuple(e) for e in expression_history]
        # 過去3秒で最も多く検出された表情を計算
        most_common_expression = Counter(tuple_history).most_common(1)[0][0]
        test.set_expression(most_common_expression)
    # =========================

    # 映像表示
    cv2.imshow('Facial Expression Recognition', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
# music.stop()
test.stop_music()
