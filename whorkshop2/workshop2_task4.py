import math
import hashlib
import random
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class HyperLogLogSimple:
    def __init__(self, m):
        self.m = m  # Número de registros (debe ser potencia de 2)
        self.registros = [0] * m

    def _hash(self, item):
        # Hash criptográfico para obtener una distribución uniforme de 32 bits
        return int(hashlib.md5(str(item).encode('utf-8')).hexdigest(), 16) & 0xFFFFFFFF

    def _rho(self, val):
        # Cuenta los ceros a la izquierda + 1 usando la función bin() nativa de Python
        if val == 0:
            return 32
        cadena_binaria = bin(val)[2:].zfill(32)
        return min(32, cadena_binaria.find('1') + 1)

    def add(self, item):
        h = self._hash(item)
        indice = h & (self.m - 1)  # Primeros log2(m) bits para el índice del registro
        w = h >> int(math.log2(self.m))  # Resto del hash para contar ceros
        self.registros[indice] = max(self.registros[indice], self._rho(w))

    def estimate(self):
        # Constante de corrección de HyperLogLog (para m pequeños usamos aproximación estándar)
        alfa = 0.7213 / (1 + 1.079 / self.m)
        estimacion_cruda = alfa * (self.m ** 2) * sum(2.0 ** (-r) for r in self.registros) ** (-1)
        return int(estimacion_cruda)

def workshop2_task4():
    print("================================================================")
    print("=== TASK 4: HYPERLOGLOG (Distinct Count Estimation)          ===")
    print("================================================================")
    print("[INFO] Cargando 'baggage_stream_dataset.json'...")

    try:
        df = pd.read_json('baggage_stream_dataset.json')
    except FileNotFoundError:
        print("⚠️ ERROR: No se encontró 'baggage_stream_dataset.json' en la carpeta.")
        return

    # Convertir timestamp y extraer la hora como periodo de análisis
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['franja_hora'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:00')

    # Seleccionar una hora aleatoria de la lista de horas disponibles
    todas_las_horas = df['franja_hora'].unique()
    hora_muestra = random.choice(todas_las_horas)

    df_hora = df[df['franja_hora'] == hora_muestra]
    conteo_distintos_real = df_hora['bag_id'].nunique()

    print(f"[INFO] Hora seleccionada aleatoriamente: {hora_muestra}")
    print(f"[INFO] Conteo exacto (True Distinct Count) de bag_ids en esa hora: {conteo_distintos_real}")

    # Probar diferentes tamaños de registros m = 16, 32, 64, 128
    valores_m = [16, 32, 64, 128]
    resultados = []

    print("\n[Parte A] Evaluando HyperLogLog con diferentes valores de m...")
    for m in valores_m:
        hll = HyperLogLogSimple(m)
        for id_maleta in df_hora['bag_id']:
            hll.add(id_maleta)

        estimacion = hll.estimate()
        error_pct = abs(estimacion - conteo_distintos_real) / conteo_distintos_real * 100
        memoria_bytes = m * 4  # Asumiendo enteros de 4 bytes por registro

        resultados.append({
            'm': m,
            'Estimado': estimacion,
            'Error (%)': error_pct,
            'Memoria (Bytes)': memoria_bytes
        })
        print(f"  * m = {m:3d} | Estimado: {estimacion:5d} | Error: {error_pct:6.2f}% | Memoria: {memoria_bytes} bytes")

    # -------------------------------------------------------------
    # Gráfica: Error vs Memoria
    # -------------------------------------------------------------
    df_resultados = pd.DataFrame(resultados)
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(8, 5))
    sns.lineplot(data=df_resultados, x='Memoria (Bytes)', y='Error (%)', marker='o', color='b', linewidth=2)
    plt.title(f"HyperLogLog: Error vs Memoria (Hora: {hora_muestra})")
    plt.xlabel("Memoria Utilizada (Bytes)")
    plt.ylabel("Error Relativo (%)")
    plt.tight_layout()

    imagen_salida = "workshop2_hll_error_vs_memory.png"
    plt.savefig(imagen_salida, dpi=300)
    print(f"\n[INFO] Gráfica de error vs memoria guardada como '{imagen_salida}'.")
    plt.show()
    print("================================================================")

if __name__ == "__main__":
    workshop2_task4()
