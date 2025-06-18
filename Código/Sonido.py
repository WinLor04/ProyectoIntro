import pygame
import os

class Sonido:
    def __init__(self):
        pygame.mixer.init()
        ruta = os.path.join("assets", "Audio")
        self.hover_sonido = pygame.mixer.Sound(os.path.join(ruta, "select.wav"))
        self.click_sonido = pygame.mixer.Sound(os.path.join(ruta, "click.wav"))
        self.atras_sonido = pygame.mixer.Sound(os.path.join(ruta, "volver.mp3"))
        self.check_sonido = pygame.mixer.Sound(os.path.join(ruta, "check.mp3"))
        self.error_sonido = pygame.mixer.Sound(os.path.join(ruta, "error.mp3"))

        self.check_sonido.set_volume(0.5)
        self.error_sonido.set_volume(0.5)

        self.atras_sonido.set_volume(0.5)
        self.hover_sonido.set_volume(0.5)
        self.click_sonido.set_volume(0.5)
        self.hover_reproducido = False  

    def reproducir_atras(self):
        self.atras_sonido.play()

    def reproducir_hover(self):
        if not self.hover_reproducido:
            self.hover_sonido.play()
            self.hover_reproducido = True

    def reproducir_click(self):
        self.click_sonido.play()

    def reset_hover(self):
        self.hover_reproducido = False
        
    def reproducir_musica(self, loop=True):
        if not pygame.mixer.music.get_busy():
            ruta_musica = os.path.join("assets", "Audio", "HeatWaves.mp3")
            pygame.mixer.music.load(ruta_musica)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1 if loop else 0)

    def detener_musica(self):
        pygame.mixer.music.stop()

    def reproducir_cancion(self, nombre_archivo, volumen=0.3, mute=False):
        ruta = os.path.join("assets", "Audio", nombre_archivo)
        pygame.mixer.music.load(ruta)
        pygame.mixer.music.set_volume(0 if mute else volumen)
        pygame.mixer.music.play(-1)
    def reproducir_check(self):
        self.check_sonido.play()

    def reproducir_error(self):
        self.error_sonido.play()

    
    
