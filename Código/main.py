
import tkinter as Tk
from GUI import Interfaz # importar la clase del otro archivo

class Main:
    def __init__(self):
        root = Tk.Tk()
        app=Interfaz(root)
        root.mainloop()

# Ejecutar el programa
if __name__ == "__main__":
    Main()
