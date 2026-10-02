"""
Proyecto 1 BI
Generador de datos de la tabla tipo_comision.
"""

from generar_comun import guardar_insert

TIPOS_COMISION = [
    ("FOR", "Formalización",       "Porcentaje del monto aprobado, cobrado al desembolsar"),
    ("AVA", "Avalúo de garantía",  "Monto fijo por valorar la garantía hipotecaria o prendaria"),
    ("GCO", "Gestión de cobro",    "Monto fijo por cada cuota pagada con más de 30 días de atraso"),
]


def id_tipo_comision_por_codigo():
    return {codigo: i for i, (codigo, *_) in enumerate(TIPOS_COMISION, start=1)}


def generar_tipos_comision():
    filas = [(i, codigo, nombre, descripcion)
             for i, (codigo, nombre, descripcion) in enumerate(TIPOS_COMISION, start=1)]
    guardar_insert("tipo_comision",
                   ["id_tipo_comision", "codigo_comision", "nombre_comision", "descripcion"],
                   filas)


if __name__ == "__main__":
    generar_tipos_comision()
