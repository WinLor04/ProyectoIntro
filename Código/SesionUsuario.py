class SesionUsuario:
    def __init__(self):
        self.nombre = None
        self.metodo = None  # "facial" o "clave"

    def iniciar_sesion(self, nombre, metodo):
        """
        Registra al usuario con su método de acceso.
        """
        self.nombre = nombre
        self.metodo = metodo

    def esta_autenticado(self):
        """
        Verifica si hay un usuario logueado.
        """
        return self.nombre is not None and self.metodo in ("facial", "clave")

    def puede_guardar_recompensa(self):
        """
        Solo los usuarios logueados pueden recibir recompensas.
        """
        return self.esta_autenticado()

    def obtener_datos(self):
        return {"nombre": self.nombre, "metodo": self.metodo}

    def cerrar_sesion(self):
        self.nombre = None
        self.metodo = None