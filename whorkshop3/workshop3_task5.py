import pandas as pd
import random

def workshop3_task5():
    print("================================================================")
    print("=== TASK 5: RANDOMIZED 2-SAT (Papadimitriou Routing Policies)  ===")
    print("================================================================")
    print("[INFO] Cargando 'baggage_graph_dataset.json'...")

    try:
        df_aristas = pd.read_json('baggage_graph_dataset.json')
    except FileNotFoundError:
        print("⚠️ ERROR: No se encontró 'baggage_graph_dataset.json' en la carpeta.")
        return

    aeropuertos = sorted(list(set(df_aristas['from_airport']).union(set(df_aristas['to_airport']))))
    n_variables = len(aeropuertos)
    print(f"[INFO] Número de variables (aeropuertos): {n_variables}")

    riesgo_perdida = df_aristas.groupby('from_airport')['lost_frac'].mean().to_dict()
    for apt in aeropuertos:
        if apt not in riesgo_perdida:
            riesgo_perdida[apt] = 0.0

    umbral = 0.015
    aeropuertos_alto_riesgo = [apt for apt, riesgo in riesgo_perdida.items() if riesgo > umbral]
    print(f"[INFO] Aeropuertos con alto riesgo de pérdida (> {umbral*100}%): {aeropuertos_alto_riesgo}")

    print("\n[Parte A] Generando restricciones lógicas de enrutamiento (Papadimitriou)...")
    clausulas = []
    for i, apt in enumerate(aeropuertos[:5]):
        var1 = i
        var2 = (i + 2) % n_variables
        clausulas.append((var1, var2))
        print(f"  * Cláusula {i+1}: Si ({apt}) tiene riesgo, activar protocolo en ({aeropuertos[var2]}) [Variables: x{var1} v x{var2}]")

    print("\n[Parte B] Ejecutando búsqueda local aleatorizada (Papadimitriou)...")

    def evaluate_clause(clause, assignment):
        literal1, literal2 = clause
        valor1 = assignment[abs(literal1)]
        valor2 = assignment[abs(literal2)]
        return valor1 or valor2

    max_intentos = 100
    max_cambios = 2 * (n_variables ** 2)
    resuelto = False
    asignacion = {}

    for intento in range(max_intentos):
        asignacion = {i: random.choice([True, False]) for i in range(n_variables)}

        for paso in range(max_cambios):
            insatisfechas = [c for c in clausulas if not evaluate_clause(c, asignacion)]
            if not insatisfechas:
                resuelto = True
                break
            clausula = random.choice(insatisfechas)
            variable_a_cambiar = random.choice(clausula)
            asignacion[abs(variable_a_cambiar)] = not asignacion[abs(variable_a_cambiar)]

        if resuelto:
            break

    print(f"\n[Resultados Task 5]")
    if resuelto:
        print("  * Estado: ¡Solución 2-SAT encontrada con éxito! ✅")
        print("  * Políticas de enrutamiento asignadas:")
        for indice, valor in asignacion.items():
            politica = "ACTIVADA (Mitigación)" if valor else "ESTÁNDAR"
            print(f"    - {aeropuertos[indice]}: {politica}")
    else:
        print("  * Estado: No se encontró solución exacta en los intentos máximos. ⚠️")
    print("================================================================")

if __name__ == "__main__":
    workshop3_task5()
