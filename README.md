# TEAM5 : Emotion Music System

🎵 **Emotion Music System** は、ユーザーの表情を認識して感情を分類し、その感情に対応する音楽を自動再生するPythonベースのリアルタイムシステムです。

---

# Member list and role

1. m5281014, ICHIKAWA Yusei プレゼン作成、見せ方を考える
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

        ├── music/                         # 音楽ファイルを格納

        ├── runs/                          # 学習履歴

        ├── YOLO_format/                   # 8クラス表情認識のデータセット

        ├── src                            # Sorce Code

            ├── train.py                   # YOLO11を用いて学習

            ├── main.py                    # Webカメラ動画から表情検出、音楽再生

            ├── detector.py                # 表情認識クラス（表情認識し、クラスとBounding Boxを表示させる）

            └── music_player.py            # 音楽再生クラス（表情認識したクラスごとに音楽を再生させる）

        ├── best.pt                        # 推論に使うYOLO11の重み

        ├── requirements.txt               # 環境構築用ファイル

        ├── .gitignore                     # Git除外設定

        └── README.md                      # このファイル

---

## ⚙️ 開発環境
Install the `ultralytics` package, including all [requirements](https://github.com/ultralytics/ultralytics/blob/main/pyproject.toml), in a [**Python>=3.8**](https://www.python.org/) environment with [**PyTorch>=1.8**](https://pytorch.org/get-started/locally/).

[![PyPI - Version](https://img.shields.io/pypi/v/ultralytics?logo=pypi&logoColor=white)](https://pypi.org/project/ultralytics/) [![Ultralytics Downloads](https://static.pepy.tech/badge/ultralytics)](https://www.pepy.tech/projects/ultralytics) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ultralytics?logo=python&logoColor=gold)](https://pypi.org/project/ultralytics/)

    pip install -r requirements.txt

- Python 3.8+
- OpenCV (`cv2`)
- ultralytics
- pygame（ローカルの音楽再生で使用予定）

---

## 🚀 使用予定モデル

- [YOLO11](https://github.com/ultralytics/ultralytics)
- 感情分類：Angry / Disgust / Fear / Happy /  Sad / Neutral / Contempt（8クラス）

## データセット

* Facial Expression Image Data AFFECTNET YOLO Format
  * [https://www.kaggle.com/datasets/fatihkgg/affectnet-yolo-format](https://www.kaggle.com/datasets/fatihkgg/affectnet-yolo-format)
    * We're going to use 8 emotions:
      * **Angry, Disgust, Fear, Happy,  Sad, Neutral, Contempt**

## ゴール
