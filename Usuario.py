class Usuario:
    def _init_(self, nombre, plataformas_contratadas=None, historial=None):
        self._nombre = nombre
        self._plataformas_contratadas = (
            plataformas_contratadas if plataformas_contratadas is not None else []
        )
        self._historial = historial if historial is not None else []

    def get_nombre(self):
        return self._nombre

    def get_plataformas(self):
        return self._plataformas_contratadas

    def get_historial(self):
        return self._historial

    def agregar_plataforma(self, plataforma):
        self._plataformas_contratadas.append(plataforma)

    def agregar_al_historial(self, pelicula):
        self._historial.append(pelicula)