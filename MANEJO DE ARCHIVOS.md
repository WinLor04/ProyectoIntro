Este documento define el propósito y el uso esperado de cada archivo .py en el proyecto, para mantener una estructura clara, modular y fácil de mantener.

🔹 main.py
Propósito: Punto de entrada del programa.

Responsabilidades:

Iniciar pygame.

Crear la ventana principal.

Instanciar y ejecutar el controlador del juego.

Reglas:

No debe contener lógica del juego directamente.

Solo se debe llamar desde este archivo al iniciar el programa.

🔹 Clasico.py
Propósito: Manejar toda la lógica del modo clásico (2 jugadores, imágenes, tiempo por turno).

Responsabilidades:

Crear un único tablero compartido para ambos jugadores.

Controlar turnos, intentos, tiempos y reglas de juego.

Verificar aciertos y manejar el final del juego.

Reglas:

Este archivo no debe tener ninguna instrucción gráfica (pygame).

Toda la lógica del juego clásico debe estar centralizada aquí.


🔹 Patrones.py
Propósito: Implementar la lógica del modo patrones (un jugador, secuencias crecientes).

Responsabilidades:

Generar secuencias aleatorias de casillas.

Verificar si el jugador repite correctamente el patrón.

Aumentar la dificultad si el jugador acierta.

Reglas:

Sin lógica gráfica.

Maneja únicamente la lógica de patrones y validación.

🔹 Jugador.py
Propósito: Representar un jugador como objeto (nombre, puntaje, intentos, etc.).

Responsabilidades:

Guardar y actualizar información del jugador.

Posibles métodos para incrementar puntaje o reiniciar estado.

Reglas:

Puede ser utilizado por ambos modos de juego.

🔹 Interfaz.py
Propósito: Controlar la interfaz gráfica utilizando pygame.

Responsabilidades:

Dibujar elementos en pantalla (tablero, botones, mensajes, etc.).

Mostrar resultados, transiciones y animaciones.

Recibir y procesar entradas del usuario.

Reglas:

No debe contener lógica de juego.

Recibe datos de los módulos Clasico o Patrones.

🔧 Buenas prácticas
Toda lógica debe estar separada de la interfaz.

Los archivos deben ser reutilizables entre sí, usando clases limpias y funciones claras.

Evitar código duplicado entre los modos clásico y patrones.

📁 `assets/`
**Propósito**: Almacenar todos los recursos multimedia utilizados por el juego.
**Estructura interna**:
  - `assets/Audio/`: Archivos de sonido y música de fondo.
  - `assets/Imágenes/`: Imágenes utilizadas en el modo clásico (cartas del tablero, fondo, íconos, etc.).
**Reglas**:
  - No se debe guardar ningún archivo de código dentro de esta carpeta.
  - Se recomienda mantener nombres descriptivos para facilitar su uso desde el código.
  - Los recursos deben cargarse dinámicamente desde el código, usando rutas relativas.