import pygame
import sys
import os
from Botones import Boton
from Guardar import Guardar
import tkinter as tk
from tkinter import messagebox
from Reconfacial import ReconFacial
from SesionUsuario import SesionUsuario
from PremiosFaciales import PremiosFaciales
from PremiosClave import PremiosClave
from JuegoPatrones import JuegoPatrones
from ModoMultijugador import ModoMultijugador
from Sonido import Sonido
from TipoCambioBCCR import TipoCambioBCCR
from OrdenPremios import OrdenPremios
import time

sonido = Sonido()
Boton.sonido_global = sonido
root = tk.Tk()
root.withdraw()
sonido.reproducir_musica()
sonido.detener_musica()

"""
Esta es una clase para el manejo de la interfaz del juego de Memory Game
"""

class Interfaz:
    FONDO_GRIS = (52, 52, 52)
    BLANCO = (255, 255, 255)
    FPS = 60
    CYAN_OSCURO = "#4FB4CD"
    FONDO_GRIS = "#343434"
    FUENTE = ('Segoe UI', 20, 'bold')

    def __init__(self):

        pygame.init()

        #Llamada a la logica
        self.LogicaPatrones = JuegoPatrones()

        info = pygame.display.Info()
        self.ANCHO = info.current_w
        self.ALTO = info.current_h

        # Crear pantalla con tamaño detectado
        self.pantalla = pygame.display.set_mode((self.ANCHO, self.ALTO), pygame.RESIZABLE)
        pygame.display.set_caption("Juego")
        self.sonido = Sonido()
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.SysFont('Segoe UI', 36, bold=True)
        self.fuente_titulo = pygame.font.SysFont('Segoe UI', 40, bold=True) 
        self.fuente_grande = pygame.font.SysFont('Segoe UI', 48, bold=True)  # o el tamaño que necesites
        self.fuente_pequena = pygame.font.SysFont('Segoe UI', 24)
        self.botones_visibles = []
        self.animando_patron = False  # Desactiva hover visual durante animación
        self.sesion = SesionUsuario()
        path_turno = os.path.join("assets", "Imágenes", "turno")
        self.img_turno_on = pygame.image.load(os.path.join(path_turno, "turno.png")).convert_alpha()
        self.img_turno_off = pygame.image.load(os.path.join(path_turno, "turno_off.png")).convert_alpha()
        self.img_turno_on = pygame.transform.scale(self.img_turno_on, (75, 65))
        self.img_turno_off = pygame.transform.scale(self.img_turno_off, (75, 65))

        ruta_fondo = os.path.join('assets', 'fondo.jpg')
        if os.path.exists(ruta_fondo):
            self.fondo = pygame.image.load(ruta_fondo)
            self.fondo = pygame.transform.scale(self.fondo, (self.ANCHO, self.ALTO))
        else:
            self.fondo = None

    # --- ACCIONES COMO MÉTODOS ---
    def ir_a_menu(self):
        self.pantalla_menu_principal()

    def ir_a_registro(self):
        self.pantalla_registro()

    def salir(self):
        pygame.quit()
        sys.exit()

    def volver(self):
        self.pantalla_inicio()

    def volver_a_inicio(self):
        sonido.detener_musica()  
        self.pantalla_inicio()

    
    def VerificarCursor(self):
        """
        Verifica si el cursor del mouse está sobre algún botón visible.
        Si está sobre un botón, cambia el cursor a una mano, de lo contrario, lo cambia a la flecha.
        """
        mouse_pos = pygame.mouse.get_pos()
        for boton in self.botones_visibles:
            if boton.rect.collidepoint(mouse_pos):
                if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_HAND:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                return
        if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def jugar(self):
        """
        Muestra la pantalla de selección de modo de juego.
        Permite al usuario elegir entre un jugador o multijugador.
        """
        self.botones_visibles.clear()

        boton_unjugador = Boton("Un Jugador", self.ANCHO // 3 - 150, self.ALTO // 2 - 50, 320, 100, self.tablero_unjugador, self.fuente_grande, interfaz=self)
        boton_multijugador = Boton("Multijugador", 2 * self.ANCHO // 3 - 150, self.ALTO // 2 - 50, 320, 100, self.pantalla_nombres_multijugador, self.fuente_grande, interfaz=self)
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
        """
        Muestra información sobre los desarrolladores y el juego.
        """
        self.botones_visibles.clear()
        boton_volver = Boton("Volver", self.ANCHO // 2 - 150, self.ALTO - 100, 300, 60, self.pantalla_menu_principal, self.fuente, interfaz=self)

        # Fuentes para cada parte
        fuente_titulo = pygame.font.SysFont('Segoe UI', 40, True)
        fuente_subtitulo = pygame.font.SysFont('Segoe UI', 32, True)
        fuente_juego = pygame.font.SysFont('Segoe UI', 28, True)
        fuente_texto = pygame.font.SysFont('Segoe UI', 24)

        # Cargar imágenes con nueva ruta
        try:
            imagen_messi = pygame.image.load(os.path.join("assets", "Imágenes", "jugadores", "messi.png"))
            imagen_cristiano = pygame.image.load(os.path.join("assets", "Imágenes", "jugadores", "cristiano.png"))

            imagen_messi = pygame.transform.scale(imagen_messi, (200, 200))
            imagen_cristiano = pygame.transform.scale(imagen_cristiano, (200, 200))
        except Exception as e:
            print("Error cargando imágenes:", e)
            imagen_messi = None
            imagen_cristiano = None

        while True:
            self.pantalla.fill(self.FONDO_GRIS)
            if self.fondo:
                self.pantalla.blit(self.fondo, (0, 0))
            y = 80

            # Título
            titulo_render = fuente_titulo.render("Instituto Tecnológico de Costa Rica", True, self.BLANCO)
            self.pantalla.blit(titulo_render, (self.ANCHO // 2 - titulo_render.get_width() // 2, y))
            y += titulo_render.get_height() + 20

            # Subtítulo
            subtitulo_render = fuente_subtitulo.render("Ingeniería en Computadores", True, self.BLANCO)
            self.pantalla.blit(subtitulo_render, (self.ANCHO // 2 - subtitulo_render.get_width() // 2, y))
            y += subtitulo_render.get_height() + 20

            # Nombre del juego
            juego_render = fuente_juego.render("Memory Game", True, self.BLANCO)
            self.pantalla.blit(juego_render, (self.ANCHO // 2 - juego_render.get_width() // 2, y))
            y += juego_render.get_height() + 40

            # Desarrolladores
            creditos_render = fuente_texto.render("Desarrollado por Windell Loria y Dylan Bonilla", True, self.BLANCO)
            self.pantalla.blit(creditos_render, (self.ANCHO // 2 - creditos_render.get_width() // 2, y))

            # Imágenes de jugadores
            if imagen_messi:
                self.pantalla.blit(imagen_messi, (80, 150))  # Izquierda
            if imagen_cristiano:
                self.pantalla.blit(imagen_cristiano, (self.ANCHO - 280, 150))  # Derecha

            # Botón volver
            boton_volver.dibujar(self.pantalla)

            # Eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salir()
                boton_volver.manejar_evento(evento)

            self.VerificarCursor()
            pygame.display.flip()
            self.reloj.tick(self.FPS)

    def premios(self):
        """
        Muestra los 5 mejores puntajes globales de todos los usuarios, considerando
        tanto los premios obtenidos por 'clave' como por 'facial'. También muestra
        la conversión del premio en colones usando el tipo de cambio actual del dólar.
        """
        self.botones_visibles.clear()
        
        # Crear el botón para volver al menú principal
        boton_volver = Boton("Volver", self.ANCHO // 2 - 150, self.ALTO - 100, 300, 60, self.pantalla_menu_principal, self.fuente, interfaz=self)
        fuente_titulo = pygame.font.SysFont('Segoe UI', 36, True)
        fuente_texto = pygame.font.SysFont('Segoe UI', 24)

        # Obtener tipo de cambio desde la API
        try:
            bccr = TipoCambioBCCR("d.bonilla.3@estudiantec.cr", "5B3R6MS2OE")
            compra = bccr.obtener_compra()  # Usamos el valor de compra
            texto_info = f"Tipo de cambio:\n{compra:.2f} $"
        except Exception as e:
            texto_info = "No se pudo obtener el tipo de cambio.\n\nVerifica tu conexión a internet."

        while True:
            self.pantalla.fill(self.FONDO_GRIS)
            if self.fondo:
                self.pantalla.blit(self.fondo, (0, 0))

            # Título de la pantalla
            titulo_render = fuente_titulo.render("Top 5 Premios Globales", True, self.BLANCO)
            self.pantalla.blit(titulo_render, (self.ANCHO // 2 - titulo_render.get_width() // 2, 50))

            # Mostrar tipo de cambio o error
            y_offset = 150
            for linea in texto_info.split('\n'):
                linea_render = fuente_texto.render(linea, True, self.BLANCO)
                self.pantalla.blit(linea_render, (self.ANCHO // 2 - linea_render.get_width() // 2, y_offset))
                y_offset += linea_render.get_height() + 10

            # Obtener los 5 mejores puntajes globales
            premios_ordenados = OrdenPremios.obtener_premios()

            y_offset += 20
            # Mostrar los primeros 5 premios ordenados
            for i, (usuario, premio) in enumerate(premios_ordenados[:5]):
                # Cálculo del nuevo premio con la fórmula
                try:
                    calculo_premio = (1 / premio) * 100 * compra  # Fórmula de cálculo
                except ZeroDivisionError:
                    calculo_premio = 0  # Si el puntaje es 0, el premio será 0.

                # Estilo: espacio visual entre los ítems, bordes y texto destacado
                texto_usuario = fuente_texto.render(f"{i+1}. {usuario}:  Puntos: {premio} → Premio: ₡{round(calculo_premio, 2)}", True, self.BLANCO)
                
                # Agregar un contorno visual (resaltado) SE PUEDE BORRAR
                pygame.draw.rect(self.pantalla, (0, 139, 139), pygame.Rect(self.ANCHO // 2 - texto_usuario.get_width() // 2 - 10, y_offset - 5, texto_usuario.get_width() + 20, texto_usuario.get_height() + 10), 3)
                
                # Mostrar el texto
                self.pantalla.blit(texto_usuario, (self.ANCHO // 2 - texto_usuario.get_width() // 2, y_offset))
                y_offset += texto_usuario.get_height() + 20  # Ajuste de espaciado entre usuarios

            # Botón Volver
            boton_volver.dibujar(self.pantalla)

            # Eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salir()
                boton_volver.manejar_evento(evento)

            self.VerificarCursor()  # Actualizar cursor en pantalla
            pygame.display.flip()  # Mostrar los cambios en la pantalla
            self.reloj.tick(self.FPS)  # Controlar la velocidad de actualización

            # Manejar eventos: volver al menú o salir
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salir()
                boton_volver.manejar_evento(evento)

            self.VerificarCursor()  # Actualizar cursor en pantalla
            pygame.display.flip()  # Mostrar los cambios en la pantalla
            self.reloj.tick(self.FPS)  # Controlar la velocidad de actualización

    def como_jugar(self):
        """
        Muestra una pantalla con instrucciones sobre cómo jugar el juego.
        Permite al usuario elegir entre el modo clásico y el modo patrones.
        """
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
        """
        Muestra la pantalla de ajustes donde el usuario puede seleccionar música, ajustar volumen y activar/desactivar mute.
        """
        self.botones_visibles.clear()

        btn_volver = Boton("Volver", self.ANCHO // 2 - 150, self.ALTO - 100, 300, 60, self.pantalla_menu_principal, self.fuente, interfaz=self)

        canciones = [("HeatWaves", "HeatWaves.mp3"), ("Feet", "Feet.mp3"), ("TheNights", "TheNights.mp3")]
        cancion_seleccionada = 0
        mute = False
        volumen = 0.3

        casilla_radio_size = 30
        slider_pos_y = 520
        slider_width = 400
        slider_height = 30
        slider_knob_radius = 18

        # Reproduce canción inicial
        self.sonido.reproducir_cancion(canciones[cancion_seleccionada][1], volumen, mute)

        centro_x = self.ANCHO // 2
        start_y = 260
        espacio_y = 50

        while True:
            self.pantalla.fill(self.FONDO_GRIS)
            if self.fondo:
                self.pantalla.blit(self.fondo, (0, 0))

            # Título centrado
            titulo = self.fuente.render("Ajustes", True, self.BLANCO)
            self.pantalla.blit(titulo, (centro_x - titulo.get_width() // 2, 50))

            # Texto "Escoger música:" encima de las casillas
            texto_musica = self.fuente.render("Escoger música:", True, self.BLANCO)
            self.pantalla.blit(texto_musica, (centro_x - texto_musica.get_width() // 2, start_y - 70))

            # Texto "Volumen:" encima del slider
            texto_volumen = self.fuente.render("Volumen:", True, self.BLANCO)
            self.pantalla.blit(texto_volumen, (centro_x - texto_volumen.get_width() // 2, slider_pos_y - 40))

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salir()

                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = evento.pos

                    # Casillas canciones
                    for i in range(len(canciones)):
                        x = centro_x - 150
                        y = start_y + i * espacio_y
                        rect_casilla = pygame.Rect(x, y, casilla_radio_size, casilla_radio_size)
                        if rect_casilla.collidepoint(mx, my):
                            cancion_seleccionada = i
                            self.sonido.reproducir_cancion(canciones[cancion_seleccionada][1], volumen, mute)

                    # Casilla mute
                    x_mute = centro_x - 150
                    y_mute = start_y + len(canciones) * espacio_y + 20
                    rect_mute = pygame.Rect(x_mute, y_mute, casilla_radio_size, casilla_radio_size)
                    if rect_mute.collidepoint(mx, my):
                        mute = not mute
                        pygame.mixer.music.set_volume(0 if mute else volumen)

                    # Slider volumen
                    x_slider = centro_x - slider_width // 2
                    y_slider = slider_pos_y
                    rect_slider = pygame.Rect(x_slider, y_slider, slider_width, slider_height)
                    if rect_slider.collidepoint(mx, my):
                        volumen = (mx - x_slider) / slider_width
                        volumen = max(0, min(1, volumen))
                        if not mute:
                            pygame.mixer.music.set_volume(volumen)

                elif evento.type == pygame.MOUSEMOTION and evento.buttons[0]:
                    mx, my = evento.pos
                    x_slider = centro_x - slider_width // 2
                    y_slider = slider_pos_y
                    rect_slider = pygame.Rect(x_slider, y_slider, slider_width, slider_height)
                    if rect_slider.collidepoint(mx, my):
                        volumen = (mx - x_slider) / slider_width
                        volumen = max(0, min(1, volumen))
                        if not mute:
                            pygame.mixer.music.set_volume(volumen)

                btn_volver.manejar_evento(evento)

            # Dibujar botón volver
            btn_volver.dibujar(self.pantalla)

            # Dibujar casillas canciones (radio buttons)
            #enumerate() es una función de Python que agrega un índice a los elementos de un iterable.
            for i, (nombre, _) in enumerate(canciones):
                x = centro_x - 150
                y = start_y + i * espacio_y

                # círculo externo
                pygame.draw.circle(self.pantalla, self.BLANCO,
                                (x + casilla_radio_size // 2, y + casilla_radio_size // 2),
                                casilla_radio_size // 2, 2)
                # círculo relleno si seleccionado
                if i == cancion_seleccionada:
                    pygame.draw.circle(self.pantalla, self.CYAN_OSCURO,
                                    (x + casilla_radio_size // 2, y + casilla_radio_size // 2),
                                    casilla_radio_size // 2 - 7)

                # texto
                texto = self.fuente.render(nombre, True, self.BLANCO)
                self.pantalla.blit(texto, (x + casilla_radio_size + 15, y - 3))

            # Dibujar casilla mute (cuadrado)
            x_mute = centro_x - 150
            y_mute = start_y + len(canciones) * espacio_y + 40
            rect_mute = pygame.Rect(x_mute, 430, casilla_radio_size, casilla_radio_size)
            pygame.draw.rect(self.pantalla, self.BLANCO, rect_mute, 3)
            if mute:
                pygame.draw.rect(self.pantalla, self.CYAN_OSCURO, rect_mute.inflate(-8, -8))

            texto_mute = self.fuente.render("Mute", True, self.BLANCO)
            self.pantalla.blit(texto_mute, (x_mute + casilla_radio_size + 15, y_mute - 30))

            # Dibujar slider volumen
            x_slider = centro_x - slider_width // 2
            y_slider = slider_pos_y
            rect_slider = pygame.Rect(x_slider, y_slider, slider_width, slider_height)
            pygame.draw.rect(self.pantalla, self.BLANCO, rect_slider, 2)

            # knob (círculo móvil)
            knob_x = x_slider + int(volumen * slider_width)
            knob_y = y_slider + slider_height // 2
            pygame.draw.circle(self.pantalla, self.CYAN_OSCURO, (knob_x, knob_y), slider_knob_radius)

            # Actualizar cursor
            self.VerificarCursor()

            pygame.display.flip()
            self.reloj.tick(self.FPS)

    def modo_clasico_window(self):
        """
        Muestra una pantalla con instrucciones sobre el modo clásico del juego.
        Permite al usuario ver ejemplos de imágenes y cómo se juega.
        """
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
            "El jugador tiene un tiempo en segundos para hacer cada jugada.\n"
            "Si falla, pasa el turno al otro jugador.\n"
            "Gana quien logre completar su tablero primero."
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
        """
        Muestra una pantalla con instrucciones sobre el modo patrones del juego.
        Permite al usuario ver ejemplos de imágenes y cómo se juega.
        """

        self.botones_visibles.clear()
        # Cargar imágenes con pygame
        path_base = os.path.join('assets', "Imágenes", "jugadores")
      
        texto = (
            "En este modo unijugador, el objetivo es memorizar un patrón .\n"
            "El patrón consiste en una secuencia botones amarillos.\n"
            "Al iniciar, el patrón tiene 3 casillas y aumenta en 1 .\n"
            "El jugador tiene 12 segundos totales y 2 segundos para elegir .\n"
            "Si falla, el juego termina .\n"
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
        """
        Muestra el tablero de juego para el modo un jugador.
        Permite al usuario jugar solo, siguiendo un patrón de casillas.
        """
        self.botones_visibles.clear()

        if self.sesion.esta_autenticado():
            print("Jugador:", self.sesion.nombre)
            print("Método:", self.sesion.metodo)
        
        btn_pausa = Boton("Pausa", self.ANCHO - 150, 20, 140, 50, self.pausa_unjugador, self.fuente_grande, bg_color=(0, 139, 139), fg_color="black", interfaz=self)
        BtnReiniciar = Boton("Reiniciar", self.ANCHO // 2 - 100, 680, 195, 50, self.ReiniciarUnJugador, self.fuente_grande, bg_color=(0, 139, 139), fg_color="black", interfaz=self)
        fuente_titulo = pygame.font.SysFont('Segoe UI', 30, True)
        texto_titulo = "Modo Un Jugador"

        # Crear la matriz de botones
        self.botones_unjugador = []
        ancho_btn = 80
        alto_btn = 80
        separacion = 10
        tablero_ancho = 6 * ancho_btn + 5 * separacion
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

        # ---------- Animación de patrón ----------
        self.LogicaPatrones.LongitudPatron= 3
        self.LogicaPatrones.GenerarPatronInicial()
        patron = self.LogicaPatrones.ObtenerPatron()

        # Desactivar botones durante animación
        for fila_botones in self.botones_unjugador:
            for btn in fila_botones:
                btn.disabled = True
        for (fila, col) in patron:
            boton = self.botones_unjugador[fila][col]
            boton.color_normal = pygame.Color("yellow")
            self.ActualizarPantalla()
            pygame.time.delay(500)
            boton.color_normal = pygame.Color("gray20")
            self.ActualizarPantalla()
            pygame.time.delay(200)
        # Activar botones y lógica
        for fila_botones in self.botones_unjugador:
            for btn in fila_botones:
                btn.disabled = False

        self.LogicaPatrones.IniciarVerificacion()
        self.LogicaPatrones.IniciarTemporizador()

        # ---------- LOOP PRINCIPAL ----------
        while True:
            self.pantalla.fill(self.FONDO_GRIS)
            if self.fondo:
                self.pantalla.blit(self.fondo, (0, 0))

            # Dibujar título
            titulo_render = fuente_titulo.render(texto_titulo, True, self.BLANCO)
            self.pantalla.blit(titulo_render, (self.ANCHO // 2 - titulo_render.get_width() // 2, 30))

            # Dibujar elementos
            btn_pausa.dibujar(self.pantalla)
            BtnReiniciar.dibujar(self.pantalla)
            for fila_botones in self.botones_unjugador:
                for btn in fila_botones:
                    btn.dibujar(self.pantalla)
            #Verificación automática de tiempo fuera
            if self.LogicaPatrones.Resultado is None:
                tiempo_actual = time.time()

                #Tiempo total agotado
                if self.LogicaPatrones.TiempoInicio is not None and tiempo_actual - self.LogicaPatrones.TiempoInicio > self.LogicaPatrones.TiempoTotalMax:
                    print("⏱ Tiempo total agotado. Reiniciando completamente...")
                    self.ReiniciarUnJugador()
                    return #Salir del ciclo actual
                
                #Tiempo entre clics agotado (solo si ya se ha hecho al menos un clic)
                if self.LogicaPatrones.IndiceActual > 0 and self.LogicaPatrones.TiempoUltimoClick is not None:
                    if tiempo_actual - self.LogicaPatrones.TiempoUltimoClick > self.LogicaPatrones.TiempoEntreCasillasMax:
                        print("⏱ Te tardaste más de 2 segundos entre clics. Reiniciando completamente...")
                        self.ReiniciarUnJugador()
                        return #Salir del ciclo actual
            # Eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salir()
                btn_pausa.manejar_evento(evento)
                BtnReiniciar.manejar_evento(evento)

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    for fila in range(6):
                        for col in range(6):
                            boton = self.botones_unjugador[fila][col]
                            if boton.rect.collidepoint(evento.pos) and not boton.disabled:
                                resultado = self.LogicaPatrones.VerificarCasilla((fila, col))
                                print(f"Resultado: {resultado}")
                                if resultado == 'correcto':
                                    boton.color_normal = pygame.Color("green")
                                    self.sonido.reproducir_check()
                                elif resultado == 'incorrecto':
                                    boton.color_normal = pygame.Color("red")
                                    self.sonido.reproducir_error()
                                elif resultado == 'completado':
                                    print("✅ ¡Patrón completado! Nuevo nivel...")

                                    boton.color_normal = pygame.Color("blue")
                                    pygame.time.delay(300)
                                    # 🔄 Limpiar el color del botón seleccionado antes de animar
                                    boton.color_normal = pygame.Color("gray20")
                                    self.ActualizarPantalla()
                                    pygame.time.delay(100)

                                    #Si llegó al final (36 casillas), gana $100
                                    if self.LogicaPatrones.LongitudPatron == 36:
                                        self.GaneUnJugador(monto=100)
                                        return  # Detener todo ANTES de generar nuevo patrón
                                    
                                    # Aumentar dificultad
                                    self.LogicaPatrones.LongitudPatron += 1

                                    self.LogicaPatrones.AgregarACasilla()
                                    patron = self.LogicaPatrones.ObtenerPatron()

                                    # Desactivar botones y limpiar colores
                                    for fila_botones in self.botones_unjugador:
                                        for btn in fila_botones:
                                            btn.color_normal = pygame.Color("gray20")
                                            btn.disabled = True
                                            btn.hovered = False
                                    self.ActualizarPantalla()
                                    pygame.time.delay(500)
                                    self.animando_patron = True  # Desactiva hover visual durante animación

                                    # Mostrar el nuevo patrón
                                    for (fila, col) in patron:
                                        boton = self.botones_unjugador[fila][col]
                                        boton.color_normal = pygame.Color("yellow")
                                        self.ActualizarPantalla()
                                        pygame.time.delay(500)
                                        boton.color_normal = pygame.Color("gray20")
                                        self.ActualizarPantalla()
                                        pygame.time.delay(200)
                                    self.animando_patron = False  # Desactiva hover visual durante animación

                                    # Reactivar lógica
                                    for fila_botones in self.botones_unjugador:
                                        for btn in fila_botones:
                                            btn.disabled = False
                                    self.LogicaPatrones.IniciarVerificacion()
                                    self.LogicaPatrones.IniciarTemporizador()
                                elif resultado in ('incorrecto', 'muy_lento', 'tiempo_agotado'):
                                    print("❌ Fallaste. Reintentando el mismo nivel...")
                                    self.ReiniciarUnJugador
                                    return
            self.VerificarCursor()
            pygame.display.flip()
            self.reloj.tick(self.FPS)
    
    def GaneUnJugador(self, monto=100):
        """
        Muestra una animación de victoria y guarda el premio si el usuario está autenticado.
        """
        self.botones_visibles.clear()

        # Guardar premio si hay sesión activa
        if self.sesion.esta_autenticado():
            nombre = self.sesion.nombre
            metodo = self.sesion.metodo
            if metodo == "clave":
                try:
                    PremiosClave.otorgar_premio(nombre, monto)
                except Exception as e:
                    print(f"Error al guardar premio por clave: {e}")
            elif metodo == "facial":
                try:
                    PremiosFaciales.otorgar_premio(nombre, monto)
                except Exception as e:
                    print(f"Error al guardar premio facial: {e}")

        # 🎉 Mostrar pantalla de gane
        texto_titulo = self.fuente_titulo.render("¡GANASTE!", True, (255, 215, 0))
        texto_dinero = self.fuente.render(f"Obtuviste ${monto}", True, (255, 255, 255))

        fondo_temporal = pygame.Surface((self.ANCHO, self.ALTO))
        fondo_temporal.set_alpha(200)
        fondo_temporal.fill((0, 0, 0))

        tiempo_inicio = time.time()

        while time.time() - tiempo_inicio < 4:
            self.pantalla.blit(fondo_temporal, (0, 0))
            self.pantalla.blit(texto_titulo, (self.ANCHO // 2 - texto_titulo.get_width() // 2, self.ALTO // 2 - 80))
            self.pantalla.blit(texto_dinero, (self.ANCHO // 2 - texto_dinero.get_width() // 2, self.ALTO // 2))
            pygame.display.flip()
            self.reloj.tick(self.FPS)
    
    def ActualizarPantalla(self):
        """
        Actualiza la pantalla del juego para el modo un jugador.
        Dibuja el fondo, los botones y actualiza la pantalla.
        """
        self.pantalla.fill(self.FONDO_GRIS)
        if self.fondo:
            self.pantalla.blit(self.fondo, (0, 0))
        for fila_botones in self.botones_unjugador:
            for b in fila_botones:
                b.dibujar(self.pantalla)
        pygame.display.flip()
    
    def ActualizaAmbosTableros(self):
        """
        Actualiza la pantalla del juego para el modo multijugador.
        Dibuja el fondo, los botones de ambos jugadores y actualiza la pantalla.
        """
        self.pantalla.fill(self.FONDO_GRIS)
        if self.fondo:
            self.pantalla.blit(self.fondo, (0, 0))

        for fila in self.botones_jugador1:
            for boton in fila:
                boton.dibujar(self.pantalla)

        for fila in self.botones_jugador2:
            for boton in fila:
                boton.dibujar(self.pantalla)

        pygame.display.flip()

    def pausa_unjugador(self):
        """
        Muestra una pantalla de pausa para el modo de un jugador en Pygame
        """
    
        self.botones_visibles.clear()

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
        btn_salir.fg_color = pygame.Color("black")

        btn_continuar = Boton(
            "Continuar",
            self.ANCHO // 2 - 200, self.ALTO // 2,
            400, 60,
            lambda: None,  # Cambio aquí para que sea callable
            self.fuente, 
            interfaz=self
        )
        btn_continuar.color_normal = self.CYAN_OSCURO
        btn_continuar.fg_color = pygame.Color("black")

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

    def ReiniciarUnJugador(self):
        self.LogicaPatrones.ReiniciarTodo()
        self.tablero_unjugador()
        self.GaneUnJugador() #Quitar si no funciona
    
    def pantalla_nombres_multijugador(self):
        """
        Muestra una pantalla para que los jugadores ingresen sus nombres antes de iniciar el juego multijugador.
        Permite a los jugadores ingresar sus nombres y luego iniciar el juego.
        """

        self.botones_visibles.clear()

        entrada_j1 = ""
        entrada_j2 = ""

        input_rect_j1 = pygame.Rect(self.ANCHO // 2 - 200, 200, 400, 60)
        input_rect_j2 = pygame.Rect(self.ANCHO // 2 - 200, 300, 400, 60)

        boton_iniciar = Boton("Iniciar Juego", self.ANCHO // 2 - 150, 400, 300, 60, None, self.fuente, interfaz=self)
        boton_volver = Boton("Volver", self.ANCHO // 2 - 150, 480, 300, 60, self.jugar, self.fuente, interfaz=self)

        activo_j1 = True
        activo_j2 = False

        while True:
            self.pantalla.fill(self.FONDO_GRIS)
            if self.fondo:
                self.pantalla.blit(self.fondo, (0, 0))

            titulo = self.fuente_titulo.render("Nombres de Jugadores", True, self.BLANCO)
            self.pantalla.blit(titulo, (self.ANCHO // 2 - titulo.get_width() // 2, 100))

            pygame.draw.rect(self.pantalla, pygame.Color("white") if activo_j1 else pygame.Color("gray"), input_rect_j1, 2)
            pygame.draw.rect(self.pantalla, pygame.Color("white") if activo_j2 else pygame.Color("gray"), input_rect_j2, 2)

            # Etiquetas
            label_j1 = self.fuente_pequena.render("Jugador 1", True, self.BLANCO)
            label_j2 = self.fuente_pequena.render("Jugador 2", True, self.BLANCO)

            self.pantalla.blit(label_j1, (input_rect_j1.x, input_rect_j1.y - 30))
            self.pantalla.blit(label_j2, (input_rect_j2.x, input_rect_j2.y - 30))

            # Texto dentro del campo
            texto_j1 = self.fuente_pequena.render(entrada_j1, True, self.BLANCO)
            texto_j2 = self.fuente_pequena.render(entrada_j2, True, self.BLANCO)

            self.pantalla.blit(texto_j1, (input_rect_j1.x + 10, input_rect_j1.y + 15))
            self.pantalla.blit(texto_j2, (input_rect_j2.x + 10, input_rect_j2.y + 15))

            boton_iniciar.dibujar(self.pantalla)
            boton_volver.dibujar(self.pantalla)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salir()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect_j1.collidepoint(evento.pos):
                        activo_j1 = True
                        activo_j2 = False
                    elif input_rect_j2.collidepoint(evento.pos):
                        activo_j2 = True
                        activo_j1 = False

                    if entrada_j1.strip() and entrada_j2.strip():
                        self.tablero_multijugador(entrada_j1.strip(), entrada_j2.strip())
                        return
                    boton_volver.manejar_evento(evento)


                elif evento.type == pygame.KEYDOWN:
                    if activo_j1:
                        if evento.key == pygame.K_BACKSPACE:
                            entrada_j1 = entrada_j1[:-1]
                        else:
                            entrada_j1 += evento.unicode
                    elif activo_j2:
                        if evento.key == pygame.K_BACKSPACE:
                            entrada_j2 = entrada_j2[:-1]
                        else:
                            entrada_j2 += evento.unicode

            self.VerificarCursor()
            pygame.display.flip()
            self.reloj.tick(self.FPS)

    def tablero_multijugador(self, nombre_j1="Jugador 1", nombre_j2="Jugador 2"):
        """
        Muestra el tablero de juego para el modo multijugador.
        Permite a los dos jugadores jugar entre sí, siguiendo un patrón de casillas.
        """

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

        # Variables para control de delay al fallo
        delay_fallo_activo = False
        delay_fallo_inicio = 0
        delay_fallo_duracion = 0.8  # segundos

        # Parámetros del tablero
        ancho_btn = 80
        alto_btn = 80
        separacion = 10
        filas, columnas = 6, 6

        tablero_ancho = columnas * ancho_btn + (columnas - 1) * separacion
        tablero_alto = filas * alto_btn + (filas - 1) * separacion

        # Posiciones para los dos tableros
        start_x_1 = self.ANCHO // 4 - tablero_ancho // 2
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
        
        self.ModoJuego = ModoMultijugador(ModoMultijugador.CargarImagenes(), self.botones_jugador1, self.botones_jugador2)

        # --- Mostrar las imágenes de ambos tableros por 3 segundos ---
        for fila in range(6):
            for col in range(6):
                # Mostrar en tablero del jugador 1
                img1 = self.ModoJuego.TableroJugador1[fila][col]
                self.botones_jugador1[fila][col].imagen = img1
                self.botones_jugador1[fila][col].disabled = True

                # Mostrar en tablero del jugador 2
                img2 = self.ModoJuego.TableroJugador2[fila][col]
                self.botones_jugador2[fila][col].imagen = img2
                self.botones_jugador2[fila][col].disabled = True

        self.ActualizaAmbosTableros()
        pygame.time.delay(3000)  # Mostrar por 3 segundos

        # --- Ocultar todas las imágenes ---
        for fila in range(6):
            for col in range(6):
                self.botones_jugador1[fila][col].imagen = None
                self.botones_jugador1[fila][col].disabled = False

                self.botones_jugador2[fila][col].imagen = None
                self.botones_jugador2[fila][col].disabled = False
        self.ActualizaAmbosTableros()

        # Loop principal
        while True:
            self.pantalla.fill(self.FONDO_GRIS)
            if self.fondo:
                self.pantalla.blit(self.fondo, (0, 0))

            # Dibujar título centrado arriba
            nombre_j1_render = self.fuente.render(nombre_j1, True, self.BLANCO)
            nombre_j2_render = self.fuente.render(nombre_j2, True, self.BLANCO)

            x_j1 = start_x_1 + (tablero_ancho // 2) - (nombre_j1_render.get_width() // 2)
            x_j2 = start_x_2 + (tablero_ancho // 2) - (nombre_j2_render.get_width() // 2)

            self.pantalla.blit(nombre_j1_render, (x_j1, start_y - 50))
            self.pantalla.blit(nombre_j2_render, (x_j2, start_y - 50))

            # Dibujar línea divisoria en el centro
            linea_x = self.ANCHO // 2
            pygame.draw.line(self.pantalla, pygame.Color("white"), (linea_x, start_y - 20), (linea_x, start_y + tablero_alto + 20), 4)

            # Mostrar turno actual
            texto_turno = f"Turno: Jugador {self.ModoJuego.TurnoActual}"
            turno_render = self.fuente.render(texto_turno, True, self.BLANCO)
            self.pantalla.blit(turno_render, (self.ANCHO // 2 - turno_render.get_width() // 2, 10))

            # Mostrar tiempo restante
            tiempo_pasado = time.time() - self.ModoJuego.TiempoInicioTurno
            tiempo_restante = max(0, int(self.ModoJuego.TiempoRestante - tiempo_pasado))
            tiempo_render = self.fuente.render(f"Tiempo: {tiempo_restante}s", True, self.BLANCO)
            self.pantalla.blit(tiempo_render, (self.ANCHO // 2 - tiempo_render.get_width() // 2, 50))

            # Dibujar botón pausa
            btn_pausa.dibujar(self.pantalla)

            # Dibujar botones jugador 1
            for fila_botones in self.botones_jugador1:
                for btn in fila_botones:
                    btn.dibujar(self.pantalla)

            # Dibujar botones jugador 2
            for fila_botones in self.botones_jugador2:
                for btn in fila_botones:
                    btn.dibujar(self.pantalla)

            # Mostrar imágenes de turno debajo de cada tablero
            y_img_turno = start_y + tablero_alto + 10
            x_img_turno_1 = start_x_1 + (tablero_ancho // 2) - (self.img_turno_on.get_width() // 2)
            x_img_turno_2 = start_x_2 + (tablero_ancho // 2) - (self.img_turno_off.get_width() // 2)

            if self.ModoJuego.TurnoActual == 1:
                self.pantalla.blit(self.img_turno_on, (x_img_turno_1, y_img_turno))
                self.pantalla.blit(self.img_turno_off, (x_img_turno_2, y_img_turno))
            else:
                self.pantalla.blit(self.img_turno_off, (x_img_turno_1, y_img_turno))
                self.pantalla.blit(self.img_turno_on, (x_img_turno_2, y_img_turno))

            # Verificar si estamos en delay de fallo para ocultar cartas y cambiar turno
            if delay_fallo_activo:
                if time.time() - delay_fallo_inicio >= delay_fallo_duracion:
                    # Ya pasó el delay, ocultar cartas fallidas
                    TurnoActual = self.ModoJuego.TurnoActual
                    botones_actuales = self.botones_jugador1 if TurnoActual == 1 else self.botones_jugador2
                    for f, c in self.ModoJuego.CartasSeleccionadas:
                        botones_actuales[f][c].imagen = None
                        botones_actuales[f][c].disabled = False

                    self.ModoJuego.CartasSeleccionadas.clear()

                    # Cambiar turno tras fallo
                    self.ModoJuego.TurnoActual = 2 if TurnoActual == 1 else 1
                    self.ModoJuego.ReiniciarTiempo()

                    delay_fallo_activo = False
            else:
                # Manejo de eventos sólo si no estamos en delay para evitar clicks durante espera
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        self.salir()

                    btn_pausa.manejar_evento(evento)

                    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                        TurnoActual = self.ModoJuego.TurnoActual
                        botones = self.botones_jugador1 if TurnoActual == 1 else self.botones_jugador2

                        for fila in range(6):
                            for col in range(6):
                                boton = botones[fila][col]
                                if boton.rect.collidepoint(evento.pos) and not boton.disabled:
                                    imagen = self.ModoJuego.TableroJugador1[fila][col] if TurnoActual == 1 else self.ModoJuego.TableroJugador2[fila][col]
                                    boton.imagen = imagen
                                    boton.disabled = True

                                    resultado = self.ModoJuego.SeleccionarCasilla(TurnoActual, fila, col)

                                    if resultado == "esperando":
                                        pass
                                    elif resultado == "acierto":
                                        self.sonido.reproducir_check()  # ✅ SONIDO DE ACIERTO
                                        self.ModoJuego.ReiniciarTiempo(bonificacion=7)
                                    elif resultado == "fallo":
                                        self.sonido.reproducir_error()  # ❌ SONIDO DE FALLO
                                        delay_fallo_activo = True
                                        delay_fallo_inicio = time.time()
                    self.VerificarCursor()

            # Verificar tiempo agotado para cambio de turno, pero solo si no estamos en delay
            if not delay_fallo_activo and self.ModoJuego.TiempoAgotado():
                # Ocultar y desbloquear las cartas seleccionadas del jugador que perdió el turno
                botones_actuales = self.botones_jugador1 if self.ModoJuego.TurnoActual == 1 else self.botones_jugador2
                for f, c in self.ModoJuego.CartasSeleccionadas:
                    btn = botones_actuales[f][c]
                    btn.imagen = None
                    btn.disabled = False

                self.ModoJuego.CartasSeleccionadas.clear()
                # Cambiar turno
                self.ModoJuego.TurnoActual = 2 if self.ModoJuego.TurnoActual == 1 else 1
                self.ModoJuego.ReiniciarTiempo()

                # Resetear imágenes seleccionadas que no son aciertos
                for fila in range(6):
                    for col in range(6):
                        btn = botones_actuales[fila][col]
                        if btn.disabled and (fila, col) not in (self.ModoJuego.ParesEncontradosJ1 + self.ModoJuego.ParesEncontradosJ2):
                            btn.imagen = None
                            btn.disabled = False

            if len(self.ModoJuego.ParesEncontradosJ1) == 36 or len(self.ModoJuego.ParesEncontradosJ2) == 36:
                if len(self.ModoJuego.ParesEncontradosJ1) > len(self.ModoJuego.ParesEncontradosJ2):
                    mensaje_ganador = f"¡{nombre_j1} gana!"
                elif len(self.ModoJuego.ParesEncontradosJ2) > len(self.ModoJuego.ParesEncontradosJ1):
                    mensaje_ganador = f"¡{nombre_j2} gana!"
                else:
                    mensaje_ganador = "¡Empate!"

                self.mostrar_ventana_ganador(mensaje_ganador)
                return  # salir del loop para mostrar la ventana del ganador

            pygame.display.flip()
            self.reloj.tick(self.FPS)

    def OtorgarParticipacion(self, monto=5):
        """
        Otorga premio de participación al usuario autenticado en el modo multijugador.
        """
        if self.sesion.esta_autenticado():
            nombre = self.sesion.nombre
            metodo = self.sesion.metodo
            if metodo == "clave":
                try:
                    PremiosClave.otorgar_premio(nombre, monto)
                except Exception as e:
                    print(f"Error al guardar premio por clave: {e}")
            elif metodo == "facial":
                try:
                    PremiosFaciales.otorgar_premio(nombre, monto)
                except Exception as e:
                    print(f"Error al guardar premio facial: {e}")

    def pausa_multijugador(self):
        """
        Pantalla de pausa para modo multijugador en Pygame
        """

        self.botones_visibles.clear()
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
        boton_salir.fg_color = pygame.Color("black")

        boton_continuar = Boton(
            "Continuar",
            self.ANCHO // 2 - 200, self.ALTO // 2,
            400, 60,
            None,  # Sin acción, controlamos con manejar_evento
            self.fuente,
            interfaz=self
        )
        boton_continuar.color_normal = self.CYAN_OSCURO
        boton_continuar.fg_color = pygame.Color("black")

        while True:
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
                    return False  # Aquí termina el bucle y reanuda el juego

            self.VerificarCursor()
            pygame.display.flip()
            self.reloj.tick(self.FPS)

    def mostrar_ventana_ganador(self, mensaje_ganador):
        """
        Muestra una pantalla de victoria.
        """
        self.botones_visibles.clear()
        self.OtorgarParticipacion()

        btn_volver = Boton(
            "Volver al Menú",
            self.ANCHO // 2 - 200, self.ALTO // 2 + 100,
            400, 60,
            lambda: self.ir_a_menu(),
            self.fuente,
            interfaz=self
        )
        btn_volver.color_normal = self.CYAN_OSCURO
        btn_volver.fg_color = pygame.Color("black")

        fuente_titulo = pygame.font.SysFont('Segoe UI', 40, True)
        texto = fuente_titulo.render(mensaje_ganador, True, self.BLANCO)

        ventana_activa = True
        while ventana_activa:
            self.pantalla.fill(self.FONDO_GRIS)
            if self.fondo:
                self.pantalla.blit(self.fondo, (0, 0))

            self.pantalla.blit(texto, (self.ANCHO // 2 - texto.get_width() // 2, self.ALTO // 2 - 50))

            btn_volver.dibujar(self.pantalla)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salir()
                if btn_volver.manejar_evento(evento):
                    ventana_activa = False  # Se cerrará la ventana y volverá al menú

            self.VerificarCursor()
            pygame.display.flip()
            self.reloj.tick(self.FPS)

    def pantalla_inicio(self):
        """
        Muestra la pantalla de inicio del juego.
        Permite al usuario elegir entre iniciar sesión, registrarse o salir del juego.
        """

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
        """
        Muestra la pantalla de registro del juego.
        Permite al usuario elegir entre registrarse con usuario y contraseña o con reconocimiento facial.
        """

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
        """
        Muestra la pantalla de registro con usuario y contraseña.
        Permite al usuario ingresar un nombre de usuario y una contraseña para registrarse.
        """
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
                            # Verificar si el usuario ya existe
                            if guardar.verificar_usuario_existe(texto_usuario.strip()):
                                # Si el usuario ya existe
                                messagebox.showerror("Error", "Este nombre de usuario ya está registrado.")
                            else:
                                # Registrar el usuario
                                exito = guardar.guardar_usuario(texto_usuario.strip(), texto_clave.strip())
                                if exito:
                                    messagebox.showinfo("Registro exitoso", "Usuario registrado con éxito.")
                                    texto_usuario = ""
                                    texto_clave = ""
                                else:
                                    messagebox.showerror("Error", "Hubo un problema al guardar el usuario.")
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
        """
        Muestra la pantalla de registro con reconocimiento facial.
        Permite al usuario registrarse utilizando su rostro.
        """

        rf = ReconFacial(self)
        rf.pantalla_reconocimiento()

    def modo_inicio_sesion(self):
        """
        Muestra la pantalla de inicio de sesión del juego.
        Permite al usuario ingresar su nombre de usuario y contraseña para iniciar sesión.
        También ofrece la opción de reconocimiento facial.
        """
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
                                self.sesion.iniciar_sesion(texto_usuario.strip(), "clave")
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
        """
        Muestra el menú principal del juego.
        Permite al usuario elegir entre jugar, ver premios, cómo jugar, ajustes o cerrar sesión.
        """

        sonido.reproducir_musica()
        self.botones_visibles.clear()
        botones = [
            Boton("Jugar", self.ANCHO // 2 - 370, 250, 300, 100, self.jugar, self.fuente, interfaz=self),
            Boton("About", self.ANCHO // 2 + 70, 250, 300, 100, self.about, self.fuente, interfaz=self),
            Boton("Premios", self.ANCHO // 2 - 370, 380, 300, 100, self.premios, self.fuente, interfaz=self),
            Boton("Cómo Jugar", self.ANCHO // 2 + 70, 380, 300, 100, self.como_jugar, self.fuente, interfaz=self),
            Boton("Ajustes", 20, self.ALTO - 70, 230, 50, self.ajustes, self.fuente, interfaz=self),
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
        """
        Inicia el reconocimiento facial para el inicio de sesión.
        """

        reconocimiento = ReconFacial(self)
        reconocimiento.iniciar_login_facial()