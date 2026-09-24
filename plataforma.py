class Plataforma:
    def _init_(self, nombre, catalogo=None):
        self._nombre = nombre
        self._catalogo = catalogo if catalogo is not None else []

    def get_nombre(self):
        return self._nombre

    def get_catalogo(self):
        return self._catalogo

    def agregar_pelicula(self, pelicula):
        self._catalogo.append(pelicula)

    def _repr_(self):
        return f"Plataforma: {self._nombre}"