"""
Proyecto 1 BI
Funciones compartidas por los generadores de datos sintéticos
"""

from datetime import date
from pathlib import Path

# Carpeta donde se guardan los archivos .sql generados
CARPETA_SALIDA = Path(__file__).resolve().parent.parent / "data" / "raw"


def valor_a_sql(valor):
    """Convierte un valor de Python a su forma escrita en SQL."""
    if valor is None:
        return "NULL"
    if isinstance(valor, bool):
        return "TRUE" if valor else "FALSE"
    if isinstance(valor, float):
        return f"{valor:.2f}"
    if isinstance(valor, int):
        return str(valor)
    if isinstance(valor, date):
        return f"'{valor.isoformat()}'"
    return "'" + str(valor).replace("'", "''") + "'"


def guardar_insert(tabla, columnas, filas, notas=()):
    lineas = [f"-- Datos sintéticos de {tabla}"]
    lineas += [f"-- {nota}" for nota in notas]
    lineas.append("")

    lineas.append(f"INSERT INTO {tabla} ({', '.join(columnas)}) VALUES")
    valores = ["(" + ", ".join(valor_a_sql(v) for v in fila) + ")" for fila in filas]
    lineas.append(",\n".join(valores) + ";")
    lineas.append("")

    lineas.append(f"SELECT setval(pg_get_serial_sequence('{tabla}', '{columnas[0]}'), "
                  f"(SELECT MAX({columnas[0]}) FROM {tabla}));")

    CARPETA_SALIDA.mkdir(parents=True, exist_ok=True)
    archivo = CARPETA_SALIDA / f"datos_{tabla}.sql"
    archivo.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print(f"Generado {archivo} ({len(filas)} filas)")
    CARPETA_SALIDA.mkdir(parents=True, exist_ok=True)
    archivo = CARPETA_SALIDA / f"datos_{tabla}.sql"
    archivo.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print(f"Generado {archivo} ({len(filas)} filas)")
