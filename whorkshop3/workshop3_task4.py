import pandas as pd
import numpy as np
import random

def workshop3_task4():
    print("================================================================")
    print("=== TASK 4: UNDIRECTED RANDOM WALK (Empirical vs Theoretical) ===")
    print("================================================================")
    print("[INFO] Cargando 'baggage_graph_dataset.json'...")

    try:
        df_aristas = pd.read_json('baggage_graph_dataset.json')
    except FileNotFoundError:
        print("⚠️ ERROR: No se encontró 'baggage_graph_dataset.json' en la carpeta.")
        return

    # 1. Construir el grafo y simetrizarlo para una caminata aleatoria no dirigida
    aeropuertos = sorted(list(set(df_aristas['from_airport']).union(set(df_aristas['to_airport']))))
    n = len(aeropuertos)
    df_matriz = pd.DataFrame(0.0, index=aeropuertos, columns=aeropuertos)

    for _, fila in df_aristas.iterrows():
        # Sumamos flujos en ambas direcciones para simetrizar el grafo
        df_matriz.loc[fila['from_airport'], fila['to_airport']] += fila['bag_count']
        df_matriz.loc[fila['to_airport'], fila['from_airport']] += fila['bag_count']

    # 2. Calcular la Distribución Teórica Estacionaria (\pi) para el grafo no dirigido
    sumas_filas = df_matriz.sum(axis=1)
    P = df_matriz.div(sumas_filas, axis=0).values

    autovalores, autovectores = np.linalg.eig(P.T)
    indice = np.argmin(np.abs(autovalores - 1.0))
    pi_teorica = np.real(autovectores[:, indice])
    pi_teorica = pi_teorica / np.sum(pi_teorica)

    # 3. Simulación de Caminata Aleatoria (Random Walk) de >= 50,000 pasos
    num_pasos = 50000
    print(f"\n[Parte A] Ejecutando Random Walk No Dirigido por {num_pasos:,} pasos...")

    nodo_actual = random.choice(aeropuertos)
    conteo_visitas = {aeropuerto: 0 for aeropuerto in aeropuertos}

    for _ in range(num_pasos):
        conteo_visitas[nodo_actual] += 1
        # Obtener vecinos y probabilidades de transición desde el nodo actual
        vecinos = df_matriz.columns.tolist()
        pesos_vecinos = df_matriz.loc[nodo_actual].values
        peso_total = pesos_vecinos.sum()

        if peso_total > 0:
            probabilidades = pesos_vecinos / peso_total
            nodo_actual = np.random.choice(vecinos, p=probabilidades)
        else:
            nodo_actual = random.choice(aeropuertos)

    print(f"  -> ¡Caminata aleatoria de {num_pasos:,} pasos finalizada con éxito!")

    # Calcular distribución empírica
    pi_empirica = np.array([conteo_visitas[aeropuerto] for aeropuerto in aeropuertos]) / num_pasos

    # 4. Comparación Empírica vs Teórica
    df_comparacion = pd.DataFrame({
        'Aeropuerto': aeropuertos,
        'Empírica (Simulada)': pi_empirica,
        'Teórica (Exacta)': pi_teorica
    })

    df_comparacion['Diferencia Absoluta'] = np.abs(df_comparacion['Empírica (Simulada)'] - df_comparacion['Teórica (Exacta)'])
    df_comparacion = df_comparacion.sort_values(by='Teórica (Exacta)', ascending=False)

    print("\n[Parte B] Comparación (Random Walk Empírico vs Teórico):")
    print(df_comparacion.to_string(index=False, formatters={
        'Empírica (Simulada)': '{:.4f}'.format,
        'Teórica (Exacta)': '{:.4f}'.format,
        'Diferencia Absoluta': '{:.4f}'.format
    }))
    print("================================================================")

if __name__ == "__main__":
    workshop3_task4()
