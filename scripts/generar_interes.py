"""
Proyecto 1 BI
Generador de datos de la tabla interes.
"""

from generar_comun import guardar_insert
from generar_credito import FECHA_CORTE, generar_creditos
from generar_cliente import generar_clientes
from generar_pago import plan_de_pagos, generar_pagos


def generar_intereses(creditos, pagos):
    intereses = []

    for credito in creditos:
        for cuota in plan_de_pagos(credito):
            if cuota["vencimiento"] <= FECHA_CORTE:
                intereses.append((credito[0], cuota["numero"], "ORDINARIO",
                                  cuota["vencimiento"], cuota["interes"]))

    for pago in pagos:
        if pago[9] > 0:
            intereses.append((pago[1], pago[3], "MORATORIO", pago[5], pago[9]))

    # Ordenar por fecha de devengo
    intereses.sort(key=lambda x: (x[3], x[0], x[1]))
    filas = [(i, *x) for i, x in enumerate(intereses, start=1)]

    guardar_insert("interes",
                   ["id_interes", "id_credito", "numero_cuota", "tipo_interes", "fecha_devengo",
                    "monto_interes"],
                   filas)


if __name__ == "__main__":
    creditos = generar_creditos()
    generar_intereses(creditos, generar_pagos(creditos, generar_clientes()))
