import random
import time
import pandas as pd

def workshop1_task2():
    print("================================================================")
    print("=== TASK 2: RANDOMIZED ALGORITHMS (Baggage Logistics)        ===")
    print("================================================================")
    print("[INFO] Cargando 'baggage_dataset.json'...")


    try:
        df = pd.read_json('baggage_dataset.json')

    except FileNotFoundError:
        print("⚠️ ERROR: No se encontró 'baggage_dataset.json' en la carpeta.")
        return


    # Selección aleatoria de un grupo con al menos 50 maletas.
    # Se filtra de antemano (sin while) para evitar un bucle infinito.
    MIN_MALETAS = 50
    conteos = df['flight_no'].value_counts()
    elegibles = conteos[conteos >= MIN_MALETAS].index.tolist()
    columna_grupo, etiqueta_grupo = 'flight_no', 'Vuelo'

    if not elegibles:
        # En este dataset ningún vuelo tiene >= 50 maletas (máx. ~8),
        # así que se agrupa por ruta (origen-destino).
        df['ruta'] = df['origin_airport'] + '-' + df['dest_airport']
        conteos = df['ruta'].value_counts()
        elegibles = conteos[conteos >= MIN_MALETAS].index.tolist()
        columna_grupo, etiqueta_grupo = 'ruta', 'Ruta'
        if not elegibles:
            print(f"⚠️ ERROR: ningún grupo tiene al menos {MIN_MALETAS} maletas.")
            return
        print(f"[INFO] Ningún vuelo tiene >= {MIN_MALETAS} maletas; se usa agrupación por ruta.")

    grupo_objetivo = random.choice(elegibles)
    df_grupo = df[df[columna_grupo] == grupo_objetivo]

    pesos = df_grupo['weight_kg'].tolist()
    conteo_exacto = len(df_grupo)

    print(f"\n[Parte A] Muestreo Aleatorio ({etiqueta_grupo} seleccionado: {grupo_objetivo})")
    print(f"       -> Total de maletas en este grupo: {conteo_exacto}")

    # 1. MUESTREO ALEATORIO VS CÁLCULO EXACTO
    promedio_exacto = df_grupo['weight_kg'].mean()

    fraccion_muestra = 0.25
    tamano_muestra = int(conteo_exacto * fraccion_muestra)
    df_muestra = df_grupo.sample(n=tamano_muestra)
    promedio_muestra = df_muestra['weight_kg'].mean()

    error_pct = abs(promedio_muestra - promedio_exacto) / promedio_exacto * 100

    print(f"  * Peso promedio EXACTO (100% de maletas): {promedio_exacto:.2f} kg")
    print(f"  * Peso promedio MUESTREADO ({int(fraccion_muestra*100)}%):  {promedio_muestra:.2f} kg")
    print(f"  * Margen / Error relativo de estimación:   {error_pct:.2f}%")

    # 2. COMPARACIÓN DE ORDENAMIENTO
    print(f"\n[Parte B] Ejecutando comparación de ordenamiento ({conteo_exacto} elementos)...")

    def quicksort_deterministic(arr):
        if len(arr) <= 1:
            return arr
        pivote = arr[len(arr) // 2]
        izquierda = [x for x in arr if x < pivote]
        centro = [x for x in arr if x == pivote]
        derecha = [x for x in arr if x > pivote]
        return quicksort_deterministic(izquierda) + centro + quicksort_deterministic(derecha)

    def quicksort_randomized(arr):
        if len(arr) <= 1:
            return arr
        indice_pivote = random.randint(0, len(arr) - 1)
        pivote = arr[indice_pivote]
        izquierda = [x for x in arr if x < pivote]
        centro = [x for x in arr if x == pivote]
        derecha = [x for x in arr if x > pivote]
        return quicksort_randomized(izquierda) + centro + quicksort_randomized(derecha)

    pesos_det = pesos.copy()
    inicio_det = time.perf_counter()
    resultado_det = quicksort_deterministic(pesos_det)
    tiempo_det = (time.perf_counter() - inicio_det) * 1000

    pesos_aleat = pesos.copy()
    inicio_aleat = time.perf_counter()
    resultado_aleat = quicksort_randomized(pesos_aleat)
    tiempo_aleat = (time.perf_counter() - inicio_aleat) * 1000

    print(f"  * Tiempo QuickSort Determinista:  {tiempo_det:.4f} ms")
    print(f"  * Tiempo QuickSort Aleatorizado:  {tiempo_aleat:.4f} ms")
    print(f"  * ¿Resultados idénticos?:         {resultado_det == resultado_aleat}")
    print("================================================================")

if __name__ == "__main__":
    workshop1_task2()
