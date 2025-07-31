import cv2
from detector import FaceExpressionDetector
from music_player import MusicPlayer

from collections import deque, Counter

# 推論用クラスと音楽再生クラスを初期化
detector = FaceExpressionDetector('../best.pt')
music = MusicPlayer('../music')

# Webカメラからビデオキャプチャ開始（0 = default camera）
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 560)

prev_expression = None
# stable_count = 0
threshold_frames = 90  # 3秒程度(30fps想定)
expression_history = deque(maxlen=threshold_frames)

current_playing_expression = ""  # 初期状態は中立

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 顔表情検出＋描画＋ラベル取得
    frame, predicted_expression = detector.detect_and_draw(frame)

    # =====================
    # ===過去数秒間の多数決===
    # 検出された表情を履歴に追加（Noneは除外）
    if predicted_expression is not None:
        expression_history.append(predicted_expression)

    # 履歴が閾値フレーム数に達したら、最頻の表情に基づいて音楽を再生
    if len(expression_history) == threshold_frames:
        # 過去3秒で最も多く検出された表情を計算
        most_common_expression = Counter(expression_history).most_common(1)[0][0]

        # 現在再生中の表情と異なる場合のみ、新しい曲を再生
        if most_common_expression != current_playing_expression:
            music.play(most_common_expression)
            current_playing_expression = most_common_expression
    # =========================
    # =========================

    # # 一定時間同じ表情が続くか判定
    # if predicted_expression == prev_expression:
    #     stable_count += 1
    # else:
    #     prev_expression = predicted_expression
    #     stable_count = 1 if predicted_expression is not None else 0

    # # 表情が3秒安定で音楽再生
    # if predicted_expression is not None and stable_count >= threshold_frames:
    #     music.play(predicted_expression)
    # # # 表情検出なしで音楽停止
    # # if predicted_expression is None and music.current_audio_label is not None:
    # #     music.stop()


    # 映像表示
    cv2.imshow('Facial Expression Recognition', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
music.stop()
