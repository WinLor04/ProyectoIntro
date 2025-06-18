import os
import json

"""
Clase utilizada para la logica donde se guarda el puntaje del jugador
sii inicio por el método: facial
"""

class PremiosFaciales:
    # Ruta del archivo que guarda los premios acumulados por usuario facial
    ARCHIVO = "premios_facial.json"

    @staticmethod
    def asegurar_archivo():
        """
        Verifica si el archivo de premios existe.
        Si no existe, lo crea vacío como un diccionario JSON.
        """
        if not os.path.exists(PremiosFaciales.ARCHIVO):
            with open(PremiosFaciales.ARCHIVO, "w", encoding="utf-8") as f:
                json.dump({}, f)

    @staticmethod
    def otorgar_premio(nombre, monto):
        """
        Suma 'monto' al usuario con el nombre dado.
        Si ya tiene premio, se suma; si no, se inicia con ese monto.
        """
        PremiosFaciales.asegurar_archivo()
        with open(PremiosFaciales.ARCHIVO, "r+", encoding="utf-8") as f:
            datos = json.load(f)  # Leer los premios actuales
            datos[nombre] = datos.get(nombre, 0) + monto  # Sumar el nuevo monto
            f.seek(0)
            json.dump(datos, f, indent=4)  # Sobrescribir con los nuevos datos
            f.truncate()
        print(f"💰 Recompensa registrada: {nombre} +${monto} (Total: ${datos[nombre]})")

    @staticmethod
    def obtener_total(nombre):
        """
        Devuelve el total de dinero que tiene acumulado un usuario.
        Si no tiene nada guardado, devuelve 0.
        """
        PremiosFaciales.asegurar_archivo()
        with open(PremiosFaciales.ARCHIVO, "r", encoding="utf-8") as f:
            datos = json.load(f)
            return datos.get(nombre, 0)
