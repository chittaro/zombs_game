import pygame

class AudioManager:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        self.sounds = {}

    def load(self, name, file):
        self.sounds[name] = pygame.mixer.Sound(f"assets/audio/{file}")

    def play(self, name):
        if name in self.sounds:
            self.sounds[name].play()
    
    def play_ongoing(self, name):
        if name in self.sounds:
            self.sounds[name].play(-1)

    def set_volume(self, name, volume):
        self.sounds[name].set_volume(volume)