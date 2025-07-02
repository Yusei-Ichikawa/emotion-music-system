あなたがこれまで構築した「Emotion Music System」の骨組み実装について、**他のエンジニアに引き継げるレベルでの詳細説明**を以下にまとめます。

---

# 🧾 Emotion Music System：骨組み実装ドキュメント

---

## 🎯 プロジェクト概要

本システムは、ユーザーの**表情から感情（4分類）をリアルタイム推論**し、それに対応する**音楽をローカルで自動再生する**ことを目的としています。

---

## 📂 ディレクトリ構成（現在）

emotion-music-system/


├── send_image_to_colab.py          # ローカル：画像をColabに送信


├── play_music_by_emotion.py        # ローカル：感情に応じて音楽再生


├── emotion_music_config.json       # 感情と音楽の対応設定


├── latest_emotion.txt              # 感情結果を一時保存（自動生成される）


├── .gitignore                      # Git除外ファイル（music/ ディレクトリを含む）


└── README.md                       # プロジェクト概要

## 🧠 現在実装されたファイルの詳細

---

### ✅ 1. `send_image_to_colab.py`

 **役割** ：

* ノートPCのWebカメラから画像を取得
* Base64でエンコードしてGoogle Colab上のFlaskサーバ（`/predict`）に送信
* 感情の推論結果を受信し、`latest_emotion.txt` に保存

 **備考** ：

* `COLAB_URL` は ngrok 経由でColabに公開されたFlaskサーバのURLに差し替える必要あり。
* 推論インターバル（秒数）なども調整可能。

---

### ✅ 2. `colab_flask_server.py`（※ローカルには未保存、Colabで使用）

 **役割** ：

* Google Colab上で起動
* `POST /predict` エンドポイントで画像を受信し、YOLOモデルで推論
* 感情（`angry`, `sad`, `happy`, `neutral`）のうち最も信頼度の高い1件を返却

 **備考** ：

* `emotion_yolo.pt` は事前学習済のYOLOモデル（4クラス）を使用。
* Flask + ngrok を組み合わせて外部公開可能。

---

### ✅ 3. `play_music_by_emotion.py`

 **役割** ：

* `latest_emotion.txt` を定期的に監視
* 感情が変化したら対応する音楽ファイルを再生・切替
* 音楽のループ再生に対応（pygame使用）

 **備考** ：

* 現在はファイル監視による単純実装。今後ソケットや非同期処理に置き換え可能。

---

### ✅ 4. `emotion_music_config.json`

 **役割** ：

* 感情とローカル音楽ファイルの対応を定義

 **例** ：

{
  "happy": "music/happy.mp3",
  "sad": "music/sad.mp3",
  "angry": "music/angry.mp3",
  "neutral": "music/neutral.mp3"
}

---

### ✅ 5. `.gitignore`

 **内容** ：

music/
__pycache__/
*.pyc
*.log
.env
.vscode/

* 音楽ファイルや一時ファイル、仮想環境などをGitから除外。
* `music/` ディレクトリはGit管理対象外。

---

## ⚙️ 現在の制限・今後の対応タスク（後任者向け）

| 項目              | 内容                                                                       |
| ----------------- | -------------------------------------------------------------------------- |
| 🔸 YOLOモデル     | `emotion_yolo.pt`は事前にColabにアップロードしておく必要あり             |
| 🔸 音楽ファイル   | `music/`ディレクトリに対応ファイルを用意（例：`happy.mp3`）            |
| 🔸 Flaskサーバ    | Colab側で `flask-ngrok`を使用し、ngrok経由で公開する必要あり             |
| 🔸 推論間隔       | `send_image_to_colab.py`の `CAPTURE_INTERVAL`で調整可能                |
| 🔸 データ連携方法 | 現在は `latest_emotion.txt`によるファイルベース。後にHTTP/ソケット化可能 |

---

## 🧩 推奨次ステップ（後任エンジニア向け）

1. `emotion_yolo.pt` をColabにアップロード＆Flaskサーバを起動
2. ローカルで `send_image_to_colab.py` 実行（ngrok URLを反映）
3. `play_music_by_emotion.py` を同時実行し、感情に応じた音楽再生を確認
4. （任意）emotion変更が頻繁な場合はスムージング機構を導入
