import math
import random
import pandas as pd

class FiltroBloom:
    def __init__(self, capacity, error_rate):
        self.capacidad = capacity
        self.tasa_error = error_rate
        # Cálculo óptimo del tamaño del arreglo de bits (m) y número de funciones hash (k)
        self.num_bits = int(-capacity * math.log(error_rate) / (math.log(2) ** 2))
        self.num_hashes = int((self.num_bits / capacity) * math.log(2))
        self.arreglo_bits = [0] * self.num_bits

    def _hashes(self, item):
        # Generar múltiples índices hash usando distintas semillas/variaciones
        for i in range(self.num_hashes):
            valor = abs(hash(str(item) + str(i))) % self.num_bits
            yield valor

    def add(self, item):
        for indice_bit in self._hashes(item):
            self.arreglo_bits[indice_bit] = 1

    def __contains__(self, item):
        for indice_bit in self._hashes(item):
            if self.arreglo_bits[indice_bit] == 0:
                return False
        return True

def workshop2_task2():
    print("================================================================")
    print("=== TASK 2: BLOOM FILTER (Duplicate Scan Detection)          ===")
    print("================================================================")
    print("[INFO] Cargando 'baggage_stream_dataset.json'...")

    try:
        df = pd.read_json('baggage_stream_dataset.json')
    except FileNotFoundError:
        print("⚠️ ERROR: No se encontró 'baggage_stream_dataset.json' en la carpeta.")
        return

    ids_maletas = df['bag_id'].tolist()
    total_maletas = len(ids_maletas)
    print(f"[INFO] Total de maletas en el stream: {total_maletas}")

    # Configuración del Bloom Filter
    capacidad_objetivo = total_maletas
    tasa_error_objetivo = 0.05  # 5% de error teórico objetivo

    filtro = FiltroBloom(capacity=capacidad_objetivo, error_rate=tasa_error_objetivo)
    print(f"[INFO] Filtro inicializado -> Tamaño de bits (m): {filtro.num_bits}, Funciones Hash (k): {filtro.num_hashes}")

    # 1. Simular escaneo inicial (llenando el filtro con la primera mitad de los elementos)
    indice_corte = total_maletas // 2
    maletas_escaneadas = ids_maletas[:indice_corte]
    maletas_no_vistas = ids_maletas[indice_corte:]

    print(f"\n[Parte A] Insertando {len(maletas_escaneadas)} maletas escaneadas previamente...")
    for id_maleta in maletas_escaneadas:
        filtro.add(id_maleta)

    # 2. Medir falsos positivos con elementos que NUNCA fueron escaneados
    print("[Parte B] Evaluando tasa de falsos positivos con elementos no escaneados...")
    falsos_positivos = 0
    muestra_prueba = random.sample(maletas_no_vistas, min(2000, len(maletas_no_vistas)))

    for id_maleta in muestra_prueba:
        if id_maleta in filtro:
            falsos_positivos += 1

    tasa_fp_empirica = (falsos_positivos / len(muestra_prueba)) * 100
    tasa_fp_teorica = tasa_error_objetivo * 100

    print(f"  * Muestras evaluadas (no vistas): {len(muestra_prueba)}")
    print(f"  * Falsos positivos detectados:   {falsos_positivos}")
    print(f"  * Tasa de Falso Positivo Empírica:   {tasa_fp_empirica:.2f}%")
    print(f"  * Tasa de Falso Positivo Teórica:    {tasa_fp_teorica:.2f}%")
    print("================================================================")

if __name__ == "__main__":
    workshop2_task2()
