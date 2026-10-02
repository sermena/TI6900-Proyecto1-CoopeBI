"""
Proyecto 1 BI
Ejecuta en orden los generadores de datos de todo el grupo.
"""

from generar_region import generar_regiones
from generar_ubicacion import generar_ubicaciones
from generar_segmento import generar_segmentos
from generar_cliente import generar_clientes
from generar_tipo_credito import generar_tipos_credito
from generar_producto_credito import generar_productos_credito
from generar_agencia import generar_agencia
from generar_credito import generar_creditos
from generar_canal_pago import generar_canales_pago
from generar_rango_atraso import generar_rangos_atraso
from generar_tipo_comision import generar_tipos_comision
from generar_pago import generar_pagos
from generar_interes import generar_intereses
from generar_comision import generar_comisiones
from generar_morosidad import generar_morosidad


def main():

    # clientes, segmentos y ubicación
    generar_regiones()
    generar_ubicaciones()
    generar_segmentos()
    clientes = generar_clientes()

    # créditos, productos de crédito y agencias
    generar_tipos_credito()
    generar_productos_credito()
    generar_agencia()
    creditos = generar_creditos()

    # pagos, canales, morosidad, intereses y comisiones
    generar_canales_pago()
    generar_rangos_atraso()
    generar_tipos_comision()
    pagos = generar_pagos(creditos, clientes)
    generar_intereses(creditos, pagos)
    generar_comisiones(creditos, pagos)
    generar_morosidad(creditos, pagos)


if __name__ == "__main__":
    main()