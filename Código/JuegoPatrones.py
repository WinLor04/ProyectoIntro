import random
import time

"""
Clase que representa un juego de patrones en un tablero de casillas.
Permite generar un patrón aleatorio de casillas y verificar si un patrón dado coincide con el generado.
"""

class JuegoPatrones:

    def __init__(self, Filas=6, Columnas=6):
        self.Filas = Filas
        self.Columnas = Columnas
        self.Tablero = [(i, j) for i in range(Filas) for j in range(Columnas)]
        self.LongitudPatron = 3
        self.Patron = []
        self.TiempoInicio = None
        self.TiempoUltimoClick = None
        self.TiempoTotalMax = 12  # segundos
        self.TiempoEntreCasillasMax = 2  # segundos

    def GenerarPatronInicial(self):
        """
        Genera una secuencia aleatoria de casillas únicas del tablero.
        """
        self.Patron = random.sample(self.Tablero, self.LongitudPatron)
    
    def AgregarACasilla(self):
        """
        Agrega una casilla nueva sin repetir, para aumentar dificultad.
        """
        disponibles = [pos for pos in self.Tablero if pos not in self.Patron]
        if disponibles:
            nueva = random.choice(disponibles)
            self.Patron.append(nueva)

    def ObtenerPatron(self):
        """
        Devuelve el patrón actual que debe recordar el jugador.
        """
        return self.Patron
    
    def IniciarVerificacion(self):
        """
        Inicializa las variables necesarias para verificar la secuencia del jugador.
        """
        self.IndiceActual = 0
        self.Resultado = None  # None: en progreso, True: éxito, False: error

    def VerificarCasilla(self, Casilla):
        """
        Verifica si la casilla seleccionada por el jugador es correcta, y valida el tiempo.
        """

        if self.Resultado is not None:
            return 'finalizado'

        tiempo_actual = time.time()

        # Verificar tiempo total
        if self.TiempoInicio is not None and tiempo_actual - self.TiempoInicio > self.TiempoTotalMax:
            self.Resultado = False
            return 'tiempo_agotado'

        # Verificar tiempo entre casillas
        if self.TiempoUltimoClick is not None and tiempo_actual - self.TiempoUltimoClick > self.TiempoEntreCasillasMax:
            self.Resultado = False
            return 'muy_lento'
        
        # Verificar si la casilla es correcta
        if Casilla == self.Patron[self.IndiceActual]:
            self.IndiceActual += 1
            self.TiempoUltimoClick = tiempo_actual
            if self.IndiceActual == len(self.Patron):
                self.Resultado = True
                return 'completado'
            return 'correcto'
        else:
            self.Resultado = False
            return 'incorrecto'
    
    def IniciarTemporizador(self):
        """
        Marca el inicio del intento del jugador.
        """
        self.TiempoInicio = time.time()
        self.TiempoUltimoClick = self.TiempoInicio
    
    def ReiniciarTodo(self):
        """
        Restaura el estado del juego al nivel inicial (3 casillas).
        """
        self.LongitudPatron = 3
        self.Resultado = None
        self.IndiceActual = 0
        self.Patron = []
        self.TiempoInicio = None
        self.TiempoUltimoClick = None