import random
import pandas as pd

print("Generando dataset limpio...")
random.seed(42)

n_registros = 10000
aeropuertos = ["BOG", "MDE", "CTG", "CLO", "BAQ", "MIA", "JFK", "LAX", "ATL", "MAD"]
aerolineas = ["AV", "LA", "CM", "AA", "DL", "IB"]
estados = ["checked_in", "loaded", "transferred", "delivered", "lost"]

datos = []
for i in range(1, n_registros + 1):
    datos.append({
        "bag_id": f"BAG-{i:07d}",
        "timestamp": "2026-10-18 08:00:00",
        "flight_no": f"{random.choice(aerolineas)}{random.randint(100, 999)}",
        "origin_airport": random.choice(aeropuertos),
        "dest_airport": random.choice(aeropuertos),
        "weight_kg": round(random.uniform(5.0, 32.0), 2),
        "status": random.choice(estados),
        "is_priority": random.random() < 0.15
    })

df = pd.DataFrame(datos)
df.to_csv("baggage_dataset.csv", index=False, encoding='utf-8')
print("¡Dataset 'baggage_dataset.csv' regenerado con éxito y listo para usar!")