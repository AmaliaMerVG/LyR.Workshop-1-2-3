import hashlib
import pandas as pd

def workshop2_task3():
    print("================================================================")
    print("=== TASK 3: STREAM SAMPLING (Min-wise Hash Sampling)         ===")
    print("================================================================")
    print("[INFO] Cargando 'baggage_stream_dataset.json'...")

    try:
        df = pd.read_json('baggage_stream_dataset.json')
    except FileNotFoundError:
        print("⚠️ ERROR: No se encontró 'baggage_stream_dataset.json' en la carpeta.")
        return

    total_registros = len(df)
    print(f"[INFO] Total de registros cargados: {total_registros}")

    # 1. CÁLCULO DE LA FRACCIÓN REAL en toda la población
    print("\n[Parte A] Calculando proporción real en la población total...")

    # Agrupamos por vuelo y determinamos si el vuelo tiene al menos una maleta perdida ('lost')
    vuelo_con_perdida = df.groupby('flight_no')['status'].apply(lambda s: (s == 'lost').any())
    conteo_real_vuelos_perdida = vuelo_con_perdida.sum()
    total_vuelos_unicos = len(vuelo_con_perdida)
    fraccion_real = conteo_real_vuelos_perdida / total_vuelos_unicos

    print(f"  * Total de vuelos únicos: {total_vuelos_unicos}")
    print(f"  * Vuelos con al menos una maleta 'lost' (Real): {conteo_real_vuelos_perdida}")
    print(f"  * Fracción real de vuelos afectados (True): {fraccion_real:.4f} ({fraccion_real * 100:.2f}%)")

    # 2. MUESTREO BASADO EN HASH (Min-wise / muestreo por hash al ~10%)
    print("\n[Parte B] Ejecutando muestreo estable basado en hash (Objetivo: ~10%)...")

    fraccion_muestra_objetivo = 0.10
    vuelos_muestreados = []

    for num_vuelo in vuelo_con_perdida.index:
        # Generar un hash determinista a partir del nombre del vuelo y convertirlo a un valor flotante en [0, 1)
        valor_hash = int(hashlib.md5(num_vuelo.encode('utf-8')).hexdigest(), 16)
        hash_normalizado = (valor_hash % 10000) / 10000.0

        # Si el valor está por debajo de la fracción objetivo, se incluye en la muestra
        if hash_normalizado < fraccion_muestra_objetivo:
            vuelos_muestreados.append(num_vuelo)

    conteo_muestreados = len(vuelos_muestreados)
    tasa_muestreo_efectiva = (conteo_muestreados / total_vuelos_unicos) * 100

    # Calcular la fracción estimada dentro de la muestra
    if conteo_muestreados > 0:
        conteo_perdidas_muestra = vuelo_con_perdida.loc[vuelos_muestreados].sum()
        fraccion_estimada = conteo_perdidas_muestra / conteo_muestreados
    else:
        conteo_perdidas_muestra = 0
        fraccion_estimada = 0.0

    print(f"  * Vuelos seleccionados en la muestra: {conteo_muestreados} (Tasa real de muestra: {tasa_muestreo_efectiva:.2f}%)")
    print(f"  * Vuelos en la muestra con maletas 'lost': {conteo_perdidas_muestra}")
    print(f"  * Fracción estimada por la muestra: {fraccion_estimada:.4f} ({fraccion_estimada * 100:.2f}%)")

    # Error de estimación
    diferencia_error = abs(fraccion_estimada - fraccion_real)
    print(f"  * Diferencia absoluta (Error de estimación): {diferencia_error:.4f}")
    print("================================================================")

if __name__ == "__main__":
    workshop2_task3()
