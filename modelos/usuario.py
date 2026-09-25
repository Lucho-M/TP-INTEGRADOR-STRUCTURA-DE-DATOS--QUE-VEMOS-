class Usuario:
    """Representa al usuario y las plataformas que tiene contratadas."""

    def __init__(self, nombre, plataformas_contratadas=None):
        self._nombre = nombre
        self._plataformas_contratadas = plataformas_contratadas if plataformas_contratadas is not None else []
        self._historial = []

    @property
    def nombre(self):
        return self._nombre

    @property
    def plataformas_contratadas(self):
        return self._plataformas_contratadas

    @property
    def historial(self):
        return self._historial

    def agregar_plataforma(self, plataforma):
        self._plataformas_contratadas.append(plataforma)

    def agregar_al_historial(self, pelicula):
        self._historial.append(pelicula)

    def __repr__(self):
        return f"Usuario: {self._nombre} - Plataformas: {', '.join(self._plataformas_contratadas)}"
