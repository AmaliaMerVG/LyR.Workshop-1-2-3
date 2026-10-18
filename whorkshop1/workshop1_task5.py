import pandas as pd

def workshop1_task5():
    print("================================================================")
    print("=== TASK 5: PROBABILITY ANALYSIS (Markov's Inequality)       ===")
    print("================================================================")
    print("[INFO] Cargando 'baggage_dataset.json'...")

    try:
        df = pd.read_json('baggage_dataset.json')
    except FileNotFoundError:
        print("⚠️ ERROR: No se encontró 'baggage_dataset.json' en la carpeta.")
        return

    total_maletas = len(df)
    total_vuelos = df['flight_no'].nunique()
    print(f"[INFO] Total de maletas: {total_maletas} | Total de vuelos únicos: {total_vuelos}")

    # 1. ANÁLISIS DE MALETAS PRIORITARIAS POR VUELO
    print("\n[Parte A] Calculando estadísticas de maletas prioritarias...")

    # Agrupar por vuelo y contar cuántas maletas prioritarias tiene cada uno
    prioritarias_por_vuelo = df.groupby('flight_no')['is_priority'].sum()
    media_prioritarias = prioritarias_por_vuelo.mean()
    max_prioritarias = prioritarias_por_vuelo.max()

    print(f"  * Promedio de maletas prioritarias por vuelo (E[X]): {media_prioritarias:.4f}")
    print(f"  * Máximo real observado en un vuelo:              {max_prioritarias}")

    # 2. APLICACIÓN DE LA DESIGUALDAD DE MARKOV
    # P(X >= a) <= E[X] / a
    # Queremos acotar la probabilidad de encontrar un vuelo con un umbral de sobrecarga (por ejemplo, a = 3 maletas prioritarias)
    print("\n[Parte B] Aplicando la Desigualdad de Markov P(X >= a) <= E[X] / a...")

    umbrales = [2, 3, 4, 5]
    for a in umbrales:
        cota_markov = media_prioritarias / a
        # Frecuencia empírica real en el dataset para comparar
        prob_empirica = (prioritarias_por_vuelo >= a).mean()

        print(f"  * Umbral (a = {a} maletas prioritarias):")
        print(f"    - Cota teórica (Markov):      {cota_markov:.4f} ({cota_markov * 100:.2f}%)")
        print(f"    - Probabilidad empírica real: {prob_empirica:.4f} ({prob_empirica * 100:.2f}%)")

    print("================================================================")

if __name__ == "__main__":
    workshop1_task5()
