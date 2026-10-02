"""
Proyecto 1 BI
Generador de datos de la tabla agencia.
"""

from datetime import date
from generar_comun import guardar_insert

AGENCIAS = [
    ("AG-001", "Agencia Central San José",   1, date(2005, 3, 1),  16),
    ("AG-002", "Agencia Desamparados",       2, date(2009, 7, 1),  10),
    ("AG-003", "Agencia Pérez Zeledón",      5, date(2012, 2, 1),   6),
    ("AG-004", "Agencia Alajuela Centro",    6, date(2007, 5, 1),  11),
    ("AG-005", "Agencia San Carlos",         9, date(2011, 9, 1),   7),
    ("AG-006", "Agencia Cartago Centro",    11, date(2006, 1, 15), 10),
    ("AG-007", "Agencia Turrialba",         13, date(2014, 6, 1),   4),
    ("AG-008", "Agencia Heredia Centro",    14, date(2008, 4, 1),  10),
    ("AG-009", "Agencia Liberia",           17, date(2010, 3, 1),   7),
    ("AG-010", "Agencia Nicoya",            18, date(2016, 11, 1),  4),
    ("AG-011", "Agencia Puntarenas Centro", 20, date(2009, 10, 1),  7),
    ("AG-012", "Agencia Limón Centro",      23, date(2011, 2, 1),   8),
]


def generar_agencia():
    filas = [(i, codigo, nombre, ubicacion, apertura, True)
             for i, (codigo, nombre, ubicacion, apertura, _peso) in enumerate(AGENCIAS, start=1)]
    guardar_insert("agencia",
                   ["id_agencia", "codigo_agencia", "nombre_agencia", "id_ubicacion",
                    "fecha_apertura", "activa"],
                   filas)


if __name__ == "__main__":
    generar_agencia()