# !/usr/bin/python
import sys
import os

# importing numpy and pandas
import numpy as np
import pandas as pd

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
# import pygame
import pygame
from pygame.locals import *

import soundfile as sf

# Logging configuration
import logging
logging.basicConfig(filename="errlog.log",
                    filemode="a",
                    format="(%(asctime)s)  | %(name)s | %(levelname)s:%(message)s",
                    datefmt="%d  %B  %Y , %H:%M:%S",
                    level=os.environ.get("LOGLEVEL", "INFO"))

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
        self.crash_sound = pygame.mixer.Sound("./src/crash.wav")

    def loadFile(self, path, firstTime=True):
        # Save prev pos
        # pos = 0
        # if not firstTime:
        #     pos = self.getPosition()

        # Stop prev sound
        pygame.mixer.music.unload()
        pygame.mixer.music.stop()
        
        # Load new sound
        pygame.mixer.music.load(path)
        try:
            pygame.mixer.music.play(0)
        except:
            logging.error("Failed to play a new sound.")

    def loadArray(self, array):
        pygame.mixer.music.stop()
        array = self.arrayTo2D(array)
        musicSound = pygame.sndarray.make_sound(array)
        self.Channel.play(musicSound)

    def arrayTo2D(self, array):
        try:
            if np.ndim(array) == 1:
                array = array.astype(np.float32)
                array = np.array(array)
                array = np.repeat(array.reshape(len(array), 1), 2, axis = 1)
        except:
            logging.error("Failed to transform 1D array to 2D float array.")

        return array

    def writeFile(self, path, equalizedArr):
        pygame.mixer.music.unload()
        pygame.mixer.music.stop()
        try :
            sf.write("./src/temp.wav", equalizedArr, 44100, closefd=True)
        except:
            logging.error("Failed to write temporarily sound file.")

    def pause(self):
        self.Channel.pause()
        pygame.mixer.music.pause()

    def unpause(self):
        self.Channel.unpause()
        pygame.mixer.music.unpause()
    
    def rewind(self):
        
        pygame.mixer.music.play(-1,0)

    def setVolume(self, volume):
        pygame.mixer.music.set_volume(volume/100)
        self.Channel.set_volume(volume/100)
        
    def getPosition(self):
        return pygame.mixer.music.get_pos()

    def setPosition(self, pos):
        try:
            pygame.mixer.music.set_pos(pos)
        except:
            logging.error("Failed to getting current position.")

    def getData(self):
        return pygame.mixer.Sound.get_raw()

    def crash(self):
        pygame.mixer.Sound.play(self.crash_sound)
        pygame.mixer.music.stop()
        logging.error("Sound has crashed.")