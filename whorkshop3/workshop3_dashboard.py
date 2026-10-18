import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def workshop3_dashboard():
    print("================================================================")
    print("=== TASK 6: GRAPH DASHBOARD (Airline Baggage - Workshop 3)   ===")
    print("================================================================")
    print("[INFO] Cargando 'baggage_graph_dataset.json'...")

    try:
        df_aristas = pd.read_json('baggage_graph_dataset.json')
    except FileNotFoundError:
        print("⚠️ ERROR: No se encontró 'baggage_graph_dataset.json' en la carpeta.")
        return

    # 1. Procesar datos del grafo para PageRank y Tráfico Bruto
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

    # PageRank con Teleportación (d = 0.85)
    d = 0.85
    pr = np.ones(n) / n
    teletransporte = np.ones((n, n)) / n
    G = d * M + (1 - d) * teletransporte

    for _ in range(100):
        pr_siguiente = pr @ G
        if np.linalg.norm(pr_siguiente - pr, ord=1) < 1e-6:
            break
        pr = pr_siguiente

    # Tráfico bruto por aeropuerto (Salidas + Llegadas)
    trafico_bruto = df_matriz.sum(axis=1) + df_matriz.sum(axis=0)

    # Identificar aeropuertos con riesgo de pérdida (> 1.5%)
    riesgo_perdida = df_aristas.groupby('from_airport')['lost_frac'].mean().to_dict()
    alto_riesgo = {apt for apt, riesgo in riesgo_perdida.items() if riesgo > 0.015}

    # Crear DataFrame para el dashboard
    df_tablero = pd.DataFrame({
        'Aeropuerto': aeropuertos,
        'PageRank': pr,
        'Tráfico Bruto': trafico_bruto.values,
        'Riesgo': ['Alto Riesgo (Lost)' if apt in alto_riesgo else 'Estándar' for apt in aeropuertos]
    })

    # Mostrar tabla resumen en la consola
    print("\n[Resumen Dashboard - PageRank vs Tráfico]")
    print(df_tablero.sort_values(by='PageRank', ascending=False).to_string(index=False, formatters={
        'PageRank': '{:.4f}'.format,
        'Tráfico Bruto': '{:,.1f}'.format
    }))

    # Configuración y generación de la gráfica visual
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 6))

    sns.scatterplot(
        data=df_tablero,
        x='Tráfico Bruto',
        y='PageRank',
        hue='Riesgo',
        palette={'Alto Riesgo (Lost)': '#d62728', 'Estándar': '#1f77b4'},
        s=130,
        edgecolor='black'
    )

    plt.title("Panel D: PageRank vs Tráfico Bruto por Aeropuerto (Riesgo Resaltado)", fontsize=13, fontweight='bold')
    plt.xlabel("Tráfico Bruto de Maletas (Entrante + Saliente)")
    plt.ylabel("Puntuación PageRank (d = 0.85)")

    # Añadir etiquetas de texto a cada punto de los aeropuertos
    for _, fila in df_tablero.iterrows():
        plt.text(fila['Tráfico Bruto'] + 15, fila['PageRank'], fila['Aeropuerto'], fontsize=9, alpha=0.85)

    plt.tight_layout()
    archivo_salida = "workshop3_dashboard.png"
    plt.savefig(archivo_salida, dpi=300)
    print(f"\n[INFO] Dashboard del Workshop 3 guardado exitosamente como '{archivo_salida}'.")
    plt.show()
    print("================================================================")

if __name__ == "__main__":
    workshop3_dashboard()
