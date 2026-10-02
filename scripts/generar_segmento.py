"""
Proyecto 1 BI
Generador de datos de la tabla segmento.
"""

from generar_comun import guardar_insert

SEGMENTOS = [
    ("APU", "Asalariado sector público", "Personas con salario de una institución pública"),
    ("APR", "Asalariado sector privado", "Personas con salario de una empresa privada"),
    ("IND", "Independiente",             "Personas que trabajan por cuenta propia"),
    ("PEN", "Pensionado",                "Personas que reciben una pensión"),
    ("PYM", "Pyme / Empresarial",        "Asociados con una pequeña o mediana empresa"),
]


def id_segmento_por_codigo():
    return {codigo: i for i, (codigo, *_) in enumerate(SEGMENTOS, start=1)}


def generar_segmentos():
    filas = [(i, codigo, nombre, descripcion)
             for i, (codigo, nombre, descripcion) in enumerate(SEGMENTOS, start=1)]
    guardar_insert("segmento", ["id_segmento", "codigo_segmento", "nombre_segmento", "descripcion"],
                   filas)


if __name__ == "__main__":
    generar_segmentos()
