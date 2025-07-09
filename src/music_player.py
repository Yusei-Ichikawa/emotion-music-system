import pygame
import os

# 音楽再生用クラス
class MusicPlayer:
    def __init__(self, music_dir='music'):
        pygame.mixer.init()
        self.music_dir = music_dir
        self.current_audio_label = None

    def play(self, expression):
        # 音楽ファイルのパスを生成
        audio_path = os.path.join(self.music_dir, expression.lower() + '.mp3')
        if self.current_audio_label != expression:
            if self.current_audio_label is not None:
                pygame.mixer.music.stop()
            if os.path.exists(audio_path):
                pygame.mixer.music.load(audio_path)
                pygame.mixer.music.play()
                self.current_audio_label = expression

    def stop(self):
        pygame.mixer.music.stop()
        self.current_audio_label = None
