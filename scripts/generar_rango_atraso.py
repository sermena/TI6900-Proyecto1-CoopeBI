"""
Proyecto 1 BI
Generador de datos de la tabla rango_atraso.
"""

from generar_comun import guardar_insert

# (código, nombre, días mínimo, días máximo).
RANGOS_ATRASO = [
    ("R0", "Al día",           0,   0),
    ("R1", "1 a 30 días",      1,   30),
    ("R2", "31 a 60 días",     31,  60),
    ("R3", "61 a 90 días",     61,  90),
    ("R4", "91 a 180 días",    91,  180),
    ("R5", "Más de 180 días",  181, None),
]


def id_rango_por_dias(dias):
    for i, (_codigo, _nombre, minimo, maximo) in enumerate(RANGOS_ATRASO, start=1):
        if dias >= minimo and (maximo is None or dias <= maximo):
            return i


def generar_rangos_atraso():
    filas = [(i, codigo, nombre, minimo, maximo)
             for i, (codigo, nombre, minimo, maximo) in enumerate(RANGOS_ATRASO, start=1)]
    guardar_insert("rango_atraso",
                   ["id_rango", "codigo_rango", "nombre_rango", "dias_minimo", "dias_maximo"],
                   filas)


if __name__ == "__main__":
    generar_rangos_atraso()
