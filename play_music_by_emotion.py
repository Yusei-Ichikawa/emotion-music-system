import pygame
import json
import time

with open("emotion_music_config.json") as f:
    emotion_to_music = json.load(f)

pygame.mixer.init()
current_emotion = None

def play_music(emotion):
    global current_emotion
    if emotion != current_emotion:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(emotion_to_music[emotion])
        pygame.mixer.music.play(-1)
        current_emotion = emotion
        print(f"🎵 {emotion} の音楽を再生中")

# サンプル：受信した感情を使って再生
while True:
    with open("latest_emotion.txt") as f:  # 外部プロセスで書き込まれた感情
        emotion = f.read().strip()
    if emotion in emotion_to_music:
        play_music(emotion)
    time.sleep(1)
