"""
Proyecto 1 BI
Generador de datos de la tabla morosidad.
"""

from datetime import date, timedelta
from generar_comun import guardar_insert, CARPETA_SALIDA
from generar_credito import FECHA_CORTE, generar_creditos
from generar_cliente import generar_clientes
from generar_pago import plan_de_pagos, generar_pagos
from generar_rango_atraso import id_rango_por_dias

# Días de atraso a la fecha de corte a partir de los que cambia el estado del crédito
DIAS_COBRO_JUDICIAL = 180
DIAS_CASTIGADO = 365


def fin_de_mes(fecha):
    siguiente = date(fecha.year + fecha.month // 12, fecha.month % 12 + 1, 1)
    return siguiente - timedelta(days=1)


def generar_morosidad(creditos, pagos):
    pagos_por_credito = {}
    for pago in pagos:
        pagos_por_credito.setdefault(pago[1], {})[pago[3]] = (pago[5], pago[7])

    registros, estados = [], {}
    for credito in creditos:
        plan = plan_de_pagos(credito)
        pagados = pagos_por_credito.get(credito[0], {})
        corte = fin_de_mes(credito[7])

        while corte <= FECHA_CORTE:
            principal_pagado = sum(principal for fecha, principal in pagados.values() if fecha <= corte)
            saldo = round(max(credito[11] - principal_pagado, 0), 2)
            atrasadas = [c for c in plan if c["vencimiento"] <= corte
                         and (c["numero"] not in pagados or pagados[c["numero"]][0] > corte)]

            # El crédito ya se canceló: no se registran más meses
            if saldo == 0 and not atrasadas:
                break

            dias = (corte - atrasadas[0]["vencimiento"]).days if atrasadas else 0
            registros.append((credito[0], corte, saldo, len(atrasadas),
                              round(sum(c["cuota"] for c in atrasadas), 2), dias, id_rango_por_dias(dias)))
            corte = fin_de_mes(corte + timedelta(days=1))

        if registros and registros[-1][0] == credito[0] and registros[-1][1] == FECHA_CORTE:
            if registros[-1][5] >= DIAS_CASTIGADO:
                estados[credito[0]] = "CASTIGADO"
            elif registros[-1][5] >= DIAS_COBRO_JUDICIAL:
                estados[credito[0]] = "COBRO_JUDICIAL"

    filas = [(i, *r) for i, r in enumerate(registros, start=1)]
    guardar_insert("morosidad",
                   ["id_morosidad", "id_credito", "fecha_corte", "saldo_pendiente", "cuotas_atrasadas",
                    "monto_atrasado", "dias_atraso", "id_rango"],
                   filas)

    # Actualiza el estado de los créditos con atraso grave a la fecha de corte
    with open(CARPETA_SALIDA / "datos_morosidad.sql", "a", encoding="utf-8") as archivo:
        archivo.write("\n-- Estado de los créditos con atraso grave a la fecha de corte\n")
        for estado in ("COBRO_JUDICIAL", "CASTIGADO"):
            ids = [str(i) for i, e in estados.items() if e == estado]
            if ids:
                archivo.write(f"UPDATE credito SET estado_credito = '{estado}' "
                              f"WHERE id_credito IN ({', '.join(ids)});\n")


if __name__ == "__main__":
    creditos = generar_creditos()
    generar_morosidad(creditos, generar_pagos(creditos, generar_clientes()))
