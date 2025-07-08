import os
import json

folder_path = "turning_points_jsons"

narrative_order = [
    "oportunity",
    "change of plans",
    "point of no return",
    "major setback",
    "climax Final"
]

order_index = {moment: i for i, moment in enumerate(narrative_order)}

results_by_movie = {}

for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Ordenamos por posición ascendente para facilitar el DP
        data_sorted = sorted(data, key=lambda x: x["position"])
        
        n = len(data_sorted)
        dp = [[] for _ in range(n)]  # dp[i] = mejor subsecuencia terminando en i
        
        for i in range(n):
            dp[i] = [data_sorted[i]]
            for j in range(i):
                # Comprobar orden narrativo y posición estrictamente creciente
                if (order_index[data_sorted[j]["moment"]] < order_index[data_sorted[i]["moment"]]
                    and data_sorted[j]["position"] < data_sorted[i]["position"]
                    and len(dp[j]) + 1 > len(dp[i])):
                    dp[i] = dp[j] + [data_sorted[i]]
        
        # Encontrar la subsecuencia más larga entre dp
        best_subseq = max(dp, key=len) if dp else []
        
        movie_name = os.path.splitext(filename)[0]
        results_by_movie[movie_name] = best_subseq

# Mostrar resultados
for movie, subseq in results_by_movie.items():
    print(f"Secuencia más larga para {movie}:")
    print(json.dumps(subseq, indent=2, ensure_ascii=False))
    print("\n---\n")

# Guardar resultados en JSON
with open("secuencias_maximas.json", "w", encoding="utf-8") as out_file:
    json.dump(results_by_movie, out_file, indent=2, ensure_ascii=False)

print("Archivo 'secuencias_maximas.json' creado con las secuencias máximas por película.")