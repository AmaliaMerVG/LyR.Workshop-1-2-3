import json
import time

def task1_workshop1():
    # -------------------------------------------------------------
    # 1. PARÁMETROS REALES (Observatorio de Turismo / El Dorado H1 2026)
    # -------------------------------------------------------------
    pasajeros_semestre = 11_200_000   # 11.2 millones en el primer semestre
    dias_semestre = 181               # Enero a Junio (181 días)

    # Promedio diario de pasajeros reales en el semestre
    pasajeros_diarios_base = pasajeros_semestre / dias_semestre

    # Parámetros del modelo
    MALETAS_POR_PASAJERO = 1.2        # Promedio estándar de equipaje
    ESCANEOS_POR_MALETA = 4           # Puntos: check_in, loaded, transferred, delivered
    FACTOR_HORA_PICO = 2.5            # Concentración en picos operativos
    FACTOR_ESCALA = 10                # Requisito del taller (10x tráfico)

    # -------------------------------------------------------------
    # 2. CÁLCULOS A ESCALA 10x
    # -------------------------------------------------------------
    pasajeros_10x = pasajeros_diarios_base * FACTOR_ESCALA
    maletas_10x = pasajeros_10x * MALETAS_POR_PASAJERO
    escaneos_10x = maletas_10x * ESCANEOS_POR_MALETA

    segundos_por_dia = 86400
    escaneos_seg_promedio = escaneos_10x / segundos_por_dia
    escaneos_seg_pico = escaneos_seg_promedio * FACTOR_HORA_PICO

    # Almacenamiento estimado (~300 bytes por evento JSON)
    bytes_por_registro = 300
    almacenamiento_gb_dia = (escaneos_10x * bytes_por_registro) / (1024 ** 3)

    # -------------------------------------------------------------
    # 3. REPORTE DE RESULTADOS
    # -------------------------------------------------------------
    print("================================================================")
    print("=== TASK 1: BIG DATA CONTEXT (El Dorado - Datos H1 2026)      ===")
    print("================================================================")
    print(f"Pasajeros H1 2026 (Real Oficial):       {pasajeros_semestre:>15,}")
    print(f"Pasajeros diarios promedio (Real):      {pasajeros_diarios_base:>15,.2f}")
    print(f"Pasajeros diarios con escala 10x:       {pasajeros_10x:>15,.2f}")
    print("----------------------------------------------------------------")
    print(f"Maletas diarias procesadas (10x):       {maletas_10x:>15,.2f}")
    print(f"Escaneos totales diarios (4 puntos):    {escaneos_10x:>15,.2f}")
    print("----------------------------------------------------------------")
    print(f"Tasa promedio de escaneos por segundo:  {escaneos_seg_promedio:>15.2f} esc/s")
    print(f"Tasa estimada en Hora Pico (2.5x):      {escaneos_seg_pico:>15.2f} esc/s")
    print("----------------------------------------------------------------")
    print(f"Almacenamiento diario requerido (10x):  {almacenamiento_gb_dia:>14.2f} GB / día")
    print(f"Almacenamiento anual proyectado:        {(almacenamiento_gb_dia * 365) / 1024:>14.2f} TB / año")
    print("================================================================")

if __name__ == "__main__":
    task1_workshop1()
