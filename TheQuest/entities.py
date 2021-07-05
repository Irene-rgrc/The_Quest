from TheQuest import ANCHO, ALTURA, FPS
import pygame as pg
import random
from enum import Enum
from pygame.locals import *
from pygame import mixer
from math import nextafter
import sys


class MarcadorH(pg.sprite.Sprite):
    
    plantilla = "{}"
    
    def __init__(self, x, y, justificado = "topleft", fontsize=25, color=(255,255,255)):
        super().__init__()
        self.fuente = pg.font.Font(None, fontsize)
        self.text = ""
        self.color = color
        self.x = x
        self.y = y
        self.justificado = justificado
        self.image = None
        self.rect = None
        
    def update(self, dt):
        self.image = self.fuente.render(self.plantilla.format(self.text), True, self.color)
        d = {self.justificado: (self.x, self.y)}
        self.rect = self.image.get_rect(**d)

class Ship(pg.sprite.Sprite):
    
    class Estado():
        viva = 0
        explotando = 1
        muerta = 2
        aterrizando = 3
    
    disfraces = ['cohete_on_wf.png',  'exp1.png','exp2.png','exp3.png','exp4.png','exp5.png']
    
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        
        self.estado = Ship.Estado.viva
        
        self.imagenes = self.cargaImagenes()
        self.imagen_actual = 0
        self.image = self.imagenes[self.imagen_actual]
        
        self.rect = self.image.get_rect(centerx = x, bottom = y)
        
        
        self.milisegundos_para_cambiar = 1000 // FPS * 5
        self.milisegundos_acumulados = 0 
        
        #Velocidad en la que se mueve en el eje y
        self.vy = 15
        
    def cargaImagenes(self):
        imagenes = []
        for fichero in self.disfraces:
            imagenes.append(pg.image.load('./Assets/ship/{}'.format(fichero)))
        return imagenes
    
    def girar_nave(self, angulo):
        self.image = pg.transform.rotozoom(self.WIN, angulo, 1)
        
    
    def draw(self, window):
        window.blit(self.imagen, (self.x,self.y))
    
    def prueba_colision(self, grupo):
        col = pg.sprite.spritecollide(self, grupo, False)
        if len(col) > 0:
            self.estado = Ship.Estado.explotando
            return 1
    
    def update(self, dt):
        
        if self.estado == Ship.Estado.viva:
            #Imagen
            self.imagen_actual = 0
            self.image = self.imagenes[self.imagen_actual]
            #Proceso de mover
            teclas_pulsadas = pg.key.get_pressed()
            if teclas_pulsadas[pg.K_DOWN]:
                self.rect.y += self.vy
                self.vy += 1
            if teclas_pulsadas[pg.K_UP]:
                self.rect.y -= self.vy
                self.vy += 1
            #Limites de la nave    
            if self.rect.top < 0:
                self.rect.top = 0
            elif self.rect.bottom > ALTURA:
                self.rect.bottom = ALTURA
            else:
                self.vy = 7

        elif self.estado == Ship.Estado.explotando:
            #Explosion
            self.milisegundos_acumulados += dt
            if self.milisegundos_acumulados >= self.milisegundos_para_cambiar:
                self.imagen_actual += 1
                self.milisegundos_acumulados = 0
                if self.imagen_actual >= (len(self.disfraces)):
                    self.estado = Ship.Estado.muerta
                    self.imagen_actual = 0
                self.image = self.imagenes[self.imagen_actual]
           
            
        
        elif self.estado == Ship.Estado.muerta:
            self.estado = Ship.Estado.viva
        
        else:
            self.estado = Ship.Estado.aterrizando
            self.rect.x += 5
            if self.rect.x > ANCHO//2:
                self.rect.x == ANCHO//2
                
            self.image = pg.transform.rotozoom(self.WIN, 180, 1)
            self.rect.x += 5
            if self.rect.x > ANCHO - 125:
                self.rect.x = ANCHO - 125
            #Animacion de fin de nivel
        
        #if Ship.Estado.aterrizando: Animacion con el planeta    


class Meteorito(pg.sprite.Sprite):
    
    disfraces = ['marron.png', 'gris.png', 'exp1.png','exp2.png','exp3.png','exp4.png','exp5.png']
    
    class Estado:
        viva = 0
        muerta = 1
        
    def __init__(self, x, y):
        super().__init__()
        self.imagenes = self.cargaImagenes()
        self.imagen_actual = random.randint(0,1)
        self.image = self.imagenes[self.imagen_actual]
        
        self.rect = self.image.get_rect(center=(x,y))
        
        self.x =  x
        self.y =  y
        
        self.vx = random.randint(5, 10)
        self.counter = 0
        
        self.estado = Meteorito.Estado.viva       
    
    def cargaImagenes(self):
        imagenes = []
        for fichero in self.disfraces:
            imagenes.append(pg.image.load("./Assets/meteor/{}".format(fichero)))
        return imagenes 
    
    
    def prueba_colision(self, grupo):
        col = pg.sprite.spritecollide(self, grupo, False)
        if len(col) > 0:
            self.estado = Meteorito.Estado.muerta
            return 1
    
    def update(self,dt):
        if self.estado == Meteorito.Estado.viva:
            self.rect.x -= self.vx
            if self.rect.left <= 0:
                self.rect.x = ANCHO + 10
                self.rect.y = random.randint(5, ALTURA)
                self.vx = random.randint(5, 10)
        
        else:
            self.estado = Meteorito.Estado.muerta
            return 10
            
    def subir_velocidad(self,level):
        self.vx += (int(level)*100)
        
class Planet(pg.sprite.Sprite):
    
    class Estado:
        lejos = 0
        cerca = 1
    
    def __init__(self,x,y):
        super().__init__()
        self.image = pg.image.load('./planet.png')
        
        self.rect = self.image.get_rect(center=(x,y))
        
        self.x =  x
        self.y =  y
        
        self.estado = Planet.Estado.lejos
        
    def update(self, dt):
        if self.estado == Planet.Estado.lejos:
            self.x =  ANCHO + 300
            self.y =  ALTURA//2
        if self.estado == Planet.Estado.cerca:
            self.x =  ANCHO + 100
            self.y =  ALTURA//2