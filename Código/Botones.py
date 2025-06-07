import pygame

CYAN_OSCURO = (79, 180, 205)
NEGRO = (0, 0, 0)

class Boton:
    def __init__(self, texto, x, y, ancho, alto, accion, fuente, interfaz=None, bg_color=CYAN_OSCURO, fg_color=NEGRO):
        self.texto = texto
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.accion = accion
        self.color_normal = bg_color
        # Color hover un poco más claro que el color normal:
        self.color_hover = tuple(min(c + 40, 255) for c in bg_color)
        self.fuente = fuente
        self.fg_color = fg_color
        self.disabled= False
        self.interfaz = interfaz

    def dibujar(self, surface):

        # Registrar el botón automáticamente si no está en la lista visible
        if self.interfaz and self not in self.interfaz.botones_visibles:
            self.interfaz.botones_visibles.append(self)

        mouse = pygame.mouse.get_pos()
        color = self.color_hover if self.rect.collidepoint(mouse) else self.color_normal
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        texto_render = self.fuente.render(self.texto, True, self.fg_color)
        texto_rect = texto_render.get_rect(center=self.rect.center)
        surface.blit(texto_render, texto_rect)

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(evento.pos):
                if callable(self.accion):  # Verifica que sea callable (una función)
                    self.accion()
                return True
        return False

