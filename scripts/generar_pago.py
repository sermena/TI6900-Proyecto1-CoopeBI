"""
Proyecto 1 BI
Generador de datos de la tabla pago.
"""

import random
from datetime import timedelta
from generar_comun import guardar_insert
from generar_credito import FECHA_CORTE, sumar_meses, generar_creditos
from generar_producto_credito import PRODUCTOS
from generar_canal_pago import CANALES
from generar_segmento import SEGMENTOS
from generar_cliente import generar_clientes

# ---------------------------------------------------------------------
# Parámetros
# ---------------------------------------------------------------------

# Semilla del generador aleatorio
SEMILLA = 2026

# Probabilidad de que un crédito vigente caiga en morosidad
PROB_MOROSO = 0.08

# Probabilidad de que un crédito tenga atrasos ocasionales
PROB_OCASIONAL = 0.25

# Probabilidad de que una cuota de un crédito con atrasos ocasionales se pague tarde
PROB_CUOTA_TARDE = 0.15

# Segmentos que pueden pagar por deducción de planilla
SEGMENTOS_PLANILLA = ("APU", "APR", "PEN")


# ---------------------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------------------

def plan_de_pagos(credito):
    """Tabla de amortización del crédito (sistema francés)."""
    desembolso, monto, plazo, tasa, cuota = credito[7], credito[11], credito[12], credito[13], credito[14]
    tasa_mensual = tasa / 100 / 12
    saldo = monto
    plan = []
    for numero in range(1, plazo + 1):
        interes = round(saldo * tasa_mensual, 2)
        principal = round(saldo, 2) if numero == plazo else round(cuota - interes, 2)
        saldo = round(saldo - principal, 2)
        plan.append({"numero": numero, "vencimiento": sumar_meses(desembolso, numero),
                     "principal": principal, "interes": interes,
                     "cuota": round(principal + interes, 2)})
    return plan


def dias_de_atraso(azar):
    return azar.choices([azar.randint(1, 15), azar.randint(16, 45), azar.randint(46, 75)],
                        weights=[60, 30, 10])[0]


def elegir_canal(azar, permitidos, preferido, dias_atraso):
    if dias_atraso > 0:
        manuales = [i for i in permitidos if not CANALES[i - 1][3]]
        return azar.choices(manuales, weights=[CANALES[i - 1][4] for i in manuales])[0]
    if azar.random() < 0.85:
        return preferido
    return azar.choices(permitidos, weights=[CANALES[i - 1][4] for i in permitidos])[0]


# ---------------------------------------------------------------------
# Generación
# ---------------------------------------------------------------------

def fechas_de_pago(azar, credito, plan):
    """Decide cuándo se paga cada cuota vencida. Las que no se pagan no aparecen."""
    vigente = credito[15] == "VIGENTE"
    perfil = azar.random()
    moroso = vigente and len(plan) >= 4 and perfil < PROB_MOROSO
    ocasional = PROB_MOROSO <= perfil < PROB_MOROSO + PROB_OCASIONAL

    if moroso:
        inicio_mora = azar.randint(3, len(plan))
        permanente = azar.random() < 0.5
        cuotas_sin_pagar = azar.randint(1, 4)

    fechas = {}
    for cuota in plan:
        numero, vencimiento = cuota["numero"], cuota["vencimiento"]

        if moroso and numero >= inicio_mora:
            if permanente:
                continue
            if numero < inicio_mora + cuotas_sin_pagar:
                # Se pone al día pagando juntas las cuotas atrasadas
                fecha = sumar_meses(credito[7], inicio_mora + cuotas_sin_pagar) + timedelta(days=azar.randint(0, 5))
                if fecha <= FECHA_CORTE:
                    fechas[numero] = fecha
                continue

        if (ocasional or moroso) and azar.random() < PROB_CUOTA_TARDE:
            fecha = vencimiento + timedelta(days=dias_de_atraso(azar))
            if fecha <= FECHA_CORTE:
                fechas[numero] = fecha
            elif not vigente:
                fechas[numero] = vencimiento
            continue

        fechas[numero] = vencimiento - timedelta(days=azar.randint(0, 4))

    return fechas


def generar_pagos(creditos, clientes):
    azar = random.Random(SEMILLA)
    segmento_por_cliente = {c[0]: SEGMENTOS[c[7] - 1][0] for c in clientes}
    pagos = []

    for credito in creditos:
        plan = [c for c in plan_de_pagos(credito) if c["vencimiento"] <= FECHA_CORTE]
        tasa_mora = PRODUCTOS[credito[3] - 1]["mora"]

        permitidos = [i for i, canal in enumerate(CANALES, start=1)
                      if canal[0] != "PLA" or segmento_por_cliente[credito[2]] in SEGMENTOS_PLANILLA]
        preferido = azar.choices(permitidos, weights=[CANALES[i - 1][4] for i in permitidos])[0]

        fechas = fechas_de_pago(azar, credito, plan)
        for cuota in plan:
            if cuota["numero"] not in fechas:
                continue
            fecha_pago = fechas[cuota["numero"]]
            dias = max(0, (fecha_pago - cuota["vencimiento"]).days)
            moratorio = round(cuota["cuota"] * tasa_mora / 100 / 365 * dias, 2)
            pagos.append([credito[0], elegir_canal(azar, permitidos, preferido, dias),
                          cuota["numero"], cuota["vencimiento"], fecha_pago, dias,
                          cuota["principal"], cuota["interes"], moratorio,
                          round(cuota["principal"] + cuota["interes"] + moratorio, 2)])

    # Ordenar por fecha de pago
    pagos.sort(key=lambda p: (p[4], p[0], p[2]))
    filas = [(i, *p) for i, p in enumerate(pagos, start=1)]

    guardar_insert("pago",
                   ["id_pago", "id_credito", "id_canal", "numero_cuota", "fecha_vencimiento_cuota",
                    "fecha_pago", "dias_atraso", "monto_principal", "monto_interes",
                    "monto_interes_moratorio", "monto_total"],
                   filas)

    # Devuelve los pagos para que los demás generadores de Persona 3 puedan usarlos
    return filas


if __name__ == "__main__":
    generar_pagos(generar_creditos(), generar_clientes())
