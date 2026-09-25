class Pelicula:
    """Representa una película del catálogo."""

    def __init__(self, titulo, anio, genero, subgenero, director, actores,
                 puntaje, duracion, plataformas, fecha_retiro=""):
        self._titulo = titulo
        self._anio = anio
        self._genero = genero
        self._subgenero = subgenero
        self._director = director
        self._actores = actores
        self._puntaje = puntaje
        self._duracion = duracion
        self._plataformas = plataformas
        self._fecha_retiro = fecha_retiro

    @property
    def titulo(self):
        return self._titulo

    @property
    def anio(self):
        return self._anio

    @property
    def genero(self):
        return self._genero

    @property
    def subgenero(self):
        return self._subgenero

    @property
    def director(self):
        return self._director

    @property
    def actores(self):
        return self._actores

    @property
    def puntaje(self):
        return self._puntaje

    @property
    def duracion(self):
        return self._duracion

    @property
    def plataformas(self):
        return self._plataformas

    @property
    def fecha_retiro(self):
        return self._fecha_retiro

    def __repr__(self):
        plataformas = ", ".join(self._plataformas) if self._plataformas else "sin plataforma"
        return f"{self._titulo} ({self._anio}) - {self._genero} - ⭐{self._puntaje} - [{plataformas}]"
