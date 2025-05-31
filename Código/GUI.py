import tkinter as Tk
from PIL import Image, ImageTk
import os

CYAN_OSCURO = "#4FB4CD"
FONDO_GRIS = "#343434"
FUENTE = ('Segoe UI', 20, 'bold')

IMG_FONDO_PATH = os.path.join('Imagenes', 'fondo.jpg')

class Interfaz:
    """Esta es la clase de la interfaz grafica de prototipo sus atributos y metodos son:
    @root (elementos graficos)
    @Titulo
    @Pantalla completa (fullscreen)
    @Imagen de fondo
    Metodos:
    poner_fondo
    limpiar_ventana"""
    def __init__(self, root):
        self.root = root
        self.root.title("Juego")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg=FONDO_GRIS)

        self.img_fondo = Image.open(IMG_FONDO_PATH)
        fondo = self.img_fondo.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.Resampling.LANCZOS)
        self.fondo_tk = ImageTk.PhotoImage(fondo)
        
        self.inicio_sesion_window()

    def poner_fondo(self, frame):
        """Coloca la imagen de fondo en el frame dado"""
        # Añade imagen fondo en frame (como etiqueta que cubre todo)
        label_fondo = Tk.Label(frame, image=self.fondo_tk)
        label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

    def limpiar_ventana(self):
        """Elimina todos los widgets actuales de las ventanas"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def inicio_sesion_window(self):
        """Muestra la ventana de inicio de sesión con botones de iniciar, registrar y salir"""
        self.limpiar_ventana()
        frame = Tk.Frame(self.root)
        frame.pack(fill='both', expand=True)
        self.poner_fondo(frame)

        titulo = Tk.Label(frame, text="BIENVENIDO!", font=('Segoe UI', 30, 'bold'), fg='white', bg=FONDO_GRIS)
        titulo.pack(pady=30)

        # Contenedor para botones de inicio y registro
        cont_botones = Tk.Frame(frame, bg=FONDO_GRIS)
        cont_botones.pack(fill='x', pady=150, padx=200)

        btn_iniciar = Tk.Button(cont_botones,text="Iniciar Sesión",font=('Segoe UI', 14, 'bold'), bg=CYAN_OSCURO,fg='black',width=25,height=8,command=self.menu_principal_window)
        btn_registrar = Tk.Button(
        cont_botones,text="Registrarse",font=('Segoe UI', 14, 'bold'),bg=CYAN_OSCURO,fg='black',width=25,height=8,command=self.registro_ventana )

        # Empacar uno a la izquierda y otro a la derecha
        btn_iniciar.pack(side='left', expand=True)
        btn_registrar.pack(side='right', expand=True)

        btn_salir = Tk.Button(frame, text="Salir", font=('Segoe UI', 14), bg='black', fg='white', command=self.root.quit)
        btn_salir.place(relx=0.5, rely=0.9, anchor='center')


    def registro_ventana(self):
        """Ventana de registro de reconocimento facial"""
        self.limpiar_ventana()
        frame = Tk.Frame(self.root)
        frame.pack(fill='both', expand=True)
        self.poner_fondo(frame)

        titulo = Tk.Label(frame, text="Pon tu rostro aquí", font=('Segoe UI', 40, 'bold'), fg='white', bg=FONDO_GRIS)
        titulo.pack(pady=50)

        # Botón para volver
        btn_volver = Tk.Button(frame, text="Volver", font=FUENTE, bg=CYAN_OSCURO, fg='black', command=self.inicio_sesion_window)
        btn_volver.pack(side='bottom', pady=30)

    def menu_principal_window(self):
        """Muestra el menú principal con botones
        de juego, about, premios, cómo jugar, ajustes y cerrar sesión"""
        self.limpiar_ventana()
        frame = Tk.Frame(self.root)
        frame.pack(fill='both', expand=True)
        self.poner_fondo(frame)

        # Título
        titulo = Tk.Label(frame, text="Menú Principal", font=('Segoe UI', 32, 'bold'), fg='white', bg=FONDO_GRIS)
        titulo.pack(pady=20)

        # Contenedor de botones
        cont_botones = Tk.Frame(frame, bg=FONDO_GRIS)
        cont_botones.pack(expand=False, fill='both', padx=30, pady=30)

        # Fuente intermedia
        btn_font = ('Segoe UI', 22, 'bold')

        # Crear botones con mismo tamaño visual
        btn_jugar = Tk.Button(cont_botones, text="Jugar", font=btn_font, bg=CYAN_OSCURO, fg='black', width=1, height=4, command=self.jugar_menu)
        btn_about = Tk.Button(cont_botones, text="About", font=btn_font, bg=CYAN_OSCURO, fg='black', width=10, height=2, command=self.about_window)
        btn_premios = Tk.Button(cont_botones, text="Premios", font=btn_font, bg=CYAN_OSCURO, fg='black', width=10, height=4, command=self.premios_window)
        btn_comojugar = Tk.Button(cont_botones, text="Cómo Jugar", font=btn_font, bg=CYAN_OSCURO, fg='black', width=10, height=2, command=self.comojugar_window)

        # Organizar en 2x2 
        btn_jugar.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        btn_about.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        btn_premios.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        btn_comojugar.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

        # Hacer que todas las celdas crezcan igual
        cont_botones.columnconfigure((0, 1), weight=1)
        cont_botones.rowconfigure((0, 1), weight=1)

        # Botón ajustes
        btn_ajustes = Tk.Button(frame, text="⚙", font=('Segoe UI', 20), bg=CYAN_OSCURO, fg='black', command=self.ajustes_window)
        btn_ajustes.place(relx=0.02, rely=0.95, anchor='sw')

        # Botón cerrar sesión
        btn_cerrar_sesion = Tk.Button(frame, text="Cerrar Sesión", font=('Segoe UI', 15), bg='black', fg='white', command=self.inicio_sesion_window)
        btn_cerrar_sesion.place(relx=0.95, rely=0.95, anchor='se')

    def ajustes_window(self):
        """Muestra la ventana para ajustes mas adelante volumen etc."""
        self.limpiar_ventana()
        frame = Tk.Frame(self.root, bg=FONDO_GRIS)
        frame.pack(fill='both', expand=True)
        self.poner_fondo(frame)

        titulo = Tk.Label(frame, text="Ajustes", font=('Segoe UI', 36, 'bold'), fg='white', bg=FONDO_GRIS)
        titulo.pack(pady=40)

        # Aqui se agregan los ajustes mas adelante ahi despues vemos

        btn_volver = Tk.Button(frame, text="Volver", font=FUENTE, bg=CYAN_OSCURO, fg='black', command=self.menu_principal_window)
        btn_volver.pack(side='bottom', pady=30)

    def about_window(self):
        """"Mostrar datos nuestros"""
        self.limpiar_ventana()
        frame = Tk.Frame(self.root)
        frame.pack(fill='both', expand=True)
        self.poner_fondo(frame)

        titulo = Tk.Label(frame, text="About", font=('Segoe UI', 36, 'bold'), fg='white', bg=FONDO_GRIS)
        titulo.pack(pady=30)

        texto = (
            "Desarrollado por:\n"
            "Dylan\n"
            "Windell\n\n"
            "Juego\n"
            "Proyecto "
        )
        lbl = Tk.Label(frame, text=texto, font=('Segoe UI', 24), fg='white', bg=FONDO_GRIS, justify='center')
        lbl.pack(pady=20)

        btn_volver = Tk.Button(frame, text="Volver", font=FUENTE, bg=CYAN_OSCURO, fg='black', command=self.menu_principal_window)
        btn_volver.pack(side='bottom', pady=30)

    def premios_window(self):
        """Ventana que muestra los premios en dólares (API BCCR)"""
        self.limpiar_ventana()
        frame = Tk.Frame(self.root)
        frame.pack(fill='both', expand=True)
        self.poner_fondo(frame)

        titulo = Tk.Label(frame, text="Premios (en dólares)", font=('Segoe UI', 36, 'bold'), fg='white', bg=FONDO_GRIS)
        titulo.pack(pady=30)

        # Aquí la API del banco

        btn_volver = Tk.Button(frame, text="Volver", font=FUENTE, bg=CYAN_OSCURO, fg='black', command=self.menu_principal_window)
        btn_volver.pack(side='bottom', pady=30)

    def comojugar_window(self):
        """Ventana que muestra un tutorial de como jugar"""
        self.limpiar_ventana()
        frame = Tk.Frame(self.root)
        frame.pack(fill='both', expand=True)
        self.poner_fondo(frame)

        titulo = Tk.Label(frame, text="Cómo Jugar", font=('Segoe UI', 36, 'bold'), fg='white', bg=FONDO_GRIS)
        titulo.pack(pady=30)

        # Aqui va como jugar despues

        btn_volver = Tk.Button(frame, text="Volver", font=FUENTE, bg=CYAN_OSCURO, fg='black', command=self.menu_principal_window)
        btn_volver.pack(side='bottom', pady=30)

    def jugar_menu(self):
        """Ventana que permite seleccionar el modo de juego: Un jugador o Multijugador"""
        self.limpiar_ventana()
        frame = Tk.Frame(self.root)
        frame.pack(fill='both', expand=True)
        self.poner_fondo(frame)

        titulo = Tk.Label(frame, text="Modo de Juego", font=('Segoe UI', 36, 'bold'), fg='white', bg=FONDO_GRIS)
        titulo.pack(pady=40)

        cont_botones = Tk.Frame(frame, bg=FONDO_GRIS)
        cont_botones.pack(expand=False, fill='both', padx=60, pady=100)

        btn_unjugador = Tk.Button(cont_botones, text="Un Jugador", font=('Segoe UI',40,'bold'), bg=CYAN_OSCURO, fg='black', command=self.tablero_unjugador)
        btn_multijugador = Tk.Button(cont_botones, text="Multijugador", font=('Segoe UI',40,'bold'), bg=CYAN_OSCURO, fg='black', command=self.tablero_multijugador)

        btn_unjugador.pack(side='left', expand=True, fill='both', padx=50, pady=50)
        btn_multijugador.pack(side='right', expand=True, fill='both', padx=50, pady=50)

        btn_volver = Tk.Button(frame, text="Volver", font=('Segoe UI', 16), bg='black', fg='white', command=self.menu_principal_window)
        btn_volver.place(relx=0.05, rely=0.95, anchor='sw')

    def tablero_unjugador(self):
        """Ventana del tablero de juego de un jugador"""
        self.limpiar_ventana()
        frame = Tk.Frame(self.root)
        frame.pack(fill='both', expand=True)
        self.poner_fondo(frame)


        top_bar = Tk.Frame(frame, bg=FONDO_GRIS)
        top_bar.pack(fill='x', pady=(20, 10), padx=20)

        titulo = Tk.Label(top_bar, text="Modo Un Jugador - Tablero 6x6", font=('Segoe UI', 30, 'bold'), fg='white', bg=FONDO_GRIS)
        titulo.pack(side='left', anchor='w')

        btn_pausa = Tk.Button(top_bar, text="Pausa", font=FUENTE, bg=CYAN_OSCURO, fg='black', command=self.pausa_unjugador)
        btn_pausa.pack(side='right', anchor='e')

        separador = Tk.Frame(frame, height=10, bg=FONDO_GRIS)
        separador.pack()

        # Contenedor del tablero bien centrado
        tablero_frame = Tk.Frame(frame, bg=FONDO_GRIS, width=600, height=600)
        tablero_frame.pack(pady=(10, 30))
        tablero_frame.grid_propagate(False)

        self.botones_unjugador = []
        #Matriz
        for fila in range(6):
            for col in range(6):
                btn = Tk.Button(
                    tablero_frame,
                    bg='gray20',
                    width=8,
                    height=4,
                    relief='raised',
                    state='disabled'
                )
                btn.grid(row=fila, column=col, padx=3, pady=3)
                if col == 0:
                    self.botones_unjugador.append([])
                self.botones_unjugador[fila].append(btn)

        for i in range(6):
            tablero_frame.columnconfigure(i, weight=1, minsize=95)
            tablero_frame.rowconfigure(i, weight=1, minsize=95)


     

    def pausa_unjugador(self):
        """Muestra una ventana de tipo popup para pausar el juego, salir o reanudar para el modo de un jugador"""
        popup = Tk.Toplevel(self.root)
        popup.attributes('-fullscreen', True)
        popup.configure(bg=FONDO_GRIS)

        label = Tk.Label(popup, text="Juego en Pausa", font=('Segoe UI', 40, 'bold'), fg='white', bg=FONDO_GRIS)
        label.pack(pady=100)

        btn_salir = Tk.Button(popup, text="Salir al Menú Principal", font=FUENTE, bg=CYAN_OSCURO, fg='black', command=lambda: [popup.destroy(), self.menu_principal_window()])
        btn_salir.pack(pady=30)

        btn_continuar = Tk.Button(popup, text="Continuar", font=FUENTE, bg=CYAN_OSCURO, fg='black', command=popup.destroy)
        btn_continuar.pack(pady=30)

    def tablero_multijugador(self):
        """Crea el tablero para el modo multijugador"""
        self.limpiar_ventana()
        frame = Tk.Frame(self.root)
        frame.pack(fill='both', expand=True)
        self.poner_fondo(frame)

        top_bar = Tk.Frame(frame, bg=FONDO_GRIS)
        top_bar.pack(fill='x', pady=(20, 10), padx=20)

        titulo = Tk.Label(top_bar, text="Modo Multijugador - Tablero 6x6", font=('Segoe UI', 30, 'bold'), fg='white', bg=FONDO_GRIS)
        titulo.pack(side='left', anchor='w')

        btn_pausa = Tk.Button(top_bar, text="Pausa", font=FUENTE, bg=CYAN_OSCURO, fg='black', command=self.pausa_multijugador)
        btn_pausa.pack(side='right', anchor='e')
        separador = Tk.Frame(frame, height=10, bg=FONDO_GRIS)
        separador.pack()

        tablero_frame = Tk.Frame(frame, bg=FONDO_GRIS, width=600, height=600)
        tablero_frame.pack(pady=(10, 30))
        tablero_frame.grid_propagate(False)

        self.botones_tablero = []
        #Matriz
        for fila in range(6):
            for col in range(6):
                btn = Tk.Button(
                    tablero_frame,
                    bg='gray20',
                    width=8,
                    height=4,
                    relief='raised',
                    state='disabled'
                )
                btn.grid(row=fila, column=col, padx=3, pady=3)
                if col == 0:
                    self.botones_tablero.append([])
                self.botones_tablero[fila].append(btn)

        for i in range(6):
            tablero_frame.columnconfigure(i, weight=1, minsize=95)
            tablero_frame.rowconfigure(i, weight=1, minsize=95)


      

    def pausa_multijugador(self):
        """Muestra una ventana de tipo popup para pausar el juego, salir o reanudar para el modo multijugador"""
        popup = Tk.Toplevel(self.root)
        popup.attributes('-fullscreen', True)
        popup.configure(bg=FONDO_GRIS)

        label = Tk.Label(popup, text="Juego en Pausa", font=('Segoe UI', 40, 'bold'), fg='white', bg=FONDO_GRIS)
        label.pack(pady=100)

        btn_salir = Tk.Button(popup, text="Salir al Menú Principal", font=FUENTE, bg=CYAN_OSCURO, fg='black', command=lambda: [popup.destroy(), self.menu_principal_window()])
        btn_salir.pack(pady=30)

        btn_continuar = Tk.Button(popup, text="Continuar", font=FUENTE, bg=CYAN_OSCURO, fg='black', command=popup.destroy)
        btn_continuar.pack(pady=30)

