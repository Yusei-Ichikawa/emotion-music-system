import cv2
from detector import FaceExpressionDetector
from music_player import MusicPlayer

# 推論用クラスと音楽再生クラスを初期化
detector = FaceExpressionDetector('best.pt')
music = MusicPlayer('music')

# Webカメラからビデオキャプチャ開始（0 = default camera）
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 560)

prev_expression = None
stable_count = 0
threshold_frames = 90  # 3秒程度(30fps想定)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 顔表情検出＋描画＋ラベル取得
    frame, predicted_expression = detector.detect_and_draw(frame)

    # 一定時間同じ表情が続くか判定
    if predicted_expression == prev_expression:
        stable_count += 1
    else:
        prev_expression = predicted_expression
        stable_count = 1 if predicted_expression is not None else 0

    # 表情が3秒安定で音楽再生
    if predicted_expression is not None and stable_count >= threshold_frames:
        music.play(predicted_expression)
    # # 表情検出なしで音楽停止
    # if predicted_expression is None and music.current_audio_label is not None:
    #     music.stop()

    # 映像表示
    cv2.imshow('Facial Expression Recognition', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
music.stop()
