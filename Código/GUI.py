import pygame
import sys
import os
from Botones import Boton
from Guardar import Guardar
import tkinter as tk
from tkinter import messagebox
from Reconfacial import ReconFacial
import threading
# Ocultar la ventana principal de tkinter para que no estorbe
root = tk.Tk()
root.withdraw()

class Interfaz:
    FONDO_GRIS = (52, 52, 52)
    BLANCO = (255, 255, 255)
    FPS = 60
    CYAN_OSCURO = "#4FB4CD"
    FONDO_GRIS = "#343434"
    FUENTE = ('Segoe UI', 20, 'bold')

    def __init__(self):
        pygame.init()

        info = pygame.display.Info()
        self.ANCHO = info.current_w
        self.ALTO = info.current_h

        # Crear pantalla con tamaño detectado
        self.pantalla = pygame.display.set_mode((self.ANCHO, self.ALTO), pygame.RESIZABLE)
        pygame.display.set_caption("Juego")
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.SysFont('Segoe UI', 36, bold=True)
        self.fuente_titulo = pygame.font.SysFont('Segoe UI', 40, bold=True) 
        self.fuente_grande = pygame.font.SysFont('Segoe UI', 48, bold=True)  # o el tamaño que necesites
        self.fuente_pequena = pygame.font.SysFont('Segoe UI', 24)
        self.botones_visibles = []
        ruta_fondo = os.path.join('assets', 'fondo.jpg')
        if os.path.exists(ruta_fondo):
            self.fondo = pygame.image.load(ruta_fondo)
            self.fondo = pygame.transform.scale(self.fondo, (self.ANCHO, self.ALTO))
        else:
            self.fondo = None

    # --- ACCIONES COMO MÉTODOS ---
    def ir_a_menu(self):
        print("→ Ir al menú principal")
        self.pantalla_menu_principal()

    def ir_a_registro(self):
        self.pantalla_registro()

    def salir(self):
        pygame.quit()
        sys.exit()

    def volver(self):
        self.pantalla_inicio()

    def volver_a_inicio(self):
        self.pantalla_inicio()
    
    def VerificarCursor(self):
        mouse_pos = pygame.mouse.get_pos()
        for boton in self.botones_visibles:
            if boton.rect.collidepoint(mouse_pos):
                if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_HAND:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                return
        if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def jugar(self):
        self.botones_visibles.clear()

        boton_unjugador = Boton("Un Jugador", self.ANCHO // 3 - 150, self.ALTO // 2 - 50, 320, 100, self.tablero_unjugador, self.fuente_grande, interfaz=self)
        boton_multijugador = Boton("Multijugador", 2 * self.ANCHO // 3 - 150, self.ALTO // 2 - 50, 320, 100, self.tablero_multijugador, self.fuente_grande, interfaz=self)
        boton_volver = Boton("Volver", 20, self.ALTO - 70, 100, 50, self.ir_a_menu, pygame.font.SysFont('Segoe UI', 30, bold=True), interfaz=self)

        fuente_titulo = pygame.font.SysFont('Segoe UI', 36, True)
        texto_titulo = "Modo de Juego"

        while True:
            self.pantalla.fill(self.FONDO_GRIS)
            if self.fondo:
                self.pantalla.blit(self.fondo, (0, 0))

            # Título centrado arriba
            titulo_render = fuente_titulo.render(texto_titulo, True, self.BLANCO)
            self.pantalla.blit(titulo_render, (self.ANCHO // 2 - titulo_render.get_width() // 2, 40))

            # Dibujar botones
            boton_unjugador.dibujar(self.pantalla)
            boton_multijugador.dibujar(self.pantalla)
            boton_volver.dibujar(self.pantalla)

            # Eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salir()
                boton_unjugador.manejar_evento(evento)
                boton_multijugador.manejar_evento(evento)
                boton_volver.manejar_evento(evento)
            
            #Verificar cursor
            self.VerificarCursor()
            pygame.display.flip()
            self.reloj.tick(self.FPS)

    def about(self):
        self.botones_visibles.clear()
        boton_volver = Boton("Volver", self.ANCHO // 2 - 150, self.ALTO - 100, 300, 60, self.pantalla_menu_principal, self.fuente, interfaz=self)

        texto = (
            "Desarrollado por:\n"
            "Dylan\n"
            "Windell\n\n"
            "Juego\n"
            "Proyecto"
        )

        fuente_titulo = pygame.font.SysFont('Segoe UI', 36, True)
        fuente_texto = pygame.font.SysFont('Segoe UI', 24)

        while True:
            self.pantalla.fill(self.FONDO_GRIS)
            if self.fondo:
                self.pantalla.blit(self.fondo, (0, 0))

            # Título
            titulo_render = fuente_titulo.render("About", True, self.BLANCO)
            self.pantalla.blit(titulo_render, (self.ANCHO // 2 - titulo_render.get_width() // 2, 100))

            # Texto multilinea centrado
            y_offset = 180
            for linea in texto.split('\n'):
                linea_render = fuente_texto.render(linea, True, self.BLANCO)
                self.pantalla.blit(linea_render, (self.ANCHO // 2 - linea_render.get_width() // 2, y_offset))
                y_offset += linea_render.get_height() + 8

            # Botón Volver
            boton_volver.dibujar(self.pantalla)

            # Manejo de eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salir()
                boton_volver.manejar_evento(evento)

            self.VerificarCursor()
            pygame.display.flip()
            self.reloj.tick(self.FPS)

    def premios(self):
        self.botones_visibles.clear()
        boton_volver = Boton("Volver", self.ANCHO // 2 - 150, self.ALTO - 100, 300, 60, self.pantalla_menu_principal, self.fuente, interfaz=self)

        fuente_titulo = pygame.font.SysFont('Segoe UI', 36, True)
        fuente_texto = pygame.font.SysFont('Segoe UI', 24)

        texto_info = "Premios (en dólares)\n\nAquí va la info de la API BCCR..."

        while True:
            self.pantalla.fill(self.FONDO_GRIS)
            if self.fondo:
                self.pantalla.blit(self.fondo, (0, 0))

            # Título
            titulo_render = fuente_titulo.render("Premios (en dólares)", True, self.BLANCO)
            self.pantalla.blit(titulo_render, (self.ANCHO // 2 - titulo_render.get_width() // 2, 100))

            # Texto multilinea centrado
            y_offset = 180
            for linea in texto_info.split('\n'):
                linea_render = fuente_texto.render(linea, True, self.BLANCO)
                self.pantalla.blit(linea_render, (self.ANCHO // 2 - linea_render.get_width() // 2, y_offset))
                y_offset += linea_render.get_height() + 8

            # Botón Volver
            boton_volver.dibujar(self.pantalla)

            # Eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salir()
                boton_volver.manejar_evento(evento)
            
            self.VerificarCursor()
            pygame.display.flip()
            self.reloj.tick(self.FPS)


    def como_jugar(self):
        self.botones_visibles.clear()
        boton_modo_clasico = Boton("Modo Clásico",self.ANCHO // 2 - 150,250,300,80,self.modo_clasico_window,self.fuente, interfaz=self)
        boton_modo_patrones = Boton("Modo Patrones",self.ANCHO // 2 - 150,350,300, 80, self.modo_patrones_window, self.fuente, interfaz=self)
        boton_volver = Boton("Volver",self.ANCHO // 2 - 150,self.ALTO - 100,300,60, self.pantalla_menu_principal, self.fuente, interfaz=self)

        while True:
            self.pantalla.fill(self.FONDO_GRIS)
            if self.fondo:
                self.pantalla.blit(self.fondo, (0, 0))

            titulo_render = self.fuente.render("Cómo Jugar", True, self.BLANCO)
            self.pantalla.blit(titulo_render, (self.ANCHO // 2 - titulo_render.get_width() // 2, 100))

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salir()
                boton_modo_clasico.manejar_evento(evento)
                boton_modo_patrones.manejar_evento(evento)
                boton_volver.manejar_evento(evento)

            boton_modo_clasico.dibujar(self.pantalla)
            boton_modo_patrones.dibujar(self.pantalla)
            boton_volver.dibujar(self.pantalla)

            self.VerificarCursor()
            pygame.display.flip()
            self.reloj.tick(self.FPS)


    def ajustes(self):
        self.botones_visibles.clear()
        # Esta es la pantalla de Ajustes, en pygame
        botones = []

        # Botón volver que llama a la pantalla principal
        btn_volver = Boton("Volver", self.ANCHO // 2 - 150, self.ALTO - 100, 300, 60, self.pantalla_menu_principal, self.fuente, interfaz=self)
        botones.append(btn_volver)

        while True:
            self.pantalla.fill(self.FONDO_GRIS)
            if self.fondo:
                self.pantalla.blit(self.fondo, (0, 0))

            # Título
            titulo = self.fuente.render("Ajustes", True, self.BLANCO)
            self.pantalla.blit(titulo, (self.ANCHO // 2 - titulo.get_width() // 2, 100))

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salir()
                for boton in botones:
                    boton.manejar_evento(evento)

            for boton in botones:
                boton.dibujar(self.pantalla)

            self.VerificarCursor()    
            pygame.display.flip()
            self.reloj.tick(self.FPS)

    def modo_clasico_window(self):
        self.botones_visibles.clear()
        # Cargar imágenes con pygame
        path_base = os.path.join('assets', "Imágenes", "jugadores")
        try:
            img_cristiano = pygame.image.load(os.path.join(path_base, "cristiano.png"))
            img_messi = pygame.image.load(os.path.join(path_base, "messi.png"))
            img_cristiano = pygame.transform.scale(img_cristiano, (130, 130))
            img_messi = pygame.transform.scale(img_messi, (130, 130))
        except Exception as e:
            print("Error cargando imágenes:", e)
            return

        texto = (
            "En el Modo Clásico se juega con una matriz de 6x6 .\n"
            "Cada matriz tiene 18 imágenes distintas con sus parejas.\n"
            "El jugador tiene 10 segundos para hacer cada jugada.\n"
            "Si falla, pasa el turno al otro jugador.\n"
            "Gana quien use menos intentos para completar el juego."
        )

        boton_volver = Boton("Volver",self.ANCHO // 2 - 150,self.ALTO - 100,300, 60,self.como_jugar, self.fuente, interfaz=self)

        # Preparar líneas de texto para renderizar (split por líneas)
        lineas_texto = texto.split('\n')

        while True:
            self.pantalla.fill(self.FONDO_GRIS)
            if self.fondo:
                self.pantalla.blit(self.fondo, (0, 0))

            # Título
            titulo_render = self.fuente_titulo.render("Modo Clásico", True, self.BLANCO)
            self.pantalla.blit(titulo_render, (self.ANCHO // 2 - titulo_render.get_width() // 2, 30))

            # Renderizar texto línea por línea con padding y justificado a la izquierda
            y_texto = 100
            for linea in lineas_texto:
                txt_render = self.fuente.render(linea, True, self.BLANCO)
                self.pantalla.blit(txt_render, (60, y_texto))
                y_texto += txt_render.get_height() + 5

            # Mostrar imágenes y símbolos debajo del texto

        
            x_correcto = self.ANCHO // 2 - 500
            y_imagenes = y_texto + 20

            self.pantalla.blit(img_cristiano, (x_correcto, y_imagenes))
            self.pantalla.blit(img_cristiano, (x_correcto + 170, y_imagenes))  # separacion aumentada

            check_verde = self.fuente_titulo.render("SI", True, (0, 255, 0))
            self.pantalla.blit(check_verde, (x_correcto + 320, y_imagenes + 40))  # desplazamiento un poco mayor

          
            x_incorrecto = self.ANCHO // 2 + 100

            self.pantalla.blit(img_messi, (x_incorrecto, y_imagenes))
            self.pantalla.blit(img_cristiano, (x_incorrecto + 170, y_imagenes))

            cruz_roja = self.fuente_titulo.render("NO", True, (255, 0, 0))
            self.pantalla.blit(cruz_roja, (x_incorrecto + 320, y_imagenes + 40))


            # Botón volver
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salir()
                boton_volver.manejar_evento(evento)

            boton_volver.dibujar(self.pantalla)

            self.VerificarCursor()
            pygame.display.flip()
            self.reloj.tick(self.FPS)

    def modo_patrones_window(self):
        self.botones_visibles.clear()
        # Cargar imágenes con pygame
        path_base = os.path.join('assets', "Imágenes", "jugadores")
        try:
            img_mbappe = pygame.image.load(os.path.join(path_base, "mbappe.png"))
            img_messi = pygame.image.load(os.path.join(path_base, "messi.png"))
            img_cristiano = pygame.image.load(os.path.join(path_base, "cristiano.png"))

            img_mbappe = pygame.transform.scale(img_mbappe, (100, 100))
            img_messi = pygame.transform.scale(img_messi, (100, 100))
            img_cristiano = pygame.transform.scale(img_cristiano, (100, 100))
        except Exception as e:
            print("Error cargando imágenes:", e)
            return

        texto = (
            "En este modo unijugador, el objetivo es memorizar un patrón que se mostrará al inicio.\n"
            "El patrón consiste en una secuencia de imágenes que el jugador debe repetir en orden.\n"
            "Al iniciar, el patrón tiene 3 casillas y aumenta en 1 con cada éxito.\n"
            "El jugador tiene 12 segundos totales y 2 segundos para elegir cada casilla.\n"
            "Si falla, el juego termina.\n"
            "Ejemplo Mbappe, Messi, Cristiano"
        )

        boton_volver = Boton(
            "Volver",self.ANCHO // 2 - 150,self.ALTO - 100,300,60,self.como_jugar, self.fuente, interfaz=self)
        lineas_texto = texto.split('\n')
        while True:
            self.pantalla.fill(self.FONDO_GRIS)
            if self.fondo:
                self.pantalla.blit(self.fondo, (0, 0))
            # Título
            titulo_render = self.fuente_titulo.render("Modo Patrones", True, self.BLANCO)
            self.pantalla.blit(titulo_render, (self.ANCHO // 2 - titulo_render.get_width() // 2, 30))
            # Renderizar texto línea por línea
            y_texto = 100
            for linea in lineas_texto:
                txt_render = self.fuente.render(linea, True, self.BLANCO)
                self.pantalla.blit(txt_render, (60, y_texto))
                y_texto += txt_render.get_height() + 5
            # Mostrar imágenes con check y cruz
            y_imagenes = y_texto + 20
            x_correcto = self.ANCHO // 2 - 500
            x_incorrecto = self.ANCHO // 2 + 100

            # Patrón correcto: Mbappe -> Messi -> Cristiano + check verde
            self.pantalla.blit(img_mbappe, (x_correcto, y_imagenes))
            self.pantalla.blit(img_messi, (x_correcto + 100, y_imagenes))
            self.pantalla.blit(img_cristiano, (x_correcto + 200, y_imagenes))

            check_verde = self.fuente_titulo.render("SI", True, (0, 255, 0))
            self.pantalla.blit(check_verde, (x_correcto + 330, y_imagenes + 30))

            # Patrón incorrecto: Messi -> Cristiano -> Mbappe + cruz roja
            self.pantalla.blit(img_messi, (x_incorrecto, y_imagenes))
            self.pantalla.blit(img_cristiano, (x_incorrecto + 110, y_imagenes))
            self.pantalla.blit(img_mbappe, (x_incorrecto + 220, y_imagenes))

            cruz_roja = self.fuente_titulo.render("NO", True, (255, 0, 0))
            self.pantalla.blit(cruz_roja, (x_incorrecto + 330, y_imagenes + 30))

            # Botón volver
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salir()
                boton_volver.manejar_evento(evento)

            boton_volver.dibujar(self.pantalla)

            self.VerificarCursor()
            pygame.display.flip()
            self.reloj.tick(self.FPS)

    def tablero_unjugador(self):
        self.botones_visibles.clear()
        # Crear botón de pausa
        btn_pausa = Boton("Pausa", self.ANCHO - 150, 20, 130, 50, self.pausa_unjugador, self.fuente_grande, bg_color=(0, 139, 139), fg_color="black", interfaz=self)


        # Título
        fuente_titulo = pygame.font.SysFont('Segoe UI', 30, True)
        texto_titulo = "Modo Un Jugador - Tablero 6x6"

        # Crear la matriz de botones para el tablero 6x6
        self.botones_unjugador = []
        ancho_btn = 80
        alto_btn = 80
        separacion = 10
        tablero_ancho = 6 * ancho_btn + 5 * separacion
        tablero_alto = 6 * alto_btn + 5 * separacion

        # Posición del tablero centrado horizontalmente y un poco abajo
        start_x = self.ANCHO // 2 - tablero_ancho // 2
        start_y = 120

        for fila in range(6):
            fila_botones = []
            for col in range(6):
                x = start_x + col * (ancho_btn + separacion)
                y = start_y + fila * (alto_btn + separacion)
               
                btn = Boton("", x, y, ancho_btn, alto_btn, None, self.fuente_pequena, interfaz=self)
                btn.color_normal = pygame.Color("gray20") 
                btn.disabled = True 
                fila_botones.append(btn)
            self.botones_unjugador.append(fila_botones)

        # Loop principal de esta "ventana"
        while True:
            self.pantalla.fill(self.FONDO_GRIS)
            if self.fondo:
                self.pantalla.blit(self.fondo, (0, 0))

            # Dibujar título centrado arriba
            titulo_render = fuente_titulo.render(texto_titulo, True, self.BLANCO)
            self.pantalla.blit(titulo_render, (self.ANCHO // 2 - titulo_render.get_width() // 2, 30))

            # Dibujar botón pausa
            btn_pausa.dibujar(self.pantalla)

            # Dibujar botones del tablero
            for fila_botones in self.botones_unjugador:
                for btn in fila_botones:
                    btn.dibujar(self.pantalla)

            # Eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salir()
                btn_pausa.manejar_evento(evento)
                # No manejamos eventos de botones deshabilitados, pero si los habilitas más adelante,
                # recuerda usar btn.manejar_evento(evento)

            self.VerificarCursor()
            pygame.display.flip()
            self.reloj.tick(self.FPS)

    def pausa_unjugador(self):
        self.botones_visibles.clear()
        """Muestra una pantalla de pausa para el modo de un jugador en Pygame"""

        # Botones sin pasar bg_color ni fg_color en el constructor
        btn_salir = Boton(
            "Salir al Menú Principal",
            self.ANCHO // 2 - 200, self.ALTO // 2 + 100,
            400, 60,
            lambda: self.ir_a_menu(),
            self.fuente, 
            interfaz=self
        )
        # Asignar colores después
        btn_salir.color_normal = self.CYAN_OSCURO
        btn_salir.color_texto = pygame.Color("black")

        btn_continuar = Boton(
            "Continuar",
            self.ANCHO // 2 - 200, self.ALTO // 2,
            400, 60,
            lambda: None,  # Cambio aquí para que sea callable
            self.fuente, 
            interfaz=self
        )
        btn_continuar.color_normal = self.CYAN_OSCURO
        btn_continuar.color_texto = pygame.Color("black")

        # Texto
        fuente_titulo = pygame.font.SysFont('Segoe UI', 40, True)
        texto = fuente_titulo.render("Juego en Pausa", True, self.BLANCO)

        en_pausa = True
        while en_pausa:
            self.pantalla.fill(self.FONDO_GRIS)
            if self.fondo:
                self.pantalla.blit(self.fondo, (0, 0))

            self.pantalla.blit(texto, (self.ANCHO // 2 - texto.get_width() // 2, 150))

            btn_salir.dibujar(self.pantalla)
            btn_continuar.dibujar(self.pantalla)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salir()
                if btn_salir.manejar_evento(evento):
                    en_pausa = False  # botón ya llama a pantalla_menu_principal
                if btn_continuar.manejar_evento(evento):
                    en_pausa = False  # simplemente continúa

            self.VerificarCursor()
            pygame.display.flip()
            self.reloj.tick(self.FPS)

    def tablero_multijugador(self):
        self.botones_visibles.clear()
        # Crear botón de pausa
        btn_pausa = Boton(
            "Pausa", 
            self.ANCHO - 150, 20, 130, 50, 
            self.pausa_multijugador, 
            self.fuente_grande, 
            bg_color=(0, 139, 139), 
            fg_color="black",
            interfaz=self
        )

        # Título
        fuente_titulo = pygame.font.SysFont('Segoe UI', 30, True)
        texto_titulo = "Modo Multijugador - Tableros 6x6"

        # Parámetros del tablero
        ancho_btn = 80
        alto_btn = 80
        separacion = 10
        filas, columnas = 6, 6

        tablero_ancho = columnas * ancho_btn + (columnas - 1) * separacion
        tablero_alto = filas * alto_btn + (filas - 1) * separacion

        # Posiciones para los dos tableros
        # Tablero 1 a la izquierda
        start_x_1 = self.ANCHO // 4 - tablero_ancho // 2
        # Tablero 2 a la derecha
        start_x_2 = 3 * self.ANCHO // 4 - tablero_ancho // 2
        start_y = 120

        # Crear botones para jugador 1
        self.botones_jugador1 = []
        for fila in range(filas):
            fila_botones = []
            for col in range(columnas):
                x = start_x_1 + col * (ancho_btn + separacion)
                y = start_y + fila * (alto_btn + separacion)

                btn = Boton("", x, y, ancho_btn, alto_btn, None, self.fuente_pequena, interfaz=self)
                btn.color_normal = pygame.Color("gray20")
                btn.disabled = True
                fila_botones.append(btn)
            self.botones_jugador1.append(fila_botones)

        # Crear botones para jugador 2
        self.botones_jugador2 = []
        for fila in range(filas):
            fila_botones = []
            for col in range(columnas):
                x = start_x_2 + col * (ancho_btn + separacion)
                y = start_y + fila * (alto_btn + separacion)

                btn = Boton("", x, y, ancho_btn, alto_btn, None, self.fuente_pequena, interfaz=self)
                btn.color_normal = pygame.Color("gray20")
                btn.disabled = True
                fila_botones.append(btn)
            self.botones_jugador2.append(fila_botones)

        # Loop principal
        while True:
            self.pantalla.fill(self.FONDO_GRIS)
            if self.fondo:
                self.pantalla.blit(self.fondo, (0, 0))

            # Dibujar título centrado arriba
            titulo_render = fuente_titulo.render(texto_titulo, True, self.BLANCO)
            self.pantalla.blit(titulo_render, (self.ANCHO // 2 - titulo_render.get_width() // 2, 30))

            # Dibujar línea divisoria en el centro
            linea_x = self.ANCHO // 2
            pygame.draw.line(self.pantalla, pygame.Color("white"), (linea_x, start_y - 20), (linea_x, start_y + tablero_alto + 20), 4)

            # Dibujar botón pausa
            btn_pausa.dibujar(self.pantalla)

            # Dibujar botones de jugador 1
            for fila_botones in self.botones_jugador1:
                for btn in fila_botones:
                    btn.dibujar(self.pantalla)

            # Dibujar botones de jugador 2
            for fila_botones in self.botones_jugador2:
                for btn in fila_botones:
                    btn.dibujar(self.pantalla)

            # Eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salir()
                btn_pausa.manejar_evento(evento)
                # Puedes agregar manejo de eventos para botones si los habilitas más adelante

            self.VerificarCursor()
            pygame.display.flip()
            self.reloj.tick(self.FPS)

    def pausa_multijugador(self):
        self.botones_visibles.clear()
        """Pantalla de pausa para modo multijugador en Pygame"""
        # Crear botones sin bg_color ni fg_color en el constructor
        boton_salir = Boton(
            "Salir al Menú Principal",
            self.ANCHO // 2 - 200,
            self.ALTO // 2 + 100,
            400, 60,
            lambda: self.ir_a_menu(),
            self.fuente,
            interfaz=self
        )
        boton_salir.color_normal = self.CYAN_OSCURO
        boton_salir.color_texto = pygame.Color("black")

        boton_continuar = Boton(
            "Continuar",
            self.ANCHO // 2 - 200, self.ALTO // 2,
            400, 60,
            None,  # Sin acción, controlamos con manejar_evento
            self.fuente,
            interfaz=self
        )
        boton_continuar.color_normal = self.CYAN_OSCURO
        boton_continuar.color_texto = pygame.Color("black")

        ejecutando = True
        while ejecutando:
            self.pantalla.fill(self.FONDO_GRIS)
            if self.fondo:
                self.pantalla.blit(self.fondo, (0, 0))

            # Texto central
            texto = self.fuente_titulo.render("Juego en Pausa", True, self.BLANCO)
            self.pantalla.blit(texto, (self.ANCHO // 2 - texto.get_width() // 2, self.ALTO // 2 - 150))

            # Dibujar botones
            boton_salir.dibujar(self.pantalla)
            boton_continuar.dibujar(self.pantalla)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salir()
                elif boton_salir.manejar_evento(evento):
                    return  # Sale al menú principal
                elif boton_continuar.manejar_evento(evento):
                    ejecutando = False  # Aquí termina el bucle y reanuda el juego

            self.VerificarCursor()
            pygame.display.flip()
            self.reloj.tick(self.FPS)

    # --- PANTALLAS ---

    def pantalla_inicio(self):
        self.botones_visibles.clear()
        botones = [
            Boton("Iniciar Sesión", self.ANCHO // 2 - 410, 260, 350, 160, self.modo_inicio_sesion, self.fuente, interfaz=self),
            Boton("Registrarse", self.ANCHO // 2 + 60, 260, 350, 160, self.ir_a_registro, self.fuente, interfaz=self),
            Boton("Salir", self.ANCHO // 2 - 150, 480, 300, 60, self.salir, self.fuente, interfaz=self),
        ]

        while True:
            self.pantalla.fill(self.FONDO_GRIS)
            if self.fondo:
                self.pantalla.blit(self.fondo, (0, 0))

            titulo = self.fuente.render("¡BIENVENIDO!", True, self.BLANCO)
            self.pantalla.blit(titulo, (self.ANCHO // 2 - titulo.get_width() // 2, 100))

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salir()
                for boton in botones:
                    boton.manejar_evento(evento)

            for boton in botones:
                boton.dibujar(self.pantalla)

            self.VerificarCursor()
            pygame.display.flip()
            self.reloj.tick(self.FPS)

    def pantalla_registro(self):
        self.botones_visibles.clear()
        boton_usuario = Boton("Con usuario y contraseña", self.ANCHO // 2 - 450 - 40, 250, 450, 100, self.modo_usuario, self.fuente, interfaz=self)
        boton_facial = Boton("Reconocimiento facial", self.ANCHO // 2 + 40, 250, 450, 100, self.modo_facial, self.fuente, interfaz=self)

        boton_volver = Boton("Volver", self.ANCHO // 2 - 150, 500, 300, 60, self.volver, self.fuente, interfaz=self)

        while True:
            self.pantalla.fill(self.FONDO_GRIS)
            if self.fondo:
                self.pantalla.blit(self.fondo, (0, 0))

            titulo = self.fuente.render("Elige el método de registro", True, self.BLANCO)
            self.pantalla.blit(titulo, (self.ANCHO // 2 - titulo.get_width() // 2, 100))

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salir()
                boton_usuario.manejar_evento(evento)
                boton_facial.manejar_evento(evento)
                boton_volver.manejar_evento(evento)

            boton_usuario.dibujar(self.pantalla)
            boton_facial.dibujar(self.pantalla)
            boton_volver.dibujar(self.pantalla)

            self.VerificarCursor()
            pygame.display.flip()
            self.reloj.tick(self.FPS)
            
    def modo_usuario(self):
        guardar = Guardar()

        # Configuración visual
        ancho_entrada = 300
        alto_entrada = 50
        espacio = 80
        centro_x = self.ANCHO // 2
        inicio_y = 200

        usuario_rect = pygame.Rect(centro_x - ancho_entrada // 2, inicio_y, ancho_entrada, alto_entrada)
        clave_rect = pygame.Rect(centro_x - ancho_entrada // 2, inicio_y + espacio, ancho_entrada, alto_entrada)
        boton_aceptar = Boton("Registrar", centro_x - 150, inicio_y + espacio * 2 + 10, 300, 60, None, self.fuente, interfaz=self)
        boton_volver = Boton("Volver", centro_x - 150, inicio_y + espacio * 3 + 30, 300, 60, self.pantalla_registro, self.fuente, interfaz=self)

        color_activo = pygame.Color("white")
        color_inactivo = pygame.Color("gray")
        activo_usuario = False
        activo_clave = False

        texto_usuario = ""
        texto_clave = ""

        while True:
            self.pantalla.fill(self.FONDO_GRIS)
            if self.fondo:
                self.pantalla.blit(self.fondo, (0, 0))

            # Título centrado
            titulo = self.fuente.render("Registro de Usuario", True, self.BLANCO)
            self.pantalla.blit(titulo, (centro_x - titulo.get_width() // 2, 100))

            # Entradas
            pygame.draw.rect(self.pantalla, color_activo if activo_usuario else color_inactivo, usuario_rect, 2)
            pygame.draw.rect(self.pantalla, color_activo if activo_clave else color_inactivo, clave_rect, 2)

            etiqueta_usuario = self.fuente_pequena.render("Usuario:", True, self.BLANCO)
            etiqueta_clave = self.fuente_pequena.render("Contraseña:", True, self.BLANCO)
            self.pantalla.blit(etiqueta_usuario, (usuario_rect.x, usuario_rect.y - 35))
            self.pantalla.blit(etiqueta_clave, (clave_rect.x, clave_rect.y - 35))

            texto_render_usuario = self.fuente_pequena.render(texto_usuario, True, self.BLANCO)
            texto_render_clave = self.fuente_pequena.render("*" * len(texto_clave), True, self.BLANCO)
            self.pantalla.blit(texto_render_usuario, (usuario_rect.x + 5, usuario_rect.y + 10))
            self.pantalla.blit(texto_render_clave, (clave_rect.x + 5, clave_rect.y + 10))

            # Botones
            boton_aceptar.dibujar(self.pantalla)
            boton_volver.dibujar(self.pantalla)

            # Eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salir()

                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if usuario_rect.collidepoint(evento.pos):
                        activo_usuario = True
                        activo_clave = False
                    elif clave_rect.collidepoint(evento.pos):
                        activo_clave = True
                        activo_usuario = False
                    else:
                        activo_usuario = False
                        activo_clave = False

                    boton_aceptar.manejar_evento(evento)
                    boton_volver.manejar_evento(evento)

                    if boton_aceptar.rect.collidepoint(evento.pos):
                        if texto_usuario.strip() != "" and texto_clave.strip() != "":
                            exito = guardar.guardar_usuario(texto_usuario.strip(), texto_clave.strip())
                            if exito:
                                messagebox.showinfo("Registro exitoso", "Usuario registrado con éxito.")
                                texto_usuario = ""
                                texto_clave = ""
                            else:
                                messagebox.showerror("Error", "Este usuario ya existe o hubo un problema al guardar.")
                        else:
                            messagebox.showwarning("Campos incompletos", "Por favor, complete ambos campos.")

                elif evento.type == pygame.KEYDOWN:
                    if activo_usuario:
                        if evento.key == pygame.K_BACKSPACE:
                            texto_usuario = texto_usuario[:-1]
                        else:
                            texto_usuario += evento.unicode
                    elif activo_clave:
                        if evento.key == pygame.K_BACKSPACE:
                            texto_clave = texto_clave[:-1]
                        else:
                            texto_clave += evento.unicode

            self.VerificarCursor()
            pygame.display.flip()
            self.reloj.tick(self.FPS)

    def modo_facial(self):
        rf = ReconFacial(self)
        rf.pantalla_reconocimiento()

    def modo_inicio_sesion(self):
        from Guardar import Guardar
        guardar = Guardar()

        ancho_entrada = 300
        alto_entrada = 50
        espacio = 80
        centro_x = self.ANCHO // 2
        inicio_y = 200

        usuario_rect = pygame.Rect(centro_x - ancho_entrada // 2, inicio_y, ancho_entrada, alto_entrada)
        clave_rect = pygame.Rect(centro_x - ancho_entrada // 2, inicio_y + espacio, ancho_entrada, alto_entrada)
        boton_aceptar = Boton("Iniciar Sesión", centro_x - 150, inicio_y + espacio * 2 + 10, 300, 60, None, self.fuente, interfaz=self)
        boton_volver = Boton("Volver", centro_x - 150, inicio_y + espacio * 3 + 30, 300, 60, self.pantalla_inicio, self.fuente, interfaz=self)
        boton_reconocimiento = Boton("Reconocimiento Facial", centro_x - 200, inicio_y + espacio * 4 + 50, 400, 60, self.iniciar_con_reconocimiento_facial, self.fuente, interfaz=self)

        color_activo = pygame.Color("white")
        color_inactivo = pygame.Color("gray")
        activo_usuario = False
        activo_clave = False

        texto_usuario = ""
        texto_clave = ""

        while True:
            self.pantalla.fill(self.FONDO_GRIS)
            if self.fondo:
                self.pantalla.blit(self.fondo, (0, 0))

            titulo = self.fuente.render("Iniciar Sesión", True, self.BLANCO)
            self.pantalla.blit(titulo, (centro_x - titulo.get_width() // 2, 100))

            pygame.draw.rect(self.pantalla, color_activo if activo_usuario else color_inactivo, usuario_rect, 2)
            pygame.draw.rect(self.pantalla, color_activo if activo_clave else color_inactivo, clave_rect, 2)

            etiqueta_usuario = self.fuente_pequena.render("Usuario:", True, self.BLANCO)
            etiqueta_clave = self.fuente_pequena.render("Contraseña:", True, self.BLANCO)
            self.pantalla.blit(etiqueta_usuario, (usuario_rect.x, usuario_rect.y - 35))
            self.pantalla.blit(etiqueta_clave, (clave_rect.x, clave_rect.y - 35))

            texto_render_usuario = self.fuente_pequena.render(texto_usuario, True, self.BLANCO)
            texto_render_clave = self.fuente_pequena.render("*" * len(texto_clave), True, self.BLANCO)
            self.pantalla.blit(texto_render_usuario, (usuario_rect.x + 5, usuario_rect.y + 10))
            self.pantalla.blit(texto_render_clave, (clave_rect.x + 5, clave_rect.y + 10))

            boton_aceptar.dibujar(self.pantalla)
            boton_volver.dibujar(self.pantalla)
            boton_reconocimiento.dibujar(self.pantalla)


            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salir()

                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if usuario_rect.collidepoint(evento.pos):
                        activo_usuario = True
                        activo_clave = False
                    elif clave_rect.collidepoint(evento.pos):
                        activo_clave = True
                        activo_usuario = False
                    else:
                        activo_usuario = False
                        activo_clave = False

                    boton_aceptar.manejar_evento(evento)
                    boton_volver.manejar_evento(evento)
                    boton_reconocimiento.manejar_evento(evento)


                    if boton_aceptar.rect.collidepoint(evento.pos):
                        if texto_usuario.strip() != "" and texto_clave.strip() != "":
                            if guardar.verificar_credenciales(texto_usuario.strip(), texto_clave.strip()):
                                messagebox.showinfo("Bienvenido", "Inicio de sesión exitoso.")
                                self.ir_a_menu()  # o lo que corresponda
                            else:
                                messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos.")
                        else:
                            messagebox.showwarning("Campos incompletos", "Por favor, complete ambos campos.")

                elif evento.type == pygame.KEYDOWN:
                    if activo_usuario:
                        if evento.key == pygame.K_BACKSPACE:
                            texto_usuario = texto_usuario[:-1]
                        else:
                            texto_usuario += evento.unicode
                    elif activo_clave:
                        if evento.key == pygame.K_BACKSPACE:
                            texto_clave = texto_clave[:-1]
                        else:
                            texto_clave += evento.unicode

            self.VerificarCursor()
            pygame.display.flip()
            self.reloj.tick(self.FPS)


    def pantalla_menu_principal(self):
        self.botones_visibles.clear()
        botones = [
            Boton("Jugar", self.ANCHO // 2 - 370, 250, 300, 100, self.jugar, self.fuente, interfaz=self),
            Boton("About", self.ANCHO // 2 + 70, 250, 300, 100, self.about, self.fuente, interfaz=self),
            Boton("Premios", self.ANCHO // 2 - 370, 380, 300, 100, self.premios, self.fuente, interfaz=self),
            Boton("Cómo Jugar", self.ANCHO // 2 + 70, 380, 300, 100, self.como_jugar, self.fuente, interfaz=self),
            Boton("Q", 20, self.ALTO - 70, 60, 50, self.ajustes, self.fuente, interfaz=self),
            Boton("Cerrar Sesión", self.ANCHO - 240, self.ALTO - 70, 230, 50, self.volver_a_inicio, self.fuente, interfaz=self),
        ]

        while True:
            self.pantalla.fill(self.FONDO_GRIS)
            if self.fondo:
                self.pantalla.blit(self.fondo, (0, 0))

            titulo = self.fuente.render("Menú Principal", True, self.BLANCO)
            self.pantalla.blit(titulo, (self.ANCHO // 2 - titulo.get_width() // 2, 100))

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salir()
                for boton in botones:
                    boton.manejar_evento(evento)

            for boton in botones:
                boton.dibujar(self.pantalla)

            self.VerificarCursor()
            pygame.display.flip()
            self.reloj.tick(self.FPS)

    def iniciar_con_reconocimiento_facial(self):
        reconocimiento = ReconFacial(self)
        reconocimiento.iniciar_login_facial()