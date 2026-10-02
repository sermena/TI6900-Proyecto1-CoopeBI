"""
Proyecto 1 BI
Generador de datos de la tabla canal_pago.
"""

from generar_comun import guardar_insert

# (código, nombre, es digital, es automático, peso)
CANALES = [
    ("VEN", "Ventanilla en agencia",  False, False, 22),
    ("PLA", "Deducción de planilla",  False, True,  30),
    ("SIN", "SINPE Móvil",            True,  False, 18),
    ("BEL", "Banca en línea",         True,  False, 15),
    ("APP", "Aplicación móvil",       True,  False, 10),
    ("DEB", "Débito automático",      True,  True,   5),
]


def generar_canales_pago():
    filas = [(i, codigo, nombre, digital)
             for i, (codigo, nombre, digital, _automatico, _peso) in enumerate(CANALES, start=1)]
    guardar_insert("canal_pago", ["id_canal", "codigo_canal", "nombre_canal", "es_digital"], filas)


if __name__ == "__main__":
    generar_canales_pago()
