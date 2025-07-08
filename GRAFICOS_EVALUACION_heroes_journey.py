import matplotlib.pyplot as plt
import numpy as np

# Nuevos datos proporcionados
raw_results = [
    {
        "threshold_0.5": {
            "score_stats": {
                "min": 0.5118584632873535,
                "max": 0.6853365898132324,
                "mean": 0.5922976583242416,
                "median": 0.5859977900981903
            },
            "diversity": 3,
            "coherence": 0.6666666666666666
        }
    },
    {
        "threshold_0.5": {
            "score_stats": {
                "min": 0.5059016942977905,
                "max": 0.5496719479560852,
                "mean": 0.5345868666966757,
                "median": 0.5481869578361511
            },
            "diversity": 2,
            "coherence": 0.5
        }
    },
    {
        "threshold_0.5": {
            "score_stats": {
                "min": 0.5199735760688782,
                "max": 0.7424778342247009,
                "mean": 0.5749474763870239,
                "median": 0.552827775478363
            },
            "diversity": 5,
            "coherence": 0.5555555555555556
        }
    },
    {
        "threshold_0.5": {
            "score_stats": {
                "min": 0.5316250324249268,
                "max": 0.6220924258232117,
                "mean": 0.5768587291240692,
                "median": 0.5768587291240692
            },
            "diversity": 2,
            "coherence": 1.0
        }
    }
]

# Etiquetas para cada película (o conjunto analizado)
names = ["12 Years a Slave", "Toy Story", "Twilight Zone", "Unbroken"]

# Extraemos las métricas para cada película
score_min = [r["threshold_0.5"]["score_stats"]["min"] for r in raw_results]
score_max = [r["threshold_0.5"]["score_stats"]["max"] for r in raw_results]
score_mean = [r["threshold_0.5"]["score_stats"]["mean"] for r in raw_results]
score_median = [r["threshold_0.5"]["score_stats"]["median"] for r in raw_results]
diversity = [r["threshold_0.5"]["diversity"] for r in raw_results]
coherence = [r["threshold_0.5"]["coherence"] for r in raw_results]

x = np.arange(len(names))

plt.figure(figsize=(14, 8))

# Gráfico estadísticas de score
plt.subplot(1, 3, 1)
plt.plot(x, score_min, label="Mínimo", marker="o")
plt.plot(x, score_max, label="Máximo", marker="o")
plt.plot(x, score_mean, label="Media", marker="o")
plt.plot(x, score_median, label="Mediana", marker="o")
plt.xticks(x, names, rotation=45, ha="right")
plt.title("Estadísticas de la puntuación")
plt.ylabel("Score")
plt.ylim(0.4, 0.8)
plt.legend()
plt.grid(True)

# Gráfico de diversidad
plt.subplot(1, 3, 2)
plt.bar(x, diversity, color="tab:green")
plt.xticks(x, names, rotation=45, ha="right")
plt.title("Diversidad de etiquetas")
plt.ylabel("Número de etiquetas únicas")
plt.grid(axis="y")

# Gráfico de coherencia
plt.subplot(1, 3, 3)
plt.bar(x, coherence, color="tab:orange")
plt.xticks(x, names, rotation=45, ha="right")
plt.title("Coherencia narrativa temporal")
plt.ylabel("Porcentaje")
plt.ylim(0, 1.05)
plt.grid(axis="y")

plt.tight_layout()
plt.show()
