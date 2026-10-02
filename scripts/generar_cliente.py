"""
Proyecto 1 BI
Generador de datos de la tabla cliente.
"""

import random
from datetime import date, timedelta
from generar_comun import guardar_insert
from generar_segmento import id_segmento_por_codigo
from generar_ubicacion import UBICACIONES

# ---------------------------------------------------------------------
# Parámetros
# ---------------------------------------------------------------------

# Semilla del generador aleatorio
SEMILLA = 2026

# Cantidad de clientes a generar
CANTIDAD_CLIENTES = 500

# Clientes del segmento Pyme / Empresarial
CLIENTES_EMPRESARIALES = (401, CANTIDAD_CLIENTES)

# Peso de cada segmento entre los clientes que no son Pyme
PESOS_SEGMENTO = {"APU": 30, "APR": 35, "IND": 15, "PEN": 20}

# Último día en que un cliente pudo asociarse
FECHA_INGRESO_MAXIMA = date(2022, 12, 31)

PROVINCIAS = ["San José", "Alajuela", "Cartago", "Heredia", "Guanacaste", "Puntarenas", "Limón"]

NOMBRES = ["José", "Juan", "Luis", "Carlos", "Andrés", "Daniel", "Diego", "Eliam", "Mario", "Pablo",
           "Ricardo", "Allan", "Alejandro", "Fernando", "Sergio", "María", "Ana", "Laura", "Carolina",
           "Daniela", "Gabriela", "Sofía", "Valeria", "Andrea", "Mónica", "Sara", "Silvia",
           "Natalia", "Paola", "Melissa"]

APELLIDOS = ["Rodríguez", "Jiménez", "Mora", "González", "Vargas", "Rojas", "Hernández", "Mena",
             "Ramírez", "Castro", "Araya", "Solís", "Segura", "Alvarado", "Quesada", "Méndez",
             "Salazar", "Madrigal", "Zúñiga", "Calderón", "Brenes", "Arias", "Segura", "Villalobos",
             "Campos", "Fallas", "Vives", "Valverde", "Ulate", "Badilla"]


# ---------------------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------------------

def fecha_aleatoria(azar, inicio, fin):
    return inicio + timedelta(days=azar.randint(0, (fin - inicio).days))


def crear_identificacion(azar, provincia, usadas):
    while True:
        identificacion = f"{PROVINCIAS.index(provincia) + 1}-{azar.randint(100, 1999):04d}-{azar.randint(1, 999):04d}"
        if identificacion not in usadas:
            usadas.add(identificacion)
            return identificacion


# ---------------------------------------------------------------------
# Generación
# ---------------------------------------------------------------------

def generar_clientes():
    azar = random.Random(SEMILLA)
    ids_segmento = id_segmento_por_codigo()
    usadas = set()
    filas = []

    for id_cliente in range(1, CANTIDAD_CLIENTES + 1):
        if id_cliente >= CLIENTES_EMPRESARIALES[0]:
            segmento = "PYM"
        else:
            segmento = azar.choices(list(PESOS_SEGMENTO), weights=list(PESOS_SEGMENTO.values()))[0]

        id_ubicacion = azar.choices(range(1, len(UBICACIONES) + 1),
                                    weights=[u[3] for u in UBICACIONES])[0]
        provincia = UBICACIONES[id_ubicacion - 1][0]

        if segmento == "PEN":
            nacimiento = fecha_aleatoria(azar, date(1950, 1, 1), date(1966, 12, 31))
        else:
            nacimiento = fecha_aleatoria(azar, date(1966, 1, 1), date(2003, 12, 31))

        mayoria_edad = date(nacimiento.year + 18, nacimiento.month, min(nacimiento.day, 28))
        ingreso = fecha_aleatoria(azar, max(date(2005, 1, 1), mayoria_edad), FECHA_INGRESO_MAXIMA)

        filas.append((id_cliente, crear_identificacion(azar, provincia, usadas),
                      azar.choice(NOMBRES), azar.choice(APELLIDOS), azar.choice(APELLIDOS),
                      nacimiento, ingreso, ids_segmento[segmento], id_ubicacion, True))

    guardar_insert("cliente",
                   ["id_cliente", "numero_identificacion", "nombre", "primer_apellido",
                    "segundo_apellido", "fecha_nacimiento", "fecha_ingreso", "id_segmento",
                    "id_ubicacion", "activo"],
                   filas)

    # Devuelve los clientes para que otros generadores puedan usarlos
    return filas


if __name__ == "__main__":
    generar_clientes()
