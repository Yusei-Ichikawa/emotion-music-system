import pygame
import json
import time
import os

# ==== 初期設定 ====
CONFIG_PATH = "emotion_music_config.json"
EMOTION_FILE = "latest_emotion.txt"  # 推論結果が書き込まれる想定ファイル

# ==== 音楽の初期化 ====
pygame.mixer.init()
current_emotion = None

# ==== 音楽マッピングの読み込み ====
with open(CONFIG_PATH, "r") as f:
    emotion_to_music = json.load(f)

# ==== 音楽再生関数 ====
def play_music(emotion):
    global current_emotion
    if emotion != current_emotion and emotion in emotion_to_music:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(emotion_to_music[emotion])
        pygame.mixer.music.play(-1)
        current_emotion = emotion
        print(f"🎵 {emotion} の音楽を再生中")

# ==== ループで感情を監視して音楽を再生 ====
try:
    while True:
        if os.path.exists(EMOTION_FILE):
            with open(EMOTION_FILE, "r") as f:
                emotion = f.read().strip()
            if emotion:
                play_music(emotion)
        time.sleep(1)

except KeyboardInterrupt:
    print("🛑 停止されました")
    pygame.mixer.music.stop()
