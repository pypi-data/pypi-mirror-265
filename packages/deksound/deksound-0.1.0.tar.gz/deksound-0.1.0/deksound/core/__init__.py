import os
import time
from pathlib import Path
from just_playback import Playback as PlaybackBase


class Playback(PlaybackBase):
    def play_sync(self):
        self.play()
        self.waiting()

    def waiting(self):
        while self.playing:
            time.sleep(0)


def play_file(filepath):
    playback = Playback()
    playback.load_file(filepath)
    playback.play_sync()


path_res = Path(__file__).resolve().parent / 'res'


def play_res(name, path=None):
    path = path or path_res
    for file in os.listdir(path):
        if os.path.splitext(file)[0] == name:
            play_file(os.path.join(path, file))
