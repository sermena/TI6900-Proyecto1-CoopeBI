"""
Proyecto 1 BI
Generador de datos de la tabla credito.
"""

import random
from datetime import date, timedelta
from generar_comun import guardar_insert
from generar_producto_credito import PRODUCTOS
from generar_agencia import AGENCIAS
from generar_cliente import CLIENTES_EMPRESARIALES

# ---------------------------------------------------------------------
# Parámetros
# ---------------------------------------------------------------------

# Semilla del generador aleatorio
SEMILLA = 2026

# Cantidad de créditos a generar
CANTIDAD_CREDITOS = 1500

# Periodo en que se desembolsan los créditos
FECHA_INICIO = date(2023, 1, 1)
FECHA_CORTE = date(2026, 8, 31)

# Plazos habituales en meses
PLAZOS_HABITUALES = [12, 18, 24, 36, 48, 60, 72, 84, 96, 120, 144, 180, 240, 300, 360]


# ---------------------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------------------

def sumar_meses(fecha, meses):
    mes_total = fecha.month - 1 + meses
    anio = fecha.year + mes_total // 12
    mes = mes_total % 12 + 1
    siguiente_mes = date(anio + mes // 12, mes % 12 + 1, 1)
    ultimo_dia = (siguiente_mes - timedelta(days=1)).day
    return date(anio, mes, min(fecha.day, ultimo_dia))


def calcular_cuota(monto, tasa_anual, plazo_meses):
    tasa_mensual = tasa_anual / 100 / 12
    return monto * tasa_mensual / (1 - (1 + tasa_mensual) ** -plazo_meses)


def elegir_fecha_desembolso(azar):
    dias_periodo = (FECHA_CORTE - FECHA_INICIO).days
    while True:
        fecha = FECHA_INICIO + timedelta(days=azar.randint(0, dias_periodo))
        probabilidad = 0.6 + 0.4 * (fecha - FECHA_INICIO).days / dias_periodo
        if fecha.month in (3, 11, 12):
            probabilidad *= 1.3
        if fecha.weekday() >= 5:
            probabilidad *= 0.15
        if azar.random() < probabilidad / 1.3:
            return fecha


def elegir_monto(azar, minimo, maximo):
    proporcion = azar.betavariate(1.8, 4.0)
    monto = minimo + proporcion * (maximo - minimo)
    return round(monto / 10_000) * 10_000


# ---------------------------------------------------------------------
# Generación
# ---------------------------------------------------------------------

def crear_credito(azar):
    id_producto = azar.choices(range(1, len(PRODUCTOS) + 1),
                               weights=[p["peso"] for p in PRODUCTOS])[0]
    producto = PRODUCTOS[id_producto - 1]
    id_agencia = azar.choices(range(1, len(AGENCIAS) + 1),
                              weights=[a[4] for a in AGENCIAS])[0]

    if producto["tipo"] == "COM":
        id_cliente = azar.randint(*CLIENTES_EMPRESARIALES)
    else:
        id_cliente = azar.randint(1, CLIENTES_EMPRESARIALES[0] - 1)

    desembolso = elegir_fecha_desembolso(azar)
    aprobacion = desembolso - timedelta(days=azar.randint(1, 7))
    dias_tramite = 30 if producto["tipo"] == "HIP" else 12
    solicitud = aprobacion - timedelta(days=azar.randint(2, dias_tramite))

    plazo = azar.choice([p for p in PLAZOS_HABITUALES
                         if producto["plazo"][0] <= p <= producto["plazo"][1]])
    monto_aprobado = elegir_monto(azar, *producto["monto"])
    tasa = round(azar.uniform(*producto["tasa"]) * 4) / 4

    monto_solicitado = monto_aprobado
    if azar.random() < 0.30:
        aumento = azar.uniform(1.05, 1.30)
        monto_solicitado = min(producto["monto"][1],
                               round(monto_aprobado * aumento / 10_000) * 10_000)

    vencimiento = sumar_meses(desembolso, plazo)

    return {
        "cliente": id_cliente, "producto": id_producto, "agencia": id_agencia,
        "solicitud": solicitud, "aprobacion": aprobacion, "desembolso": desembolso,
        "primer_pago": sumar_meses(desembolso, 1), "vencimiento": vencimiento,
        "monto_solicitado": float(monto_solicitado), "monto_aprobado": float(monto_aprobado),
        "plazo": plazo, "tasa": tasa,
        "cuota": round(calcular_cuota(monto_aprobado, tasa, plazo), 2),
        "estado": "CANCELADO" if vencimiento <= FECHA_CORTE else "VIGENTE",
    }


def generar_creditos():
    azar = random.Random(SEMILLA)
    creditos = [crear_credito(azar) for _ in range(CANTIDAD_CREDITOS)]

    # Ordenar por fecha
    creditos.sort(key=lambda c: c["desembolso"])

    # Número de operación
    filas, consecutivo_por_anio = [], {}
    for i, c in enumerate(creditos, start=1):
        anio = c["desembolso"].year
        consecutivo_por_anio[anio] = consecutivo_por_anio.get(anio, 0) + 1
        numero_operacion = f"OP-{anio}-{consecutivo_por_anio[anio]:06d}"
        filas.append((i, numero_operacion, c["cliente"], c["producto"], c["agencia"],
                      c["solicitud"], c["aprobacion"], c["desembolso"], c["primer_pago"],
                      c["vencimiento"], c["monto_solicitado"], c["monto_aprobado"],
                      c["plazo"], c["tasa"], c["cuota"], c["estado"]))

    guardar_insert("credito",
                   ["id_credito", "numero_operacion", "id_cliente", "id_producto", "id_agencia",
                    "fecha_solicitud", "fecha_aprobacion", "fecha_desembolso", "fecha_primer_pago",
                    "fecha_vencimiento", "monto_solicitado", "monto_aprobado", "plazo_meses",
                    "tasa_interes_anual", "cuota_mensual", "estado_credito"],
                   filas)

    # Devuelve los créditos para que otros generadores puedan usarlos
    return filas


if __name__ == "__main__":
    generar_creditos()
