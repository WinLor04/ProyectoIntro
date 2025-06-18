import random
import time
import os
import pygame

"""
Clase para integrar la lógica del modo de juego multijugador
"""

class ModoMultijugador:
    def __init__(self, Imagenes, botones_jugador1, botones_jugador2):
        """
        :param Imagenes: Lista con 18 imágenes (pygame.Surface), usadas como pares.
        :param botones_jugador1: Botones del tablero del Jugador 1.
        :param botones_jugador2: Botones del tablero del Jugador 2.
        """
        self.Imagenes = Imagenes
        self.TableroJugador1 = self._generar_tablero()
        self.TableroJugador2 = self._generar_tablero()
        
        # Botones pasados como parámetros
        self.botones_jugador1 = botones_jugador1
        self.botones_jugador2 = botones_jugador2
        
        self.TurnoActual = 1
        self.CartasSeleccionadas = []  # [(fila, col)]
        self.ParesEncontradosJ1 = []
        self.ParesEncontradosJ2 = []
        self.IntentosJ1 = 0
        self.IntentosJ2 = 0
        self.TiempoInicioTurno = time.time()
        self.TiempoRestante = 10
        self.LimiteTiempoTurno = 10

    def _generar_tablero(self):
        """
        Crea una matriz 6x6 con las 18 imágenes duplicadas y mezcladas.
        """
        pares = self.Imagenes * 2
        random.shuffle(pares)

        tablero = []
        idx = 0
        for fila in range(6):
            fila_actual = []
            for col in range(6):
                fila_actual.append(pares[idx])
                idx += 1
            tablero.append(fila_actual)
        return tablero

    def ReiniciarTiempo(self, bonificacion=0):
        """
        Reinicia el tiempo del turno actual, con opción de sumar segundos por acierto.
        """
        self.TiempoInicioTurno = time.time()
        self.TiempoRestante = self.LimiteTiempoTurno + bonificacion

    def TiempoAgotado(self):
        """
        Retorna True si el jugador actual se quedó sin tiempo.
        """
        tiempo_pasado = time.time() - self.TiempoInicioTurno
        return tiempo_pasado >= self.TiempoRestante

    @staticmethod
    def CargarImagenes():
        """
        Carga las imágenes de los jugadores.
        """
        Carpeta = os.path.join("assets", "Imágenes", "jugadores")
        Nombres = [
            "campbell.png", "cristiano.png", "iniesta.png", "keylor.png", "kroos.png", "lamine.png",
            "maradona.png", "marcelo.png", "mbappe.png", "messi.png", "modric.png", "neymar.png",
            "nazario.png", "pele.png", "ronaldinho.png", "ramos.png", "vini.png", "xavi.png"]
        
        Imagenes = []
        for nombre in Nombres:
            ruta = os.path.join(Carpeta, nombre)
            Imagen = pygame.image.load(ruta).convert_alpha()
            Imagen = pygame.transform.scale(Imagen, (80, 80))
            Imagenes.append(Imagen)
        return Imagenes
    
    def SeleccionarCasilla(self, jugador, fila, col):
        """
        Registra la selección de una casilla por el jugador actual.
        Retorna:
            - "esperando": aún falta seleccionar una segunda carta.
            - "acierto": si encontró pareja.
            - "fallo": si no coinciden.
        """
        tablero = self.TableroJugador1 if jugador == 1 else self.TableroJugador2
        pares_encontrados = self.ParesEncontradosJ1 if jugador == 1 else self.ParesEncontradosJ2

        self.CartasSeleccionadas.append((fila, col))

        if len(self.CartasSeleccionadas) < 2:
            return "esperando"

        (f1, c1), (f2, c2) = self.CartasSeleccionadas
        img1 = tablero[f1][c1]
        img2 = tablero[f2][c2]

        # Registrar intento
        if jugador == 1:
            self.IntentosJ1 += 1
        else:
            self.IntentosJ2 += 1

        if img1 == img2:
            pares_encontrados.append((f1, c1))
            pares_encontrados.append((f2, c2))
            self.CartasSeleccionadas.clear()
            return "acierto"
        else:
            return "fallo"