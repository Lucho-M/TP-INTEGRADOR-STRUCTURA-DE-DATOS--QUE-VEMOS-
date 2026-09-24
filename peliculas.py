class Pelicula:
    def _init_(self, titulo, anio, genero, director, elenco, puntaje, duracion, plataformas, fecha_retiro):
        self._titulo = titulo
        self._anio = anio
        self._genero = genero
        self._director = director
        self._elenco = elenco
        self._puntaje = puntaje
        self._duracion = duracion
        self._plataformas = plataformas
        self._fecha_retiro = fecha_retiro

    def get_titulo(self):
        return self._titulo

    def get_anio(self):
        return self._anio

    def get_genero(self):
        return self._genero

    def get_puntaje(self):
        return self._puntaje

    def _repr_(self):
        return f"{self._titulo} ({self._anio}) - {self._genero}"