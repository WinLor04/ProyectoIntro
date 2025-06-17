class Jugador:
    def __init__(self, nombre):
        """
        Inicializa un jugador con su nombre, intentos y aciertos.
        """
        self.Nombre = nombre
        self.Intentos = 0
        self.Aciertos = 0

    def RegistrarIntento(self):
        """
        Incrementa en 1 el número de intentos del jugador.
        """
        self.Intentos += 1

    def RegistrarAcierto(self):
        """
        Incrementa en 1 el número de aciertos del jugador.
        """
        self.Aciertos += 1