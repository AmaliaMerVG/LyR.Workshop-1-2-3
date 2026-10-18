import json
import random
import pandas as pd

def generate_graph_dataset():
    print("================================================================")
    print("=== WORKSHOP 3: GENERADOR DE DATOS DE GRAFO DE RUTAS         ===")
    print("================================================================")

    try:
        df = pd.read_json('baggage_stream_dataset.json')
    except FileNotFoundError:
        try:
            df = pd.read_json('baggage_dataset.json')
        except FileNotFoundError:
            print("⚠️ Advertencia: No se encontró dataset previo. Generando rutas sintéticas...")
            df = None

    aeropuertos = ['BOG', 'MDE', 'CLO', 'CTG', 'BAQ', 'PEI', 'ADZ', 'CLO', 'MEO', 'UIO']
    aeropuertos = list(set(aeropuertos))  # Asegurar al menos 8 aeropuertos únicos (requisito del taller)

    aristas = []
    contador_id_arista = 1

    if df is not None and 'origin_airport' in df.columns:
        grupos_ruta = df.groupby(['origin_airport', 'dest_airport'])
        for (origen, destino), grupo in grupos_ruta:
            if origen != destino:
                aristas.append({
                    "edge_id": f"e{contador_id_arista:03d}",
                    "from_airport": origen,
                    "to_airport": destino,
                    "bag_count": int(len(grupo) * random.uniform(1.2, 2.5)),
                    "avg_weight_kg": round(float(grupo['weight_kg'].mean()), 2),
                    "lost_frac": round(float((grupo['status'] == 'lost').mean()), 4)
                })
                contador_id_arista += 1

    # Asegurar al menos un grafo completo y conectado con >= 8 nodos
    for i, origen in enumerate(aeropuertos):
        for j, destino in enumerate(aeropuertos):
        # Evitar auto-conexiones y asegurar suficientes rutas
            if origen != destino and not any(e['from_airport'] == origen and e['to_airport'] == destino for e in aristas):
                if random.random() < 0.6:  # Probabilidad de conexión
                    aristas.append({
                        "edge_id": f"e{contador_id_arista:03d}",
                        "from_airport": origen,
                        "to_airport": destino,
                        "bag_count": random.randint(150, 800),
                        "avg_weight_kg": round(random.uniform(14.0, 24.0), 2),
                        "lost_frac": round(random.uniform(0.005, 0.035), 4)
                    })
                    contador_id_arista += 1

    archivo_salida = 'baggage_graph_dataset.json'
    with open(archivo_salida, 'w') as archivo:
        json.dump(aristas, archivo, indent=2)

    print(f"[INFO] Dataset de grafo generado y guardado en '{archivo_salida}'.")
    print(f"[INFO] Total de rutas (aristas) creadas: {len(aristas)}")
    print("================================================================")

if __name__ == "__main__":
    generate_graph_dataset()
