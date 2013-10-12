from models.EstadoEstablecimiento import EstadoEstablecimiento
from models.EstadoAnexo import EstadoAnexo
from models.EstadoExtensionAulica import EstadoExtensionAulica


class FSMEstablecimiento:
    def __init__(self):
        self.estados = {}
        self._estadoDesde = {}
        for e in EstadoEstablecimiento.objects.all():
            self.estados[e.nombre] = e
        self._estadoDesde[EstadoEstablecimiento.PENDIENTE] = [self.estados[EstadoEstablecimiento.REGISTRADO]]
        self._estadoDesde[EstadoEstablecimiento.REGISTRADO] = [self.estados[EstadoEstablecimiento.NO_VIGENTE]]
        self._estadoDesde[EstadoEstablecimiento.NO_VIGENTE] = [self.estados[EstadoEstablecimiento.REGISTRADO]]

    def estadosDesde(self, estado):
        return self._estadoDesde[estado.nombre]


class FSMAnexo:
    def __init__(self):
        self.estados = {}
        self._estadoDesde = {}
        for a in EstadoAnexo.objects.all():
            self.estados[a.nombre] = a
        self._estadoDesde[EstadoAnexo.PENDIENTE] = [self.estados[EstadoAnexo.REGISTRADO]]
        self._estadoDesde[EstadoAnexo.REGISTRADO] = [self.estados[EstadoAnexo.NO_VIGENTE]]
        self._estadoDesde[EstadoAnexo.NO_VIGENTE] = [self.estados[EstadoAnexo.REGISTRADO]]

    def estadosDesde(self, estado):
        return self._estadoDesde[estado.nombre]


class FSMExtensionAulica:
    def __init__(self):
        self.estados = {}
        self._estadoDesde = {}
        for e in EstadoExtensionAulica.objects.all():
            self.estados[e.nombre] = e
        self._estadoDesde[EstadoExtensionAulica.PENDIENTE] = [self.estados[EstadoExtensionAulica.REGISTRADA]]
        self._estadoDesde[EstadoExtensionAulica.REGISTRADA] = [self.estados[EstadoExtensionAulica.NO_VIGENTE]]
        self._estadoDesde[EstadoExtensionAulica.NO_VIGENTE] = [self.estados[EstadoExtensionAulica.REGISTRADA]]

    def estadosDesde(self, estado):
        return self._estadoDesde[estado.nombre]
