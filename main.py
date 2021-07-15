     
from TheQuest.game import Thequest
import pygame as pg
from TheQuest.escenes import Game
from TheQuest import ANCHO, ALTURA


if __name__ == '__main__':
    pg.init()
    controler = Thequest()
    controler.start()
    
    
