from models.EstadoEstablecimiento import EstadoEstablecimiento
from models.EstadoAnexo import EstadoAnexo


class FSMEstablecimiento:
    def __init__(self):
        self.estados = {}
        self._estadoDesde = {}
        for e in EstadoEstablecimiento.objects.all():
            self.estados[e.nombre] = e
        self._estadoDesde[EstadoEstablecimiento.PENDIENTE] = [self.estados[EstadoEstablecimiento.REGISTRADO]]
        self._estadoDesde[EstadoEstablecimiento.REGISTRADO] = [self.estados[EstadoEstablecimiento.NO_VIGENTE], self.estados[EstadoEstablecimiento.VIGENTE]]
        self._estadoDesde[EstadoEstablecimiento.NO_VIGENTE] = [self.estados[EstadoEstablecimiento.PENDIENTE]]
        self._estadoDesde[EstadoEstablecimiento.VIGENTE] = [self.estados[EstadoEstablecimiento.NO_VIGENTE]]

    def estadosDesde(self, estado):
        return self._estadoDesde[estado.nombre]


class FSMAnexo:
    def __init__(self):
        self.estados = {}
        self._estadoDesde = {}
        for e in EstadoAnexo.objects.all():
            self.estados[e.nombre] = e
        self._estadoDesde[EstadoAnexo.PENDIENTE] = [self.estados[EstadoAnexo.REGISTRADO]]
        self._estadoDesde[EstadoAnexo.REGISTRADO] = [self.estados[EstadoAnexo.NO_VIGENTE], self.estados[EstadoAnexo.VIGENTE]]
        self._estadoDesde[EstadoAnexo.NO_VIGENTE] = [self.estados[EstadoAnexo.PENDIENTE]]
        self._estadoDesde[EstadoAnexo.VIGENTE] = [self.estados[EstadoAnexo.NO_VIGENTE]]

    def estadosDesde(self, estado):
        return self._estadoDesde[estado.nombre]
