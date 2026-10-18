import hashlib
import random
import pandas as pd

class BosquejoAMS:
    def __init__(self, r):
        self.r = r  # Número de instancias (pesos independientes)
        # Inicializamos las tablas contadoras y funciones hash aleatorias para cada instancia
        self.tablas = [[0] * 256 for _ in range(r)]
        self.semillas = [random.randint(1, 10000) for _ in range(r)]

    def _hash(self, item, salt):
        # Hash para mapear el elemento a una posición en la tabla de tamaño 256 (-1 o +1)
        h = int(hashlib.md5(f"{item}_{salt}".encode('utf-8')).hexdigest(), 16)
        # Retorna el índice (0 a 255) y el signo (+1 o -1)
        indice = h % 256
        signo = 1 if (h & 1) == 0 else -1
        return indice, signo

    def add(self, item):
        for i in range(self.r):
            indice, signo = self._hash(item, self.semillas[i])
            self.tablas[i][indice] += signo

    def estimate_f2(self):
        # Estima F2 tomando la mediana de las estimaciones de cada instancia r
        estimaciones = []
        for i in range(self.r):
            # F2 estimado por cada tabla es la suma de los cuadrados de sus contadores
            est = sum(valor ** 2 for valor in self.tablas[i])
            estimaciones.append(est)

        # Ordenar para obtener la mediana
        estimaciones.sort()
        medio = self.r // 2
        if self.r % 2 == 0:
            return (estimaciones[medio - 1] + estimaciones[medio]) / 2
        else:
            return estimaciones[medio]

def workshop2_task5():
    print("================================================================")
    print("=== TASK 5: FREQUENCY MOMENTS (AMS Sketch & F2 Estimation)   ===")
    print("================================================================")
    print("[INFO] Cargando 'baggage_stream_dataset.json'...")

    try:
        df = pd.read_json('baggage_stream_dataset.json')
    except FileNotFoundError:
        print("⚠️ ERROR: No se encontró 'baggage_stream_dataset.json' en la carpeta.")
        return

    flujo_vuelos = df['flight_no'].tolist()

    # Calcular el F2 real (suma de los cuadrados de las frecuencias de cada vuelo)
    frecuencias = df['flight_no'].value_counts()
    f2_real = sum(f ** 2 for f in frecuencias)
    print(f"[INFO] F2 real (Exact Second Frequency Moment): {f2_real}")

    # Probar con distintas instancias r = 5, 10, 20
    valores_r = [5, 10, 20]
    print("\n[Parte A] Evaluando AMS Sketch con r = 5, 10, 20 instancias...")

    for r in valores_r:
        bosquejo = BosquejoAMS(r)
        for vuelo in flujo_vuelos:
            bosquejo.add(vuelo)

        f2_estimado = bosquejo.estimate_f2()
        error_pct = abs(f2_estimado - f2_real) / f2_real * 100
        print(f"  * r = {r:2d} | F2 Estimado: {f2_estimado:10.1f} | Error Relativo: {error_pct:6.2f}%")

    # -------------------------------------------------------------
    # SIMULACIÓN: Vuelo retrasado causando una acumulación (backlog) de escaneos
    # -------------------------------------------------------------
    print("\n[Parte B] Simulando retraso de vuelo (backlog de escaneos)...")
    vuelo_retrasado = frecuencias.idxmax()  # Seleccionamos el vuelo con más tráfico para simular el retraso
    multiplicador_acumulacion = 3  # Triplicamos sus escaneos repentinamente

    print(f"  * Vuelo afectado por retraso crítico: {vuelo_retrasado}")
    print(f"  * Inyectando backlog de escaneos (+{multiplicador_acumulacion}x tráfico)...")

    flujo_acumulado = flujo_vuelos + ([vuelo_retrasado] * (int(frecuencias[vuelo_retrasado]) * (multiplicador_acumulacion - 1)))

    # Recalcular F2 real con la acumulación
    nuevas_frecuencias = pd.Series(flujo_acumulado).value_counts()
    nuevo_f2_real = sum(f ** 2 for f in nuevas_frecuencias)

    # Evaluar con AMS Sketch (usando r = 20)
    bosquejo_retraso = BosquejoAMS(r=20)
    for vuelo in flujo_acumulado:
        bosquejo_retraso.add(vuelo)

    nuevo_f2_estimado = bosquejo_retraso.estimate_f2()
    nuevo_error_pct = abs(nuevo_f2_estimado - nuevo_f2_real) / nuevo_f2_real * 100

    print(f"  * Nuevo F2 real (con retraso):     {nuevo_f2_real}")
    print(f"  * Nuevo F2 estimado (AMS Sketch):  {nuevo_f2_estimado:.1f}")
    print(f"  * Error Relativo post-retraso:     {nuevo_error_pct:.2f}%")
    print("================================================================")

if __name__ == "__main__":
    workshop2_task5()
