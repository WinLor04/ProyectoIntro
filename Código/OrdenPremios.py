import json
from PremiosClave import PremiosClave
from PremiosFaciales import PremiosFaciales

"""
Clase utilizada para la búsqueda de los puntajes más altos entre los archivos
designados para método: clave o facial
"""

class OrdenPremios:
    @staticmethod
    def obtener_premios():
        """
        Lee los archivos de premios de los usuarios con clave y facial, los combina
        y devuelve los 5 mejores puntajes globales.
        """
        premiosTotales = {}

        # Premios de los usuarios con clave
        with open("premios_clave.json", "r") as f:
            datosClave = json.load(f)
            for usuario, premio in datosClave.items():
                premiosTotales[usuario] = premio

        # Premios de los usuarios con facial
        with open("premios_facial.json", "r") as f:
            datosFacial = json.load(f)
            for usuario, premio in datosFacial.items():
                if usuario in premiosTotales:
                    premiosTotales[usuario] += premio  # Sumar si ya existe
                else:
                    premiosTotales[usuario] = premio

        # Ordenar los premios de mayor a menor
        premiosOrdenados = sorted(premiosTotales.items(), key=lambda x: x[1], reverse=True)

        # Devolver los 5 mejores puntajes
        return premiosOrdenados[:5]