"""
Proyecto 1 BI
Generador de datos de la tabla region.
"""

from generar_comun import guardar_insert

REGIONES = [
    ("CEN", "Central"),
    ("CHO", "Chorotega"),
    ("PCE", "Pacífico Central"),
    ("BRU", "Brunca"),
    ("HCA", "Huetar Caribe"),
    ("HNO", "Huetar Norte"),
]


def id_region_por_codigo():
    return {codigo: i for i, (codigo, _nombre) in enumerate(REGIONES, start=1)}


def generar_regiones():
    filas = [(i, codigo, nombre) for i, (codigo, nombre) in enumerate(REGIONES, start=1)]
    guardar_insert("region", ["id_region", "codigo_region", "nombre_region"], filas)


if __name__ == "__main__":
    generar_regiones()
