from TheQuest import ANCHO, ALTURA, FPS
from TheQuest.escenes import Portada, Game, Controles, Gameacabado
import pygame as pg

pg.init()

class Thequest():
    def __init__(self):
        WIN = pg.display.set_mode((ANCHO,ALTURA))
        self.escenas = [Portada(WIN),Controles(WIN) ,Game(WIN), Gameacabado(WIN) ]  #Controlador de escenas
        self.escena_activa = 0
        
    def start(self):
        while True:
            la_escena = self.escenas[self.escena_activa]
            print(la_escena)
            la_escena.reset()
            la_escena.main_loop()

            self.escena_activa += 1
            if self.escena_activa >= len(self.escenas):
                self.escena_activa = 0

            

            