"""
Proyecto 1 BI
Generador de datos de la tabla comision.
"""

from generar_comun import guardar_insert
from generar_credito import generar_creditos
from generar_producto_credito import PRODUCTOS
from generar_tipo_comision import id_tipo_comision_por_codigo
from generar_cliente import generar_clientes
from generar_pago import generar_pagos

# Monto fijo del avalúo según el tipo de crédito
MONTO_AVALUO = {"HIP": 150_000.0, "PRE": 60_000.0}

# Monto fijo por gestión de cobro y días de atraso a partir de los que se cobra
MONTO_GESTION_COBRO = 7_500.0
DIAS_GESTION_COBRO = 30


def generar_comisiones(creditos, pagos):
    ids_tipo = id_tipo_comision_por_codigo()
    comisiones = []

    for credito in creditos:
        producto = PRODUCTOS[credito[3] - 1]
        comisiones.append((credito[0], ids_tipo["FOR"], credito[7],
                           round(credito[11] * producto["comision"] / 100, 2)))
        if producto["tipo"] in MONTO_AVALUO:
            comisiones.append((credito[0], ids_tipo["AVA"], credito[6], MONTO_AVALUO[producto["tipo"]]))

    for pago in pagos:
        if pago[6] > DIAS_GESTION_COBRO:
            comisiones.append((pago[1], ids_tipo["GCO"], pago[5], MONTO_GESTION_COBRO))

    # Ordenar por fecha de cobro
    comisiones.sort(key=lambda c: (c[2], c[0], c[1]))
    filas = [(i, *c) for i, c in enumerate(comisiones, start=1)]

    guardar_insert("comision",
                   ["id_comision", "id_credito", "id_tipo_comision", "fecha_cobro", "monto_comision"],
                   filas)


if __name__ == "__main__":
    creditos = generar_creditos()
    generar_comisiones(creditos, generar_pagos(creditos, generar_clientes()))
