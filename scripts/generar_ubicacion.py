"""
Proyecto 1 BI
Generador de datos de la tabla ubicacion.
"""

from generar_comun import guardar_insert
from generar_region import id_region_por_codigo

# (provincia, cantón, región, peso).
UBICACIONES = [
    ("San José",   "San José",      "CEN", 18),
    ("San José",   "Desamparados",  "CEN", 12),
    ("San José",   "Goicoechea",    "CEN",  6),
    ("San José",   "Montes de Oca", "CEN",  4),
    ("San José",   "Pérez Zeledón", "BRU",  6),
    ("Alajuela",   "Alajuela",      "CEN", 12),
    ("Alajuela",   "Grecia",        "CEN",  4),
    ("Alajuela",   "San Ramón",     "CEN",  4),
    ("Alajuela",   "San Carlos",    "HNO",  7),
    ("Alajuela",   "Upala",         "HNO",  2),
    ("Cartago",    "Cartago",       "CEN", 10),
    ("Cartago",    "La Unión",      "CEN",  5),
    ("Cartago",    "Turrialba",     "CEN",  4),
    ("Heredia",    "Heredia",       "CEN",  9),
    ("Heredia",    "Santo Domingo", "CEN",  4),
    ("Heredia",    "Barva",         "CEN",  3),
    ("Guanacaste", "Liberia",       "CHO",  5),
    ("Guanacaste", "Nicoya",        "CHO",  3),
    ("Guanacaste", "Santa Cruz",    "CHO",  3),
    ("Puntarenas", "Puntarenas",    "PCE",  5),
    ("Puntarenas", "Esparza",       "PCE",  2),
    ("Puntarenas", "Corredores",    "BRU",  2),
    ("Limón",      "Limón",         "HCA",  6),
    ("Limón",      "Pococí",        "HCA",  5),
    ("Limón",      "Siquirres",     "HCA",  2),
]


def generar_ubicaciones():
    ids_region = id_region_por_codigo()
    filas = [(i, provincia, canton, ids_region[region])
             for i, (provincia, canton, region, _peso) in enumerate(UBICACIONES, start=1)]
    guardar_insert("ubicacion", ["id_ubicacion", "provincia", "canton", "id_region"], filas)


if __name__ == "__main__":
    generar_ubicaciones()
