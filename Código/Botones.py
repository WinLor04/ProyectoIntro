import pygame

class Boton:
    sonido_global = None  # Sonido compartido entre todos los botones

    def __init__(self, texto, x, y, ancho, alto, accion, fuente, interfaz=None,
                 bg_color=(79, 180, 205), fg_color=(0, 0, 0)):
        self.texto = texto
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.accion = accion
        self.color_normal = bg_color
        self.color_hover = tuple(min(c + 40, 255) for c in bg_color)
        self.fuente = fuente
        self.fg_color = fg_color
        self.interfaz = interfaz
        self.hovered = False  # Para controlar si está el cursor encima

    def dibujar(self, surface):
        if self.interfaz and self not in self.interfaz.botones_visibles:
            self.interfaz.botones_visibles.append(self)

        mouse_pos = pygame.mouse.get_pos()
        esta_hover = self.rect.collidepoint(mouse_pos)

        # Si el mouse entra en hover y antes no estaba, reproducir sonido
        if esta_hover and not self.hovered:
            if Boton.sonido_global:
                Boton.sonido_global.reproducir_hover()
            self.hovered = True

        # Si el mouse sale del hover, resetear flag y sonido hover
        if not esta_hover and self.hovered:
            self.hovered = False
            if Boton.sonido_global:
                Boton.sonido_global.reset_hover()

        color = self.color_hover if esta_hover else self.color_normal
        pygame.draw.rect(surface, color, self.rect, border_radius=10)

        texto_render = self.fuente.render(self.texto, True, self.fg_color)
        texto_rect = texto_render.get_rect(center=self.rect.center)
        surface.blit(texto_render, texto_rect)

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(evento.pos):
                if Boton.sonido_global:
                    if self.texto.lower() in ["volver", "atrás"]:
                        Boton.sonido_global.reproducir_atras()
                    else:
                        Boton.sonido_global.reproducir_click()
                if callable(self.accion):
                    self.accion()
                return True
        return False

