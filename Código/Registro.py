from Botones import Boton
import pygame

class Registro:
    def __init__(self, interfaz):
        self.interfaz = interfaz

    def pantalla_inicio(self):
        self.interfaz.botones_visibles.clear()
        botones = [
            Boton("Iniciar Sesión", self.interfaz.ANCHO // 2 - 410, 260, 350, 160, self.interfaz.ir_a_menu, self.interfaz.fuente, interfaz=self.interfaz),
            Boton("Registrarse", self.interfaz.ANCHO // 2 + 60, 260, 350, 160, self.interfaz.ir_a_registro, self.interfaz.fuente, interfaz=self.interfaz),
            Boton("Salir", self.interfaz.ANCHO // 2 - 150, 480, 300, 60, self.interfaz.salir, self.interfaz.fuente, interfaz=self.interfaz),
        ]

        while True:
            self.interfaz.pantalla.fill(self.interfaz.FONDO_GRIS)
            if self.interfaz.fondo:
                self.interfaz.pantalla.blit(self.interfaz.fondo, (0, 0))

            titulo = self.interfaz.fuente.render("¡BIENVENIDO!", True, self.interfaz.BLANCO)
            self.interfaz.pantalla.blit(titulo, (self.interfaz.ANCHO // 2 - titulo.get_width() // 2, 100))

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.interfaz.salir()
                for boton in botones:
                    boton.manejar_evento(evento)

            for boton in botones:
                boton.dibujar(self.interfaz.pantalla)

            self.interfaz.VerificarCursor()
            pygame.display.flip()
            self.interfaz.reloj.tick(self.interfaz.FPS)

    def pantalla_registro(self):
        self.interfaz.botones_visibles.clear()
        boton_volver = Boton("Volver", self.interfaz.ANCHO // 2 - 150, 600, 300, 60, self.interfaz.volver, self.interfaz.fuente, interfaz=self.interfaz)

        while True:
            self.interfaz.pantalla.fill(self.interfaz.FONDO_GRIS)
            if self.interfaz.fondo:
                self.interfaz.pantalla.blit(self.interfaz.fondo, (0, 0))

            titulo = self.interfaz.fuente.render("Pon tu rostro aquí", True, self.interfaz.BLANCO)
            self.interfaz.pantalla.blit(titulo, (self.interfaz.ANCHO // 2 - titulo.get_width() // 2, 150))

            boton_volver.dibujar(self.interfaz.pantalla)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.interfaz.salir()
                boton_volver.manejar_evento(evento)

            self.interfaz.VerificarCursor()
            pygame.display.flip()
            self.interfaz.reloj.tick(self.interfaz.FPS)
