import random
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def workshop1_dashboard():
    print("================================================================")
    print("=== TASK 6: DASHBOARD & VISUALIZATION (Airline Baggage)      ===")
    print("================================================================")
    print("[INFO] Cargando 'baggage_dataset.json'...")

    try:
        df = pd.read_json('baggage_dataset.json')
    except FileNotFoundError:
        print("⚠️ ERROR: No se encontró 'baggage_dataset.json' en la carpeta.")
        return

    # Configuración de estilo visual
    sns.set_theme(style="whitegrid")
    figura, ejes = plt.subplots(1, 3, figsize=(18, 6))
    figura.suptitle("Dashboard Operativo - Airline Baggage Tracking & Logistics", fontsize=16, fontweight='bold')

    # -------------------------------------------------------------
    # PANEL A: Distribución de carga por bucket (Encadenamiento vs Potencia de 2)
    # -------------------------------------------------------------
    print("[INFO] Generando Panel A (Distribución de buckets)...")
    vuelos = df['flight_no'].tolist()
    num_buckets = 50

    # Encadenamiento (Chaining)
    tabla_encadenamiento = [0] * num_buckets
    for vuelo in vuelos:
        indice = abs(hash(vuelo)) % num_buckets
        tabla_encadenamiento[indice] += 1

    # Potencia de dos opciones (Power of Two Choices)
    tabla_p2 = [0] * num_buckets
    for vuelo in vuelos:
        indice1 = abs(hash(vuelo + "_1")) % num_buckets
        indice2 = abs(hash(vuelo + "_2")) % num_buckets
        elegido = indice1 if tabla_p2[indice1] <= tabla_p2[indice2] else indice2
        tabla_p2[elegido] += 1

    df_panel_a = pd.DataFrame({
        'Bucket': list(range(num_buckets)) * 2,
        'Carga': tabla_encadenamiento + tabla_p2,
        'Estrategia': ['Chaining'] * num_buckets + ['Power of Two Choices'] * num_buckets
    })

    sns.histplot(data=df_panel_a, x='Carga', hue='Estrategia', multiple='dodge', bins=10, ax=ejes[0], palette='Set2')
    ejes[0].set_title("Panel A: Chaining vs Power of 2")
    ejes[0].set_xlabel("Carga por Bucket")
    ejes[0].set_ylabel("Frecuencia")

    # -------------------------------------------------------------
    # PANEL B: Tiempo de ejecución: QuickSort Aleatorizado vs Determinista
    # -------------------------------------------------------------
    print("[INFO] Generando Panel B (Comparación de QuickSort)...")

    def quicksort_det(arr):
        if len(arr) <= 1: return arr
        pivote = arr[len(arr) // 2]
        return quicksort_det([x for x in arr if x < pivote]) + [x for x in arr if x == pivote] + quicksort_det([x for x in arr if x > pivote])

    def quicksort_rand(arr):
        if len(arr) <= 1: return arr
        pivote = arr[random.randint(0, len(arr) - 1)]
        return quicksort_rand([x for x in arr if x < pivote]) + [x for x in arr if x == pivote] + quicksort_rand([x for x in arr if x > pivote])

    tamanos = [100, 500, 1000, 2000, 5000]
    tiempos_det, tiempos_aleat = [], []

    conjunto_pesos = df['weight_kg'].tolist()
    for tam in tamanos:
        sub_arreglo = random.choices(conjunto_pesos, k=tam)

        t0 = time.perf_counter()
        quicksort_det(sub_arreglo.copy())
        tiempos_det.append((time.perf_counter() - t0) * 1000)

        t0 = time.perf_counter()
        quicksort_rand(sub_arreglo.copy())
        tiempos_aleat.append((time.perf_counter() - t0) * 1000)

    df_panel_b = pd.DataFrame({
        'Tamaño': tamanos * 2,
        'Tiempo (ms)': tiempos_det + tiempos_aleat,
        'Algoritmo': ['Determinista'] * len(tamanos) + ['Aleatorizado'] * len(tamanos)
    })

    sns.lineplot(data=df_panel_b, x='Tamaño', y='Tiempo (ms)', hue='Algoritmo', marker='o', ax=ejes[1], palette='tab10')
    ejes[1].set_title("Panel B: QuickSort Runtime")
    ejes[1].set_xlabel("Tamaño de Entrada (n)")
    ejes[1].set_ylabel("Tiempo (ms)")

    # -------------------------------------------------------------
    # PANEL C: Embudo de maletas por estado del vuelo
    # -------------------------------------------------------------
    print("[INFO] Generando Panel C (Embudo de estados)...")
    orden_estados = ['checked_in', 'loaded', 'transferred', 'delivered', 'lost']
    conteo_estados = df['status'].value_counts().reindex(orden_estados).fillna(0).reset_index()
    conteo_estados.columns = ['Estado', 'Cantidad']

    sns.barplot(data=conteo_estados, x='Estado', y='Cantidad', ax=ejes[2], palette='Blues_r')
    ejes[2].set_title("Panel C: Embudo de Estados de Maletas")
    ejes[2].set_xlabel("Estado del Equipaje")
    ejes[2].set_ylabel("Cantidad de Maletas")
    ejes[2].tick_params(axis='x', rotation=30)

    plt.tight_layout()
    archivo_salida = "workshop1_dashboard.png"
    plt.savefig(archivo_salida, dpi=300)
    print(f"[INFO] Dashboard guardado exitosamente como '{archivo_salida}'.")
    plt.show()
    print("================================================================")

if __name__ == "__main__":
    workshop1_dashboard()
