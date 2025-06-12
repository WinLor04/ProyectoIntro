import json
import os

class Guardar:
    def __init__(self, archivo="Registro.json"):
        self.archivo = archivo
        # Crear archivo si no existe
        if not os.path.exists(self.archivo):
            with open(self.archivo, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=4)

    def guardar_usuario(self, usuario, clave):
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)

            if usuario in datos:
                return False  # Ya existe

            datos[usuario] = clave  # Agregar nuevo

            with open(self.archivo, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4)

            return True
        except Exception as e:
            print(f"Error al guardar: {e}")
            return False
        
    def verificar_credenciales(self, usuario, clave):
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
            return datos.get(usuario) == clave
        except Exception as e:
            print(f"Error al verificar: {e}")
            return False
    def verificar_usuario_por_rostro(self, nombre_usuario):
        """
        Verifica si el nombre reconocido por rostro existe en el archivo de usuarios registrados.
        """
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
            return nombre_usuario in datos
        except Exception as e:
            print(f"Error al verificar usuario por rostro: {e}")
            return False

