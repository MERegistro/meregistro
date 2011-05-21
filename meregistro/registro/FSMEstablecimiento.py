from models.Estado import Estado

class FSMEstablecimiento:
    def __init__(self):
        self.estados = {}
        self._estadoDesde = {}
        for e in Estado.objects.all():
            self.estados[e.nombre] = e
        self._estadoDesde[Estado.PENDIENTE] = [self.estados[Estado.REGISTRADO]]
        self._estadoDesde[Estado.REGISTRADO] = [self.estados[Estado.NO_VIGENTE], self.estados[Estado.VIGENTE]]
        self._estadoDesde[Estado.NO_VIGENTE] = [self.estados[Estado.PENDIENTE]]
        self._estadoDesde[Estado.VIGENTE] = [self.estados[Estado.NO_VIGENTE]]

    def estadosDesde(self, estado):
        return self._estadoDesde[estado.nombre]
