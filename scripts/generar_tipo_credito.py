"""
Proyecto 1 BI
Generador de datos de la tabla tipo de credito.
"""

from generar_comun import guardar_insert

TIPOS_CREDITO = [
    ("PER", "Personal",    "FIDUCIARIA",  "Créditos de consumo respaldados por fiador o salario"),
    ("HIP", "Hipotecario", "HIPOTECARIA", "Créditos para vivienda respaldados por hipoteca"),
    ("COM", "Comercial",   "MIXTA",       "Créditos para actividades productivas de pymes"),
    ("PRE", "Prendario",   "PRENDARIA",   "Créditos respaldados por prenda sobre vehículo"),
]

def id_tipo_por_codigo():
    return {codigo: i for i, (codigo, *_) in enumerate(TIPOS_CREDITO, start=1)}

def generar_tipos_credito():
    filas = [(i, codigo, nombre, garantia, descripcion)
             for i, (codigo, nombre, garantia, descripcion) in enumerate(TIPOS_CREDITO, start=1)]
    guardar_insert("tipo_credito",
                   ["id_tipo_credito", "codigo_tipo", "nombre_tipo", "tipo_garantia", "descripcion"],
                   filas)


if __name__ == "__main__":
    generar_tipos_credito()