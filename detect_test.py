import ultralytics
ultralytics.checks()  # 環境チェック（省略可）

from ultralytics import YOLO

# Detectionをモジュール化
# source="movies/543618324613824613.mp4"
def run_detection(source="movies/ScreenRecordin.mov", conf=0.5, show=True):
    # 訓練済みモデルのロード
    model = YOLO("runs/detect/train/weights/best.pt")

    results = model.predict(
        source=source,
        conf=conf,
        show=show
    )

    for i, result in enumerate(results):
        #results.show()
        if i%50==0:
            result.save(filename=f"facial_emotion_detection/img_{i}.jpg")

    return results

if __name__ == "__main__":
    results = run_detection()
