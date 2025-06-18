import pygame
import cv2
import os
import numpy as np
import threading
import time
from Botones import Boton
from Guardar import Guardar
USERS_DIR = "users_lbph"

"""
Clase para la lógica del reconocimiento facial
"""
class ReconFacial:
    def __init__(self, interfaz):
        self.interfaz = interfaz
        if not os.path.exists(USERS_DIR):
            os.makedirs(USERS_DIR)

        self.fuente = interfaz.fuente
        self.fuente_pequena = interfaz.fuente_pequena

    def pantalla_reconocimiento(self):
        from Botones import Boton
        self.interfaz.botones_visibles.clear()

        boton_registrar = Boton("Registrar nuevo rostro", self.interfaz.ANCHO // 2 - 200, 280, 400, 80, self.registrar_rostro, self.fuente, interfaz=self.interfaz)
        boton_volver = Boton("Volver", self.interfaz.ANCHO // 2 - 150, 420, 300, 60, self.interfaz.pantalla_registro, self.fuente, interfaz=self.interfaz)

        while True:
            self.interfaz.pantalla.fill(self.interfaz.FONDO_GRIS)
            if self.interfaz.fondo:
                self.interfaz.pantalla.blit(self.interfaz.fondo, (0, 0))

            titulo = self.fuente.render("Reconocimiento Facial", True, self.interfaz.BLANCO)
            self.interfaz.pantalla.blit(titulo, (self.interfaz.ANCHO // 2 - titulo.get_width() // 2, 150))

            boton_registrar.dibujar(self.interfaz.pantalla)
            boton_volver.dibujar(self.interfaz.pantalla)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.interfaz.salir()
                boton_registrar.manejar_evento(evento)
                boton_volver.manejar_evento(evento)

            self.interfaz.VerificarCursor()
            pygame.display.flip()
            self.interfaz.reloj.tick(self.interfaz.FPS)


    def registrar_rostro(self):
        """
        Registra un nuevo rostro para un usuario.
        Verifica si el usuario ya existe en el sistema (clave o rostro).
        """
        nombre = self.pedir_texto("Ingresa tu nombre de usuario:")
        if not nombre:
            self.mensaje("Nombre inválido.", error=True)
            return

        nombre = nombre.strip().lower()

        # Verificar si el usuario ya existe (clave o rostro)
        guardar = Guardar()
        if guardar.verificar_usuario_existe(nombre):
            self.mensaje("¡Este nombre de usuario ya está registrado!", error=True)
            return

        # Si el usuario no existe, continuar con el registro del rostro
        cap = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        count = 0
        faces_data = []

        self.mensaje("Mira a la cámara. Se capturarán 10 imágenes.")

        while True:
            ret, frame = cap.read()
            if not ret:
                self.mensaje("No se pudo acceder a la cámara.", error=True)
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                face_resized = cv2.resize(face, (100, 100))
                faces_data.append(face_resized)
                count += 1

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, f"Captura {count}/10", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            cv2.imshow("Registrando rostro", frame)
            if count >= 10 or cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        if faces_data:
            mean_face = np.mean(faces_data, axis=0)
            filepath = os.path.join(USERS_DIR, f"{nombre}.npy")
            np.save(filepath, mean_face)
            self.mensaje(f"Rostro guardado correctamente como '{filepath}'")
        else:
            self.mensaje("No se capturó ningún rostro.", error=True)

    def iniciar_login_facial(self):
        self._login_facial_proceso()

    def _login_facial_proceso(self):
        try:
            known_encodings, known_names = self.load_known_faces()
            if not known_encodings:
                self.mensaje("No hay rostros registrados.", error=True)
                return

            cap = cv2.VideoCapture(0)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

            start_time = time.time()
            recognized = False

            while True:
                ret, frame = cap.read()
                if not ret:
                    self.mensaje("No se pudo acceder a la cámara.", error=True)
                    break

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    face = cv2.resize(gray[y:y+h, x:x+w], (100, 100)).flatten()
                    distances = [np.linalg.norm(face - known_enc) for known_enc in known_encodings]
                    min_distance = min(distances)
                    best_match_index = np.argmin(distances)

                    if min_distance < 2000:
                        name = known_names[best_match_index]
                        recognized = True

                    label = f"Reconocido: {name}" if recognized else "Desconocido"
                    color = (0, 255, 0) if recognized else (0, 0, 255)

                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

                    if recognized and name:
                        cv2.imshow("Login con rostro", frame)
                        cv2.waitKey(1000)
                        self.interfaz.sesion.iniciar_sesion(name, "facial")
                        self.mensaje(f"¡Bienvenido, {name}!")
                        cap.release()
                        cv2.destroyAllWindows()
                        self.interfaz.ir_a_menu()
                        return

                cv2.imshow("Login con rostro", frame)

                if time.time() - start_time > 15:
                    break

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()
            self.mensaje("No se reconoció ningún rostro.", error=True)

        except Exception as e:
            self.mensaje(f"Error inesperado: {e}", error=True)

    def load_known_faces(self):
        encodings = []
        names = []

        for file in os.listdir(USERS_DIR):
            if file.endswith(".npy"):
                path = os.path.join(USERS_DIR, file)
                encoding = np.load(path).flatten()
                encodings.append(encoding)
                names.append(os.path.splitext(file)[0])

        return encodings, names

    def mensaje(self, texto, error=False):
        print("[Mensaje]", texto)
        color = (255, 50, 50) if error else (50, 255, 50)
        msg = self.fuente_pequena.render(texto, True, color)
        self.interfaz.pantalla.blit(msg, (self.interfaz.ANCHO // 2 - msg.get_width() // 2, 650))
        pygame.display.flip()
        time.sleep(2)

    def pedir_texto(self, prompt):
  

        fuente = self.interfaz.fuente_pequena
        input_rect = pygame.Rect(self.interfaz.ANCHO // 2 - 200, self.interfaz.ALTO // 2, 400, 50)
        texto = ""
        activo = True
        reloj = pygame.time.Clock()

        boton_aceptar = Boton(
            "Aceptar",
            self.interfaz.ANCHO // 2 - 75,
            self.interfaz.ALTO // 2 + 50,
            150,
            50,
            None,
            fuente,
            interfaz=self.interfaz
        )

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.interfaz.salir()
                elif evento.type == pygame.KEYDOWN and activo:
                    if evento.key == pygame.K_ESCAPE:
                        return None
                    elif evento.key == pygame.K_RETURN:
                        return texto.strip()
                    elif evento.key == pygame.K_BACKSPACE:
                        texto = texto[:-1]
                    else:
                        texto += evento.unicode
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if boton_aceptar.rect.collidepoint(evento.pos):
                        return texto.strip()

            # Fondo desenfocado/suave
            self.interfaz.pantalla.fill(self.interfaz.FONDO_GRIS)
            if self.interfaz.fondo:
                self.interfaz.pantalla.blit(self.interfaz.fondo, (0, 0))

            # Caja modal
            caja = pygame.Rect(self.interfaz.ANCHO // 2 - 250, self.interfaz.ALTO // 2 - 120, 500, 220)
            pygame.draw.rect(self.interfaz.pantalla, (40, 40, 40), caja)
            pygame.draw.rect(self.interfaz.pantalla, pygame.Color('white'), caja, 3)

            # Título
            titulo = fuente.render(prompt, True, pygame.Color('white'))
            self.interfaz.pantalla.blit(titulo, (caja.centerx - titulo.get_width() // 2, caja.y + 20))

            # Campo de texto
            pygame.draw.rect(self.interfaz.pantalla, pygame.Color('white'), input_rect, 2)
            texto_render = fuente.render(texto, True, pygame.Color('white'))
            self.interfaz.pantalla.blit(texto_render, (input_rect.x + 10, input_rect.y + 10))

            # Botón aceptar
            boton_aceptar.dibujar(self.interfaz.pantalla)

            self.interfaz.VerificarCursor()
            pygame.display.flip()
            reloj.tick(30)