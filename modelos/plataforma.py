class Plataforma:
    """Representa una plataforma de streaming y las películas disponibles en ella."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._catalogo = []

    @property
    def nombre(self):
        return self._nombre

    @property
    def catalogo(self):
        return self._catalogo

    def agregar_pelicula(self, pelicula):
        self._catalogo.append(pelicula)

    def __repr__(self):
        return f"{self._nombre} ({len(self._catalogo)} películas)"
