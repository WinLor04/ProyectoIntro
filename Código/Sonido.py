import pygame
import os

"""
Esta es una clase para gestionar todos los sonidos y música del juego.
Permite reproducir efectos de sonido y música de fondo.
"""
class Sonido:
    
    def __init__(self):
        pygame.mixer.init()
        ruta = os.path.join("assets", "Audio")
        # Cargar efectos de sonido
        self.hover_sonido = pygame.mixer.Sound(os.path.join(ruta, "select.wav"))
        self.click_sonido = pygame.mixer.Sound(os.path.join(ruta, "click.wav"))
        self.atras_sonido = pygame.mixer.Sound(os.path.join(ruta, "volver.mp3"))
        self.check_sonido = pygame.mixer.Sound(os.path.join(ruta, "check.mp3"))
        self.error_sonido = pygame.mixer.Sound(os.path.join(ruta, "error.mp3"))

        # Ajustar volumen de los efectos
        self.check_sonido.set_volume(0.5)
        self.error_sonido.set_volume(0.5)
        self.atras_sonido.set_volume(0.5)
        self.hover_sonido.set_volume(0.5)
        self.click_sonido.set_volume(0.5)
        self.hover_reproducido = False  # Controla si el sonido hover ya fue reproducido

    def reproducir_atras(self):
        """Reproduce el sonido de retroceso o volver."""
        self.atras_sonido.play()

    def reproducir_hover(self):
        """
        Reproduce el sonido de hover solo una vez hasta que se reinicie.
        Evita que el sonido se repita constantemente mientras el cursor está sobre un botón.
        """
        if not self.hover_reproducido:
            self.hover_sonido.play()
            self.hover_reproducido = True

    def reproducir_click(self):
        """Reproduce el sonido de click."""
        self.click_sonido.play()

    def reset_hover(self):
        """Permite que el sonido de hover se pueda reproducir de nuevo."""
        self.hover_reproducido = False
        
    def reproducir_musica(self, loop=True):
        """
        Reproduce la música de fondo principal si no está sonando ya.
        :param loop: Si True, la música se repite indefinidamente.
        """
        if not pygame.mixer.music.get_busy():
            ruta_musica = os.path.join("assets", "Audio", "HeatWaves.mp3")
            pygame.mixer.music.load(ruta_musica)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1 if loop else 0)

    def detener_musica(self):
        """Detiene la música de fondo."""
        pygame.mixer.music.stop()

    def reproducir_cancion(self, nombre_archivo, volumen=0.3, mute=False):
        """
        Reproduce una canción específica.
        :param nombre_archivo: Nombre del archivo de audio a reproducir.
        :param volumen: Volumen de reproducción.
        :param mute: Si True, la canción se reproduce en silencio.
        """
        ruta = os.path.join("assets", "Audio", nombre_archivo)
        pygame.mixer.music.load(ruta)
        pygame.mixer.music.set_volume(0 if mute else volumen)
        pygame.mixer.music.play(-1)

    def reproducir_check(self):
        """Reproduce el sonido de confirmación o acierto."""
        self.check_sonido.play()

    def reproducir_error(self):
        """Reproduce el sonido de error o fallo."""
        self.error_sonido.play()