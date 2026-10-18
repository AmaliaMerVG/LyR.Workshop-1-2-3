import pandas as pd
import numpy as np

def workshop3_task1():
    print("================================================================")
    print("=== TASK 1: DTMC CONSTRUCTION & STATE CLASSIFICATION         ===")
    print("================================================================")
    print("[INFO] Cargando 'baggage_graph_dataset.json'...")

    try:
        df_aristas = pd.read_json('baggage_graph_dataset.json')
    except FileNotFoundError:
        print("⚠️ ERROR: No se encontró 'baggage_graph_dataset.json' en la carpeta.")
        print("💡 Sugerencia: Ejecuta primero el generador de grafos ('generate_graph_data.py').")
        return

    print(f"[INFO] Total de rutas cargadas: {len(df_aristas)}")

    # 1. Identificar todos los aeropuertos únicos (Estados del DTMC)
    aeropuertos = sorted(list(set(df_aristas['from_airport']).union(set(df_aristas['to_airport']))))
    n_estados = len(aeropuertos)
    print(f"[INFO] Número de estados (Aeropuertos únicos, >=8): {n_estados}")
    print(f"[INFO] Listado de aeropuertos: {aeropuertos}")

    # 2. Construir la matriz de adyacencia basada en bag_count
    # M[i, j] representa el flujo de maletas desde el aeropuerto i hacia el aeropuerto j
    df_matriz = pd.DataFrame(0.0, index=aeropuertos, columns=aeropuertos)

    for _, fila in df_aristas.iterrows():
        origen = fila['from_airport']
        destino = fila['to_airport']
        maletas = fila['bag_count']
        df_matriz.loc[origen, destino] += maletas

    # 3. Normalizar la matriz para obtener la Matriz de Transición de Probabilidad P
    # Cada fila debe sumar 1 (si un aeropuerto no tiene salidas, se maneja absorbente o autorreferencial)
    sumas_filas = df_matriz.sum(axis=1)

    # Manejar aeropuertos sin salidas salientes para evitar división por cero
    for aeropuerto in aeropuertos:
        if sumas_filas[aeropuerto] == 0:
            df_matriz.loc[aeropuerto, aeropuerto] = 1.0  # Estado absorbente temporal
            sumas_filas[aeropuerto] = 1.0

    matriz_transicion = df_matriz.div(sumas_filas, axis=0)

    print("\n[Parte A] Matriz de Transición de Probabilidades P (Primeras dimensiones):")
    print(matriz_transicion.iloc[:min(5, n_estados), :min(5, n_estados)].round(4))

    # 4. Clasificación de Estados (Hubs recurrentes vs Spoke transitorios)
    print("\n[Parte B] Clasificación de Aeropuertos (Hubs vs Spoke)...")

    # Calculamos el tráfico total (entrante + saliente) por aeropuerto
    trafico_total = df_matriz.sum(axis=1) + df_matriz.sum(axis=0)
    umbral_trafico = trafico_total.mean()

    print(f"  * Tráfico promedio por aeropuerto: {umbral_trafico:.2f} maletas")

    hubs_recurrentes = []
    spokes_transitorios = []

    for aeropuerto in aeropuertos:
        # Un aeropuerto con alta conectividad y tráfico superior al promedio se clasifica como Hub (Recurrente)
        grado_salida = (matriz_transicion.loc[aeropuerto] > 0).sum()
        if trafico_total[aeropuerto] >= umbral_trafico and grado_salida >= (n_estados / 2):
            hubs_recurrentes.append(aeropuerto)
        else:
            spokes_transitorios.append(aeropuerto)

    print(f"  * Hub Airports (Clasificados como Recurrentes): {hubs_recurrentes}")
    print(f"  * Spoke Airports (Clasificados como Transitorios): {spokes_transitorios}")
    print("================================================================")

if __name__ == "__main__":
    workshop3_task1()
