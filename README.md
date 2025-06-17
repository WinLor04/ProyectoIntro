# 🧠 Memory Game

Memory Game es una aplicación interactiva desarrollada en Python que ofrece a los usuarios la experiencia del clásico juego de memoria con una propuesta moderna, flexible y adaptada a diferentes tipos de manejo de datos. El objetivo es ejercitar la memoria a corto plazo a través de dos modalidades de juego.

## 🎮 Tipos de juego
**Modo Clásico**

El clásico juego de memoria, donde el jugador debe encontrar pares de cartas. En este modo, los jugadores compiten para completar su tablero con la menor cantidad de intentos posibles.

**Modo Patrones**

En este modo, el jugador debe recordar y replicar un patrón de casillas iluminadas. A medida que avanza, la dificultad aumenta al agregar más casillas al patrón en cada ronda ganada.

## 🛠️ Herramientas utilizadas

**Python**: Lenguaje principal para la lógica del juego y la implementación de las funcionalidades.

**Visual Studio Code (VS Code)**: Entorno de desarrollo utilizado para escribir y organizar el código fuente.

**GitKraken**: Herramienta gráfica para el manejo de versiones, integración con Git y GitHub.

**API**: Integración con una API del Banco Central de Costa Rica (BCCR) para obtener el tipo de cambio del dólar y realizar el cálculo de premios para el jugador en colones, utilizando su puntaje.

## 🔗 Instalación y requisitos:

**pygame**:
Para ejecutar la interfaz gráfica y los elementos interactivos del juego.
```python
pip install pygame
```

**opencv-python**:
Para la implementación de reconocimiento facial.
```python
pip install opencv-python
```

**numpy**:
Para el almacenamiento y manejo de datos relacionados con el reconocimiento facial.
```python
pip install numpy
```

**requests**:
Para realizar peticiones HTTP, que se usa con frecuencia para interactuar con APIs.
```python
pip install requests
```

## 🛠️ Versiones de Herramientas y Dependencias Utilizadas
Para asegurar la compatibilidad del proyecto y facilitar su instalación en otros entornos, a continuación se presentan las versiones de las herramientas y dependencias utilizadas:

**Python**: 3.12.6

**PIP**: 24.2 (gestor de paquetes para Python)

**Pygame**: 2.6.1 (SDL 2.28.4, Python 3.12.6)

**OpenCV**: 4.11.0

**NumPy**: 2.2.3

**Requests**: 2.32.4

**Tkinter**: 8.6.13 (preinstalado con Python)

**Git**: 2.47.0.windows.2 (para el manejo de versiones)

## ⚠️ Posible error

- **Error: "No se pudo acceder a la cámara"**: Asegúrate de que tu cámara esté conectada y funcionando correctamente.

## 🌐 Enlaces 

- [Documentación de la API del Banco Central de Costa Rica (BCCR)](https://www.bccr.fi.cr/indicadores-economicos/servicio-web/gu%C3%ADa-de-uso)
- [Pygame - Documentación oficial](https://www.pygame.org/docs/)
- [NumPy - Documentación oficial](https://numpy.org/doc/)
- [Requests - Documentación oficial](https://docs.python-requests.org/en/latest/)
- [GitKraken - Página oficial](https://www.gitkraken.com/)
