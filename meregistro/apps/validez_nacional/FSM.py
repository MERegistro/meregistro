from models.EstadoSolicitud import EstadoSolicitud
"""
De Pendiente puede pasar a: controlado, retenido.
De controlado puede pasar a: retenido, evaluado, numerado.
De Retenido puede pasar a:controlado, evaluado
De Evaluado puedo pasar a: numerado
"""

class FSMSolicitud:
    def __init__(self):
        self.estados = {}
        self._estadoDesde = {}
        for e in EstadoSolicitud.objects.all():
            self.estados[e.nombre] = e
        self._estadoDesde[EstadoSolicitud.PENDIENTE] = [self.estados[EstadoSolicitud.PENDIENTE], self.estados[EstadoSolicitud.CONTROLADO], self.estados[EstadoSolicitud.RETENIDO],]
        self._estadoDesde[EstadoSolicitud.CONTROLADO] = [self.estados[EstadoSolicitud.CONTROLADO], self.estados[EstadoSolicitud.PENDIENTE], self.estados[EstadoSolicitud.RETENIDO], self.estados[EstadoSolicitud.EVALUADO],]
        self._estadoDesde[EstadoSolicitud.RETENIDO] = [self.estados[EstadoSolicitud.RETENIDO], self.estados[EstadoSolicitud.PENDIENTE], self.estados[EstadoSolicitud.CONTROLADO], self.estados[EstadoSolicitud.EVALUADO],]
        self._estadoDesde[EstadoSolicitud.EVALUADO] = [self.estados[EstadoSolicitud.EVALUADO], self.estados[EstadoSolicitud.PENDIENTE],]


    def estadosDesde(self, estado):
        return self._estadoDesde[estado.nombre]
