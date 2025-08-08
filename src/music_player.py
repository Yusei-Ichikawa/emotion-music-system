import pygame
import os

music_dir_1 = "music/ver1"
music_dir_2 = "music/ver2"

# 音楽再生用クラス
class MusicPlayer:
    def __init__(self, music_dir=music_dir_1):
        pygame.mixer.init()
        self.music_dir = music_dir
        self.current_audio_label = None

    def play(self, expression):
        # "Anger": # 怒り: 赤
        # "Disgust": # 嫌悪: 濃い緑
        # "Fear": # 恐れ: 紫
        # "Happy": # 喜び: 黄色
        # "Sad": # 悲しみ; 水色
        # "Surprise": # 驚き: 黄緑
        # "Neutral": # 中立: グレー
        # "Contempt": # 軽蔑: 青
        # group1: happy
        # group2: anger, fear
        # group3: sad, disgust, contempt
        # group4: surprise
        # group5: neutral
        # 音楽ファイルのパスを生成
        # audio_path = os.path.join(self.music_dir, expression.lower() + '.mp3')
        if expression == "Anger" or expression == "Fear":
            expression = "Anger"
        elif expression == "sad" or expression == "Disgust" or expression == "Contempt":
            expression = "Fear"
        audio_path = os.path.join(self.music_dir, expression.lower() + '.mid')
        if self.current_audio_label != expression:
            if self.current_audio_label is not None:
                pygame.mixer.music.stop()
            if os.path.exists(audio_path):
                pygame.mixer.music.load(audio_path)
                pygame.mixer.music.play(-1)
                self.current_audio_label = expression

    def stop(self):
        pygame.mixer.music.stop()
        self.current_audio_label = None
