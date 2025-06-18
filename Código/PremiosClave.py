import os
import json

"""
Clase utilizada para la logica donde se guarda el puntaje del jugador
sii inicio por el método: clave
"""

class PremiosClave:
    ARCHIVO = "premios_clave.json"  # Archivo donde se guardan los premios

    @staticmethod
    def asegurar_archivo():
        """Crea el archivo si no existe."""
        if not os.path.exists(PremiosClave.ARCHIVO):
            with open(PremiosClave.ARCHIVO, "w", encoding="utf-8") as f:
                json.dump({}, f)

    @staticmethod
    def otorgar_premio(nombre, monto):
        """Suma el premio al usuario correspondiente."""
        PremiosClave.asegurar_archivo()
        with open(PremiosClave.ARCHIVO, "r+", encoding="utf-8") as f:
            datos = json.load(f)
            datos[nombre] = datos.get(nombre, 0) + monto
            f.seek(0)
            json.dump(datos, f, indent=4)
            f.truncate()
        print(f"💰 Premio por clave: {nombre} +${monto} (Total: ${datos[nombre]})")

    @staticmethod
    def obtener_total(nombre):
        """Devuelve cuánto dinero lleva el usuario."""
        PremiosClave.asegurar_archivo()
        with open(PremiosClave.ARCHIVO, "r", encoding="utf-8") as f:
            datos = json.load(f)
            return datos.get(nombre, 0)