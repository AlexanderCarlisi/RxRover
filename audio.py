from robot_hat import Music,TTS
import time

class Audio:

    camera = None
    music = None
    tts = None

    patrickDir = "/home/lilrobo/Documents/Code/PatrickVoice/"
    patrickFiles = [patrickDir+"patrick1.mp3", patrickDir+"patrick2.mp3", patrickDir+"patrick3.mp3"]
    patrickIndex = 0
    audioEnd = 0

    def __init__(self, _camera):
        self.music = Music()
        self.music.music_set_volume(100)
        self.tts = TTS()
        self.camera = _camera

    def periodic(self):
        if self.camera.detectsFace and time.time() > self.audioEnd:
            self.music.sound_play(self.patrickFiles[self.patrickIndex])
            self.audioEnd = time.time() + self.music.sound_length(self.patrickFiles[self.patrickIndex])
            self.patrickIndex += 1
            if self.patrickIndex >= len(self.patrickFiles):
                self.patrickIndex = 0