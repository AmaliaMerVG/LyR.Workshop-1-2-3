import pandas as pd
import numpy as np

def workshop3_task3():
    print("================================================================")
    print("=== TASK 3: TELEPORTATION PAGERANK (Airport Ranking & Hubs)    ===")
    print("================================================================")
    print("[INFO] Cargando 'baggage_graph_dataset.json'...")

    try:
        df_aristas = pd.read_json('baggage_graph_dataset.json')
    except FileNotFoundError:
        print("⚠️ ERROR: No se encontró 'baggage_graph_dataset.json' en la carpeta.")
        return

    # 1. Construir la matriz de adyacencia y transición
    aeropuertos = sorted(list(set(df_aristas['from_airport']).union(set(df_aristas['to_airport']))))
    n = len(aeropuertos)
    df_matriz = pd.DataFrame(0.0, index=aeropuertos, columns=aeropuertos)

    for _, fila in df_aristas.iterrows():
        df_matriz.loc[fila['from_airport'], fila['to_airport']] += fila['bag_count']

    sumas_filas = df_matriz.sum(axis=1)
    for aeropuerto in aeropuertos:
        if sumas_filas[aeropuerto] == 0:
            df_matriz.loc[aeropuerto, aeropuerto] = 1.0
            sumas_filas[aeropuerto] = 1.0

    M = df_matriz.div(sumas_filas, axis=0).values

    # 2. PageRank con Teleportación (d = 0.85)
    print("\n[Parte A] Ejecutando algoritmo PageRank (d = 0.85)...")
    d = 0.85
    # Vector de probabilidad inicial uniforme
    pr = np.ones(n) / n
    matriz_teletransporte = np.ones((n, n)) / n

    # Matriz de Google (matriz estocástica con factor de amortiguación)
    G = d * M + (1 - d) * matriz_teletransporte

    # Método iterativo de la potencia para converger PageRank
    for _ in range(100):
        pr_siguiente = pr @ G
        if np.linalg.norm(pr_siguiente - pr, ord=1) < 1e-6:
            break
        pr = pr_siguiente

    # 3. Comparación con el ranking de tráfico bruto
    trafico_bruto = df_matriz.sum(axis=1) + df_matriz.sum(axis=0)
    ranking_bruto = trafico_bruto.rank(ascending=False, method='min')

    # Crear DataFrame comparativo
    df_ranking = pd.DataFrame({
        'Aeropuerto': aeropuertos,
        'PageRank Score': pr,
        'Tráfico Bruto': trafico_bruto.values
    })

    df_ranking['Rank PageRank'] = df_ranking['PageRank Score'].rank(ascending=False, method='min').astype(int)
    df_ranking['Rank Tráfico Bruto'] = df_ranking['Tráfico Bruto'].rank(ascending=False, method='min').astype(int)

    df_ranking = df_ranking.sort_values(by='PageRank Score', ascending=False)

    print("\n[Parte B] Comparación de Rankings (PageRank vs Tráfico Bruto):")
    print(df_ranking[['Aeropuerto', 'Rank PageRank', 'PageRank Score', 'Rank Tráfico Bruto', 'Tráfico Bruto']].to_string(index=False, formatters={'PageRank Score': '{:.4f}'.format}))
    print("================================================================")

if __name__ == "__main__":
    workshop3_task3()
