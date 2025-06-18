import json
import os

"""
Clase que maneja el guardado del usuario con el método de log in mediante
nombre y clave
"""

class Guardar:
    def __init__(self, archivo="Registro.json"):
        self.archivo = archivo
        # Crear archivo si no existe
        if not os.path.exists(self.archivo):
            with open(self.archivo, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=4)

    def guardar_usuario(self, usuario, clave):
        """
        Guarda un nuevo usuario y su clave en el archivo JSON.
        Retorna True si se guardó correctamente, False si ya existe.
        """
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
        """
        Verifica si las credenciales del usuario (nombre y clave) coinciden con las registradas
        en el archivo de usuarios.
        """
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

    def verificar_usuario_existe(self, nombre_usuario):
        """
        Verifica si un usuario existe en cualquiera de los registros: clave, rostro (json), o rostro (npy).
        """
        try:
            # Verificar en archivo de usuarios con clave
            with open(self.archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
            if nombre_usuario in datos:
                return True  # Si existe en el archivo de clave, retornamos True

            # Verificar en archivo de usuarios con rostro (JSON)
            rostro_archivo = "premios_facial.json"  # Archivo donde están los usuarios faciales
            if os.path.exists(rostro_archivo):
                with open(rostro_archivo, "r", encoding="utf-8") as f:
                    datos_rostro = json.load(f)
                if nombre_usuario in datos_rostro:
                    return True  # Si existe en el archivo facial, retornamos True

            # Verificar en archivo de usuarios faciales (npy)
            rostro_npy_archivo = f"users_lbph/{nombre_usuario}.npy"
            if os.path.exists(rostro_npy_archivo):
                return True  # Si existe el archivo .npy, retornamos True

            # Si no se encuentra en ninguno de los archivos, retornamos False
            return False
        except Exception as e:
            print(f"Error al verificar usuario en clave, rostro (json) o rostro (npy): {e}")
            return False
