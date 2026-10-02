"""
Proyecto 1 BI
Generador de datos de la tabla producto de credito.
"""

from datetime import date
from generar_comun import guardar_insert
from generar_tipo_credito import id_tipo_por_codigo

# Catálogo de productos
PRODUCTOS = [
    {"codigo": "PER-CON", "nombre": "Personal de consumo", "tipo": "PER", "monto": (500_000, 10_000_000), "plazo": (12, 72), "tasa": (15.50, 19.50), "mora": 3.00, "comision": 2.00, "lanzamiento": date(2015, 3, 1), "peso": 26},
    {"codigo": "PER-EDU", "nombre": "Personal para educación", "tipo": "PER", "monto": (300_000, 8_000_000), "plazo": (12, 60), "tasa": (12.00, 15.00), "mora": 3.00, "comision": 1.00, "lanzamiento": date(2017, 1, 15), "peso": 8},
    {"codigo": "PER-CDE", "nombre": "Consolidación de deudas", "tipo": "PER", "monto": (1_000_000, 20_000_000), "plazo": (24, 96), "tasa": (14.00, 17.50), "mora": 3.00, "comision": 2.00, "lanzamiento": date(2019, 6, 1),  "peso": 12},
    {"codigo": "HIP-VIV", "nombre": "Hipotecario vivienda", "tipo": "HIP", "monto": (20_000_000, 120_000_000), "plazo": (120, 360), "tasa": (8.50, 10.75), "mora": 2.00, "comision": 1.50, "lanzamiento": date(2014, 1, 10), "peso": 9},
    {"codigo": "HIP-CON", "nombre": "Hipotecario construcción", "tipo": "HIP", "monto": (15_000_000, 90_000_000), "plazo": (120, 300), "tasa": (9.00, 11.25), "mora": 2.00, "comision": 1.50, "lanzamiento": date(2016, 8, 1),  "peso": 5},
    {"codigo": "HIP-LOT", "nombre": "Hipotecario compra de lote", "tipo": "HIP", "monto": (8_000_000, 45_000_000), "plazo": (60, 180),  "tasa": (9.75, 12.00), "mora": 2.00, "comision": 1.50, "lanzamiento": date(2018, 2, 1),  "peso": 4},
    {"codigo": "COM-CTR", "nombre": "Comercial capital de trabajo", "tipo": "COM", "monto": (3_000_000, 40_000_000), "plazo": (12, 60), "tasa": (12.50, 16.00), "mora": 3.00, "comision": 2.50, "lanzamiento": date(2016, 4, 1), "peso": 7},
    {"codigo": "COM-INV", "nombre": "Comercial inversión pyme", "tipo": "COM", "monto": (10_000_000, 80_000_000), "plazo": (36, 120), "tasa": (11.50, 14.50), "mora": 3.00, "comision": 2.50, "lanzamiento": date(2018, 9, 1), "peso": 5},
    {"codigo": "PRE-VNU", "nombre": "Prendario vehículo nuevo", "tipo": "PRE", "monto": (6_000_000, 30_000_000), "plazo": (36, 96), "tasa": (10.00, 12.50), "mora": 2.50, "comision": 1.75, "lanzamiento": date(2015, 5, 1),  "peso": 11},
    {"codigo": "PRE-VUS", "nombre": "Prendario vehículo usado", "tipo": "PRE", "monto": (3_000_000, 18_000_000), "plazo": (24, 84), "tasa": (12.00, 14.75), "mora": 2.50, "comision": 1.75, "lanzamiento": date(2015, 5, 1), "peso": 13},
]


def generar_productos_credito():
    ids_tipo = id_tipo_por_codigo()
    filas = []
    for i, p in enumerate(PRODUCTOS, start=1):
        filas.append((i, p["codigo"], p["nombre"], ids_tipo[p["tipo"]], "CRC",
                      float(p["monto"][0]), float(p["monto"][1]),
                      p["plazo"][0], p["plazo"][1],
                      p["tasa"][0], p["tasa"][1],
                      p["mora"], p["comision"], p["lanzamiento"], True))
    guardar_insert("producto_credito",
                   ["id_producto", "codigo_producto", "nombre_producto", "id_tipo_credito", "moneda",
                    "monto_minimo", "monto_maximo", "plazo_minimo_meses", "plazo_maximo_meses",
                    "tasa_interes_min_anual", "tasa_interes_max_anual", "tasa_moratoria_anual",
                    "pct_comision_formalizacion", "fecha_lanzamiento", "activo"],
                   filas)


if __name__ == "__main__":
    generar_productos_credito()