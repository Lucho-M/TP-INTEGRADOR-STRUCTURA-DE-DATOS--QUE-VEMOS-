class Catalogo:
    def _init_(self, peliculas=None):
        self._peliculas = peliculas if peliculas is not None else []

    def get_peliculas(self):
        return self._peliculas

    def agregar_pelicula(self, pelicula):
        self._peliculas.append(pelicula)

    def _repr_(self):
        return f"Catálogo con {len(self._peliculas)} películas"