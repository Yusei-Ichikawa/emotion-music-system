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
- YOLOで「怒り・嫌悪・恐れ・喜び・悲しみ・驚き・軽蔑・真顔」の８つの感情を推論
  - 8つだと音楽に関して作るのが大変なので5つのグループ(happy, [anger, fear], [sad, disgust, contempt], surprise, neutral)にまとめた
  - 2人の時検出された時のグループをさらに追加した
    - happy + [anger, fear] -> 激情
    - happy + [sad, disgust, contempt] -> 複雑な心境
    - happy + surprise -> サプライズ成功
    - [anger, fear] + [sad, disgust, contempt] -> 叱責
    - [anger, fear] + surprise -> 突然の雷
    - [sad, disgust, contempt] + surprise -> 悪い知らせ
- 推論結果に応じて、常に流れている音楽(きらきら星)を編曲
  - 3秒間で最も検出された表情を用いて編曲する
  - 音楽はピアノ(メロディ), ピアノ(コード伴奏), ギター, ベース, ドラム, ストリングス(弦楽器), ブラス(管楽器)の7つの楽器で構成される
  - 変化するパラメータはテンポ, キー, 各楽器の音量, メロディの音の高さ, コード進行

---

## 🏗️ 構成ファイル

    emotion-music-system/
        ├── FluidR3_GM                     # サウンドフォントを格納

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

    pip install -r requirements.txt

- Python 3.8+
- OpenCV (`cv2`)
- ultralytics
- pygame（ローカルの音楽再生で使用予定）
- fluidsynth

---

## 🚀 使用予定モデル

- [YOLO11](https://github.com/ultralytics/ultralytics)
- 感情分類：Angry / Disgust / Fear / Happy /  Sad / Neutral / Contempt（8クラス）

## データセット

* Facial Expression Image Data AFFECTNET YOLO Format
  * [https://www.kaggle.com/datasets/fatihkgg/affectnet-yolo-format](https://www.kaggle.com/datasets/fatihkgg/affectnet-yolo-format)
    * We're going to use 8 emotions:
      * **Angry, Disgust, Fear, Happy,  Sad, Neutral, Contempt**

## 使用サウンドフォント
- The Fluid Release 3 General-MIDI Soundfont

## ゴール
