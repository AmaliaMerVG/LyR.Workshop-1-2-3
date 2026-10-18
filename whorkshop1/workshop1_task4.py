import random
import time
import pandas as pd

def workshop1_task4():
    print("================================================================")
    print("=== TASK 4: HASH TABLE OPERATIONS (Chaining vs Power of 2)   ===")
    print("================================================================")
    print("[INFO] Cargando 'baggage_dataset.json'...")

    try:
        df = pd.read_json('baggage_dataset.json')
    except FileNotFoundError:
        print("⚠️ ERROR: No se encontró 'baggage_dataset.json' en la carpeta.")
        return

    vuelos = df['flight_no'].tolist()
    total_maletas = len(vuelos)
    print(f"[INFO] Total de maletas cargadas para distribución: {total_maletas}")

    # Número de buckets (por ejemplo, basado en el número de vuelos únicos o un tamaño fijo)
    num_buckets = 50
    print(f"[INFO] Número de buckets disponibles (m): {num_buckets}")

    # -------------------------------------------------------------
    # 1. ESTRATEGIA 1: CHAINING (Encadenamiento Estándar)
    # -------------------------------------------------------------
    print("\n[Parte A] Simulando Chaining (Asignación Directa)...")
    tabla_encadenamiento = [[] for _ in range(num_buckets)]

    inicio_encadenamiento = time.perf_counter()
    for vuelo in vuelos:
        # Usamos un hash simple basado en el string del vuelo
        indice = abs(hash(vuelo)) % num_buckets
        tabla_encadenamiento[indice].append(vuelo)
    tiempo_encadenamiento = (time.perf_counter() - inicio_encadenamiento) * 1000

    carga_max_encadenamiento = max(len(cubeta) for cubeta in tabla_encadenamiento)
    carga_prom_encadenamiento = total_maletas / num_buckets

    print(f"  * Tiempo de inserción (Chaining): {tiempo_encadenamiento:.4f} ms")
    print(f"  * Carga máxima en un bucket:      {carga_max_encadenamiento}")
    print(f"  * Carga promedio por bucket:      {carga_prom_encadenamiento:.2f}")

    # -------------------------------------------------------------
    # 2. ESTRATEGIA 2: POWER OF TWO CHOICES (Dos Opciones)
    # -------------------------------------------------------------
    print("\n[Parte B] Simulando Power of Two Choices (Balanceo Óptimo)...")
    tabla_p2 = [[] for _ in range(num_buckets)]

    inicio_p2 = time.perf_counter()
    for vuelo in vuelos:
        # Elegir dos buckets aleatorios candidatos
        indice1 = abs(hash(vuelo + "_1")) % num_buckets
        indice2 = abs(hash(vuelo + "_2")) % num_buckets

        # Seleccionar el bucket que tenga menor cantidad de elementos acumulados
        if len(tabla_p2[indice1]) <= len(tabla_p2[indice2]):
            indice_elegido = indice1
        else:
            indice_elegido = indice2

        tabla_p2[indice_elegido].append(vuelo)
    tiempo_p2 = (time.perf_counter() - inicio_p2) * 1000

    carga_max_p2 = max(len(cubeta) for cubeta in tabla_p2)
    carga_prom_p2 = total_maletas / num_buckets

    print(f"  * Tiempo de inserción (Power of 2): {tiempo_p2:.4f} ms")
    print(f"  * Carga máxima en un bucket:        {carga_max_p2}")
    print(f"  * Carga promedio por bucket:        {carga_prom_p2:.2f}")

    # -------------------------------------------------------------
    # 3. RESUMEN COMPARATIVO
    # -------------------------------------------------------------
    print("\n[Resumen Comparativo Task 4]")
    print(f"  * Mejora en la carga máxima (Desbalance): Chaining ({carga_max_encadenamiento}) vs Power of 2 ({carga_max_p2})")
    print("================================================================")

if __name__ == "__main__":
    workshop1_task4()
