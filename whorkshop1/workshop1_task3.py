import random
import time
import pandas as pd

def workshop1_task3():
    print("================================================================")
    print("=== TASK 3: UNIVERSAL HASHING & COLLISION ANALYSIS (Baggage) ===")
    print("================================================================")
    print("[INFO] Cargando 'baggage_dataset.json'...")

    try:
        df = pd.read_json('baggage_dataset.json')

    except FileNotFoundError:
        print("⚠️ ERROR: No se encontró 'baggage_dataset.json' en la carpeta.")
        return

    ids_maletas = df['bag_id'].tolist()
    total_maletas = len(ids_maletas)
    print(f"[INFO] Total de maletas cargadas para indexación: {total_maletas}")

    # Parámetros de la Tabla Hash (número primo para optimizar la dispersión)
    tamano_tabla = 1009
    print(f"[INFO] Tamaño de la tabla hash (m): {tamano_tabla}")

    # Función de Hash Universal: h(k) = ((a * k_int + b) % p) % m
    p = 2**31 - 1
    a = random.randint(1, p - 1)
    b = random.randint(0, p - 1)

    def string_to_int(s):
        """Convierte el ID alfanumérico de la maleta a entero usando el método de Horner."""
        valor = 0
        for caracter in s:
            valor = (valor * 31 + ord(caracter)) % p
        return valor

    def universal_hash(bag_id):
        k_entero = string_to_int(bag_id)
        return ((a * k_entero + b) % p) % tamano_tabla

    # Simulación de inserción y medición de colisiones
    print("\n[Parte A] Construcción de tabla hash y conteo de colisiones...")
    tabla_hash = [[] for _ in range(tamano_tabla)]
    colisiones = 0

    tiempo_inicio = time.perf_counter()
    for id_maleta in ids_maletas:
        indice = universal_hash(id_maleta)
        if len(tabla_hash[indice]) > 0:
            colisiones += 1
        tabla_hash[indice].append(id_maleta)
    tiempo_transcurrido = (time.perf_counter() - tiempo_inicio) * 1000

    # Estadísticas de distribución
    slots_ocupados = sum(1 for cubeta in tabla_hash if len(cubeta) > 0)
    tamano_max_cubeta = max(len(cubeta) for cubeta in tabla_hash)
    tasa_colision = (colisiones / total_maletas) * 100

    print(f"  * Tiempo de indexación total:       {tiempo_transcurrido:.4f} ms")
    print(f"  * Slots ocupados en la tabla:       {slots_ocupados} / {tamano_tabla}")
    print(f"  * Colisiones totales detectadas:    {colisiones}")
    print(f"  * Tasa de colisión efectiva:        {tasa_colision:.2f}%")
    print(f"  * Tamaño máximo del bucket (colisión): {tamano_max_cubeta}")
    print("================================================================")

if __name__ == "__main__":
    workshop1_task3()
