# -*- encoding: utf-8 -*-

# -------------------------------------------------
# Clase Escena con lo metodos abstractos

class Escena:

    def __init__(self, director):
        self.director = director
        self.completado = False
        self.retardoTrasFinalizar = 60

    def update(self, *args):
        raise NotImplemented("Tiene que implementar el metodo update.")

    def eventos(self, *args):
        raise NotImplemented("Tiene que implementar el metodo eventos.")

    def dibujar(self, pantalla):
        raise NotImplemented("Tiene que implementar el metodo dibujar.")
    
    def retardo(self):
        self.retardoTrasFinalizar -= 1
        return self.retardoTrasFinalizar < 0
