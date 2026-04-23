from decimal import Decimal

from .logic import CalculadorImpuestos
from ..models import Orden


class OrdenBuilder:
    """
    Builder fluido: acumula datos y en build() aplica IVA (1.19) y persiste Orden.
    lista_productos: iterable de (Libro, cantidad).
    """

    def __init__(self):
        self.reset()

    def reset(self):
        self._usuario = None
        self._productos = []
        self._direccion = ""

    def con_usuario(self, usuario):
        self._usuario = usuario
        return self

    def con_productos(self, lista_productos):
        self._productos = list(lista_productos)
        return self

    def para_envio(self, direccion):
        self._direccion = direccion
        return self

    def build(self) -> Orden:
        if not self._productos:
            raise ValueError("Datos insuficientes para crear la orden.")

        total = Decimal(0)
        for libro, cantidad in self._productos:
            unitario_iva = CalculadorImpuestos.obtener_total_con_iva(libro.precio)
            total += Decimal(str(unitario_iva)) * cantidad

        libro = self._productos[0][0]
        orden = Orden.objects.create(
            usuario=self._usuario,
            libro=libro,
            total=total,
            direccion_envio=self._direccion,
        )
        self.reset()
        return orden
