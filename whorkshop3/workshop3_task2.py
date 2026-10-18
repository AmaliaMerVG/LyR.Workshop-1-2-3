import pandas as pd
import numpy as np

def workshop3_task2():
    print("================================================================")
    print("=== TASK 2: STATIONARY DISTRIBUTION (Long-run Airport Share) ===")
    print("================================================================")
    print("[INFO] Cargando 'baggage_graph_dataset.json'...")

    try:
        df_aristas = pd.read_json('baggage_graph_dataset.json')
    except FileNotFoundError:
        print("⚠️ ERROR: No se encontró 'baggage_graph_dataset.json' en la carpeta.")
        return

    # 1. Reconstruir la matriz de transición de probabilidad P
    aeropuertos = sorted(list(set(df_aristas['from_airport']).union(set(df_aristas['to_airport']))))
    df_matriz = pd.DataFrame(0.0, index=aeropuertos, columns=aeropuertos)

    for _, fila in df_aristas.iterrows():
        df_matriz.loc[fila['from_airport'], fila['to_airport']] += fila['bag_count']

    sumas_filas = df_matriz.sum(axis=1)
    for aeropuerto in aeropuertos:
        if sumas_filas[aeropuerto] == 0:
            df_matriz.loc[aeropuerto, aeropuerto] = 1.0
            sumas_filas[aeropuerto] = 1.0

    P = df_matriz.div(sumas_filas, axis=0).values
    n = len(aeropuertos)

    # 2. Calcular la Distribución Estacionaria (\pi) resolviendo pi * P = pi  (o mediante autovectores)
    print("\n[Parte A] Calculando la distribución estacionaria (\pi)...")

    # Transponemos P para resolver (P^T - I) * pi^T = 0 con autovalores (autovalor 1)
    autovalores, autovectores = np.linalg.eig(P.T)

    # Encontrar el autovector correspondiente al autovalor más cercano a 1.0
    indice = np.argmin(np.abs(autovalores - 1.0))
    pi = np.real(autovectores[:, indice])

    # Normalizar para que la suma de probabilidades sea 1.0
    pi = pi / np.sum(pi)

    # 3. Comparación con el tráfico bruto (conteo bruto de maletas)
    trafico_bruto_origen = df_matriz.sum(axis=1)
    trafico_bruto_destino = df_matriz.sum(axis=0)
    trafico_bruto_total = trafico_bruto_origen + trafico_bruto_destino
    participacion_bruta = trafico_bruto_total / trafico_bruto_total.sum()

    df_comparacion = pd.DataFrame({
        'Aeropuerto': aeropuertos,
        'Estacionaria (\pi)': pi,
        'Tráfico Bruto (Share)': participacion_bruta.values
    }).sort_values(by='Estacionaria (\pi)', ascending=False)

    print("\n[Parte B] Comparación: Distribución Estacionaria vs Tráfico Bruto:")
    print(df_comparacion.to_string(index=False, formatters={'Estacionaria (\pi)': '{:.4f}'.format, 'Tráfico Bruto (Share)': '{:.4f}'.format}))
    print("================================================================")

if __name__ == "__main__":
    workshop3_task2()
