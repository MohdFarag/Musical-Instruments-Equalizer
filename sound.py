# !/usr/bin/python

# importing numpy and pandas
from matplotlib.pyplot import pause
import numpy as np
import pandas as pd
import sys

import pygame
from pygame.locals import *
import soundfile as sf

class music():
    """Main Plot."""
    def __init__(self):
        
        """Initializer."""
        super().__init__()
        pygame.mixer.init(44100, -16, 2, 512)
        pygame.init()
        pygame.mixer.set_num_channels(1)
        self.Channel = pygame.mixer.Channel(0)
        
        # Variables
        self.data = []
        self.crash_sound = pygame.mixer.Sound("src/crash.wav")

    def loadFile(self, path, firstTime=True):
        # Save prev pos
        pos = 0
        if not firstTime:
            pos = self.getPosition()

        # Stop prev sound
        pygame.mixer.music.unload()
        pygame.mixer.music.stop()
        
        # Load new sound
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)

    def loadArray(self, array):
        pygame.mixer.music.stop()
        array = self.arrayEdit(array)
        musicSound = pygame.sndarray.make_sound(array)
        self.Channel.play(musicSound)

    def arrayEdit(self, array):
        if np.ndim(array) == 1:
            array = array.astype(np.float32)
            array = np.array(array)
            array = np.repeat(array.reshape(len(array), 1), 2, axis = 1)

        return array

    def writeArray(self, path, equalizedArr):
        pygame.mixer.music.unload()
        pygame.mixer.music.stop()
        sf.write("src/temp.wav", equalizedArr, 44100, closefd=True)

    def pause(self):
        self.Channel.pause()
        pygame.mixer.music.pause()

    def unpause(self):
        self.Channel.unpause()
        pygame.mixer.music.unpause()
    
    def rewind(self):
        pygame.mixer.music.play()

    def setVolume(self, volume):
        pygame.mixer.music.set_volume(volume/100)
        self.Channel.set_volume(volume/100)
        
    def getPosition(self):
        return pygame.mixer.music.get_pos()

    def setPosition(self, pos):
        pygame.mixer.music.set_pos(pos)

    def getData(self):
        return pygame.mixer.Sound.get_raw()

    def crash(self):
        pygame.mixer.Sound.play(self.crash_sound)
        pygame.mixer.music.stop()