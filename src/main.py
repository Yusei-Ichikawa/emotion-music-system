import cv2
from detector import FaceExpressionDetector
from music_player import MusicPlayer

# 推論用クラスと音楽再生クラスを初期化
detector = FaceExpressionDetector('../best.pt')
music = MusicPlayer('../music')

# Webカメラからビデオキャプチャ開始（0 = default camera）
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 560)

prev_expression = None
stable_count = 0
threshold_frames = 90  # 3秒程度(30fps想定)

# 状況設定辞書
expression_to_state = {
    tuple(sorted(['Happy'])): 'joy_music',
    tuple(sorted(['Sad'])): 'sad_music',
    tuple(sorted(['Anger'])): 'anger_music',
    tuple(sorted(['Fear'])): 'fear_music',
    tuple(sorted(['Surprise'])): 'surprise_music',
    tuple(sorted(['Neutral'])): 'neutral_music',
    tuple(sorted(['Disgust'])): 'disgust_music',
    tuple(sorted(['Contempt'])): 'contempt_music',

    tuple(sorted(['Happy', 'Surprise'])): 'excited_music',
    tuple(sorted(['Fear', 'Sad'])): 'anxious_music',
    tuple(sorted(['Anger', 'Disgust'])): 'angry_disgust_music',
    tuple(sorted(['Contempt', 'Neutral'])): 'calm_but_disdain',
    tuple(sorted(['Happy', 'Neutral'])): 'content_music',
    tuple(sorted(['Contempt', 'Sad'])): 'bitter_music',
    tuple(sorted(['Contempt', 'Fear'])): 'fearful_disdain',
    tuple(sorted(['Fear', 'Surprise'])): 'shocked_music',
}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 顔表情検出＋描画＋ラベル取得
    frame, predicted_expression = detector.detect_and_draw(frame)

    # 表情ラベルの組み合わせをソート＆一意化
    current_expressions = sorted(set(predicted_expression)) if predicted_expression else []

    # 一定時間同じ表情が続くか判定
    if current_expressions == prev_expression:
        stable_count += 1
    else:
        prev_expression = current_expressions
        stable_count = 1 if current_expressions else 0

    # 状況判定と音楽再生
    if current_expressions and stable_count >= threshold_frames:
        key = tuple(current_expressions)
        state = expression_to_state.get(key, 'default_music')
        music.play(state)
    else:
        state = 'No stable expression'
        music.stop()

    # --- 画面上部中央に現在の状況表示 ---
    display_text = f'State: {state}'
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.0
    font_thickness = 2
    text_size, _ = cv2.getTextSize(display_text, font, font_scale, font_thickness)
    text_width, text_height = text_size
sydney@SYDNEY
    frame_width = frame.shape[1]
    x = (frame_width - text_width) // 2
    y = 30

    # 背景の黒い矩形
    cv2.rectangle(frame, (x - 10, y - text_height - 10), (x + text_width + 10, y + 10), (0, 0, 0), -1)
    # 文字描画（白色）
    cv2.putText(frame, display_text, (x, y), font, font_scale, (255, 255, 255), font_thickness)

    # 映像表示
    cv2.imshow('Facial Expression Recognition', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
music.stop()
