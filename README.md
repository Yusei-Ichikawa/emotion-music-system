# TEAM5 : Emotion Music System

🎵 **Emotion Music System** は、ユーザーの表情を認識して感情を分類し、その感情に対応する音楽を自動再生するPythonベースのリアルタイムシステムです。

---

# Member list and role

1. m5281014, Yusei Ichikawa プレゼン作成、見せ方を考える
2. m5281030, NAKAMURA Zen システム構築
3. m5291051, MURAKAMI Tatsuya 適切な音楽を探す
4. m5291067, SHU Hoshitaka システム構築

## 🧠 システム概要

- ノートPCのWebカメラで映像を取得
- 取得した画像をGoogle Colab上のYOLOモデルに送信
- YOLOで「怒り・悲しみ・笑い・真顔」の4つの感情を推論
- 推論結果に応じて、ローカルPC上で対応する音楽を再生

---

## 🏗️ 構成ファイル

emotion-music-system/

├──fine-tune/　　　#ファインチューニング用フォルダ

    ├──data.yaml

    ├──train_command.txt　　　#ファインチューイングコマンド

├── send_image_to_colab.py         # Webカメラ画像をColabへ送信

├── play_music_by_emotion.py       # 感情に応じて音楽を再生

├── emotion_music_config.json      # 感情と音楽ファイルのマッピング

├── music/                         # 音楽ファイルを格納

├── .gitignore                     # Git除外設定

└── README.md                      # このファイル

---

## ⚙️ 開発環境　※適当なので後で編集してください

- Python 3.8+
- OpenCV (`cv2`)
- requests
- Flask（Colab側）
- pygame（ローカルの音楽再生で使用予定）

---

## 🚀 使用予定モデル

- [YOLOv5 / YOLOv8](https://github.com/ultralytics/yolov5)（Google Colab で事前学習済みモデルを使用）
- 感情分類：Angry / Sad / Happy / Neutral（4クラス）
  - 最終層だけ4クラスに分けて再学習するだけで十分

## データセット

* Facial Expression Image Data AFFECTNET YOLO Format
  * [https://www.kaggle.com/datasets/fatihkgg/affectnet-yolo-format](https://www.kaggle.com/datasets/fatihkgg/affectnet-yolo-format)
    * We're going to use 4 emotions:
      * **Anger, Sad, Happy, Neutral**

## ゴール
