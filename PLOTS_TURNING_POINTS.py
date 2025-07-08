import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

# Cargar JSON
input_file = "secuencias_maximas.json"

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Definir rangos y colores para cada momento
moment_ranges = {
    "oportunity": (0.0, 0.25),
    "change of plans": (0.25, 0.4),
    "point of no return": (0.4, 0.6),
    "major setback": (0.6, 0.8),
    "climax Final": (0.8, 1.0),
}

colors = {
    "oportunity": "#a6cee3",
    "change of plans": "#1f78b4",
    "point of no return": "#b2df8a",
    "major setback": "#33a02c",
    "climax Final": "#fb9a99",
}

output_dir = Path("plots_turning_points")
output_dir.mkdir(exist_ok=True)

for key, moments in data.items():
    plt.figure(figsize=(8, 4))  # Formato más cuadrado
    ax = plt.gca()

    # Dibujar rangos de fondo
    for moment, (start, end) in moment_ranges.items():
        ax.add_patch(
            patches.Rectangle(
                (start, 0),
                end - start,
                1,
                color=colors[moment],
                alpha=0.3,
                label=moment if moment not in ax.get_legend_handles_labels()[1] else None
            )
        )

    # Añadir los puntos de los momentos detectados
    for m in moments:
        pos = m["position"]
        moment = m["moment"]

        ax.plot(
            pos, 0.5, "o",
            color=colors.get(moment, "black"),
            markersize=10,
            markeredgecolor="black",  # Borde negro
            markeredgewidth=1.0       # Grosor del borde
        )

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xlabel("Posición relativa en el guion", fontsize=10)
    ax.set_title(f"Estructura narrativa: {key}", fontsize=12)
    ax.legend(loc="upper right", bbox_to_anchor=(1.15, 1), fontsize=8)

    plt.tight_layout()
    plt.savefig(output_dir / f"{key}.png", dpi=150)
    plt.close()

print(f"Se han generado las gráficas en la carpeta '{output_dir.resolve()}'")
