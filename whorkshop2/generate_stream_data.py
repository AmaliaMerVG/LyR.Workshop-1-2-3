import json
import random
from datetime import datetime, timedelta

def generate_streaming_dataset():
    print("================================================================")
    print("=== WORKSHOP 2: GENERADOR DE DATOS DE STREAMING DE EQUIPAJE ===")
    print("================================================================")

    # Intentamos cargar el dataset anterior para mantener consistencia con los IDs y vuelos
    try:
        with open('baggage_dataset.json', 'r') as archivo:
            datos_base = json.load(archivo)
        print(f"[INFO] Se cargaron {len(datos_base)} registros base de 'baggage_dataset.json'.")
    except FileNotFoundError:
        print("⚠️ Advertencia: No se encontró 'baggage_dataset.json'. Se generarán datos desde cero.")
        datos_base = []

    escaneres = ["SCN-GATE-01", "SCN-GATE-02", "SCN-CHECKIN-A", "SCN-CHECKIN-B", "SCN-TRANSFER-01", "SCN-ARRIVALS"]
    datos_streaming = []

    # Si tenemos datos base, los extendemos con los campos de streaming de la Unidad 2
    if datos_base:
        for indice, maleta in enumerate(datos_base, start=1):
            maleta_streaming = maleta.copy()
            maleta_streaming['stream_seq'] = indice
            maleta_streaming['scanner_id'] = random.choice(escaneres)
            datos_streaming.append(maleta_streaming)
    else:
        # Generación sintética si no existiera el archivo previo
        aerolineas = ['LA', 'AV', 'DL', 'AA', 'IB']
        aeropuertos = ['BOG', 'MDE', 'CLO', 'CTG', 'BAQ', 'PEI', 'ADZ']
        estados = ['checked_in', 'loaded', 'transferred', 'delivered', 'lost']

        tiempo_base = datetime(2026, 10, 1, 6, 0, 0)
        for i in range(1, 10001):
            datos_streaming.append({
                "bag_id": f"BAG-{i:05d}",
                "timestamp": (tiempo_base + timedelta(minutes=random.randint(1, 10000))).strftime("%Y-%m-%d %H:%M:%S"),
                "flight_no": f"{random.choice(aerolineas)}{random.randint(100, 999)}",
                "origin_airport": random.choice(aeropuertos),
                "dest_airport": random.choice(aeropuertos),
                "weight_kg": round(random.uniform(5.0, 32.0), 2),
                "status": random.choices(estados, weights=[30, 30, 20, 15, 5])[0],
                "is_priority": random.random() < 0.15,
                "stream_seq": i,
                "scanner_id": random.choice(escaneres)
            })

    archivo_salida = 'baggage_stream_dataset.json'
    with open(archivo_salida, 'w') as archivo:
        json.dump(datos_streaming, archivo, indent=2)

    print(f"[INFO] Dataset de streaming generado y guardado exitosamente en '{archivo_salida}'.")
    print(f"[INFO] Total de registros en el stream: {len(datos_streaming)}")
    print("================================================================")

if __name__ == "__main__":
    generate_streaming_dataset()
