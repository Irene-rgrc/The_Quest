import pygame as pg
from TheQuest import ANCHO, ALTURA, levels, FPS
from TheQuest.entities import MarcadorH, Ship, Meteorito, Planet
from math import nextafter
import sys
import random
from enum import Enum
from pygame.locals import *
from pygame import mixer

class Escene():
    def __init__(self, WIN):
        self.WIN = WIN
        self.todoGrupo = pg.sprite.Group()
        self.reloj = pg.time.Clock()

    def reset(self):
        pass

    def maneja_eventos(self):
        for evento in pg.event.get():
            if evento.type == pg.QUIT or \
                evento.type == pg.KEYDOWN and evento.key == pg.K_q:
                    pg.quit()
                    sys.exit()


    def main_loop(self):
        pass
    
class Game(Escene):
    def __init__(self, WIN):
        super().__init__(WIN)
        self.grupoJugador = pg.sprite.Group()
        self.grupoMeteoritos = pg.sprite.Group()
        
        self.cuentaPuntos = MarcadorH(10,10, fontsize=50)
        self.cuentaVidas = MarcadorH(1180, 10, "topright", 50, (255, 255, 255))
        self.cuentaVidas.plantilla = '{}'
        self.caption = pg.display.set_caption('The quest') # Nombre de la ventana
        
        #self.estado = Meteorito.Estado.viva
        self.meteorito = Meteorito(x = ANCHO + 5,y = random.randint(0,ALTURA - 60))
        self.grupoMeteoritos.add(self.meteorito)
        
        self.estado = Ship.Estado.viva
        self.spaceship = Ship(x=125 , y= ALTURA//2)
        self.grupoJugador.add(self.spaceship)
        
        #self.todoGrupo = pg.sprite.Group()
        self.todoGrupo.add(self.grupoJugador)
        
        self.background = pg.image.load('./Assets/space.png')
        self.musica_background = pg.mixer.Sound('background.wav')
        
        self.planet = Planet(ANCHO//2, ALTURA//2)
        self.planeta = Planet.Estado.lejos
        self.todoGrupo.add(self.planet)
        
        #Las pongo?
        self.puntuacion = 0
        self.vidas = 3
        self.level = 0
        
        self.contador = 0
    
    def reset(self):
        self.musica_background.stop()
        self.estado = Ship.Estado.viva
        self.planeta = Planet.Estado.lejos
        self.n = 3
        self.puntuacion = 0
        self.vidas = 3
        self.level = 0
        self.todoGrupo.remove(self.grupoMeteoritos)
        self.grupoMeteoritos.empty()
        self.todoGrupo.remove(self.cuentaPuntos, self.cuentaVidas)
        self.todoGrupo.add(self.cuentaPuntos, self.cuentaVidas)
    
        
    def main_loop(self):
        reloj = pg.time.Clock()
        game_over = False
        self.musica_background.play(-1)
        
        self.n = 2
        for i in range(self.n):
                self.meteorito = Meteorito(x = ANCHO + 5,y = random.randint(0,ALTURA - 60))
                self.grupoMeteoritos.add(self.meteorito)
                self.todoGrupo.add(self.grupoMeteoritos)
                
    
        while not game_over and self.vidas > 0:
            dt = reloj.tick(FPS)
            self.contador += dt
            self.maneja_eventos()
        
            self.cuentaPuntos.text = self.puntuacion
            self.cuentaVidas.text = self.vidas
            
            for nave in self.grupoJugador:
                if nave.estado == Ship.Estado.viva:
                    nave.prueba_colision(self.grupoMeteoritos)
                if nave.estado == Ship.Estado.explotando:
                    mixer.music.load('boom.wav')
                    mixer.music.play()
                if nave.estado == Ship.Estado.muerta:
                    self.vidas -= 1
                             
                else:
                    for meteorito in self.grupoMeteoritos:
                        if meteorito.rect.x < 10:
                            self.puntuacion += 5 
                            
                    if (self.contador)/1000 > 5:
                        for meteorito in self.grupoMeteoritos:
                            if meteorito.rect.x < 10:
                                self.grupoMeteoritos.remove(meteorito)
                                self.todoGrupo.remove(meteorito)
                        self.planeta = Planet.Estado.cerca
                        self.estado = Ship.Estado.aterrizando
                        self.final = MarcadorH(ANCHO// 2, ALTURA//2, 'center', 60, (255,255,255))
                        self.final.text = ('Pulsa espacio para continuar')
                        self.todoGrupo.add(self.final)
                        teclas_pulsadas = pg.key.get_pressed()
                        if teclas_pulsadas[pg.K_SPACE]:
                            self.estado = Ship.Estado.viva
                            self.planeta = Planet.Estado.cerca
                            self.contador = 0
                            self.puntuacion = 0
                            self.level += 1
                            meteorito.subir_velocidad(levels[self.level])
                            self.n += 1
                            for meteorito in self.grupoMeteoritos:
                                for i in range(self.n):
                                    self.meteorito = Meteorito(x = ANCHO + 5,y = random.randint(0,ALTURA - 60))
                                    self.grupoMeteoritos.add(self.meteorito)
                                    self.todoGrupo.add(self.grupoMeteoritos)
                         
                                
                
            self.todoGrupo.update(dt)
                  
            self.WIN.blit(self.background, (0,0))
            self.todoGrupo.draw(self.WIN)
            
            pg.display.flip()
        self.musica_background.stop()
        
            


class Portada(Escene):
    def __init__(self,WIN):
        super().__init__(WIN)
        self.titulo = MarcadorH(ANCHO//2, ALTURA//2 - 300, 'center', 100, (200,0,128))
        self.titulo.text = ('The quest')
        self.instrucciones = MarcadorH(ANCHO - 200, ALTURA- 200, 'topright', 50, (50,0,50))
        self.instrucciones.text = ('PULSA ESPACIO PARA COMENZAR')
        self.historia1 = MarcadorH(ANCHO//2, ALTURA// 2 - 100, 'center', 40, (255,255,255))
        self.historia1.text = ('La búsqueda comienza en un planeta tierra moribundo por el cambio climático.')
        self.historia2 = MarcadorH(ANCHO//2, ALTURA// 2 , 'center', 40, (255,255,255))
        self.historia2.text = ('Partiremos a la búsqueda de un planeta compatible con la vida humana,')
        self.historia3 = MarcadorH(ANCHO//2, ALTURA// 2 + 100, 'center', 40, (200,100,200))
        self.historia3.text = ('para colonizarlo')
        self.todoGrupo.add(self.titulo, self.instrucciones, self.historia1, self.historia2, self.historia3)
        
    def main_loop(self):
        game_over = False
        while not game_over:
            dt = self.reloj.tick(FPS)
            
            self.maneja_eventos()
            
            teclas_pulsadas = pg.key.get_pressed()
            if teclas_pulsadas[pg.K_SPACE]:
                game_over = True
                
            self.todoGrupo.update(dt)
            self.WIN.fill((0,0,0))
            self.todoGrupo.draw(self.WIN)
            
            pg.display.flip()
            
class Controles(Escene):
    def __init__(self,WIN):
        super().__init__(WIN)
        self.instrucciones = MarcadorH(50, 50, 'topleft', 100, (0,255,255))
        self.instrucciones.text = ('Controles de la nave')
        self.controlup = MarcadorH(400, ALTURA//2 - 200, 'center', 50, (255,255,255))
        self.controlup.text = ('- Flecha hacia arriba: Subir la nave')
        self.controldown = MarcadorH(400, ALTURA//2, 'center', 50, (255,255,255))
        self.controldown.text = ('- Flecha hacia abajo: Bajar la nave')
        self.objetivo = MarcadorH(50, ALTURA//2 + 200, 'topleft', 40, (255,255,0))
        self.objetivo.text = ('El objetivo es no dejarse tocar por los meteoritos. Pulsa la letra a para comenzar')
        self.todoGrupo.add(self.instrucciones, self.controlup, self.controldown, self.objetivo)
        
    def main_loop(self):
        game_over = False
        while not game_over:
            dt = self.reloj.tick(FPS)
            
            self.maneja_eventos()
            
            teclas_pulsadas = pg.key.get_pressed()
            if teclas_pulsadas[pg.K_a]:
                game_over = True
                
            self.todoGrupo.update(dt)
            self.WIN.fill((0,0,0))
            self.todoGrupo.draw(self.WIN)
            
            pg.display.flip()
    
class Gameacabado(Escene):
    def __init__(self,WIN):
        super().__init__(WIN)
        self.instrucciones = MarcadorH(ANCHO//2, ALTURA//2, 'center', 150, (255,0,0))
        self.instrucciones.text = ('GAMEOVER')
        self.rempezar = MarcadorH(ANCHO//2 + 200, ALTURA//2 + 200, 'center', 50, (0,0,0))
        self.rempezar.text = ('Pulsa a para volver a empezar')
        self.todoGrupo.add(self.instrucciones, self.rempezar)
        
    def main_loop(self):
        game_over = False
        while not game_over:
            dt = self.reloj.tick(FPS)
            
            self.maneja_eventos()
            
            teclas_pulsadas = pg.key.get_pressed()
            if teclas_pulsadas[pg.K_a]:
                game_over = True
                
            self.todoGrupo.update(dt)
            self.WIN.fill((255,255,255))
            self.todoGrupo.draw(self.WIN)
            
            pg.display.flip()