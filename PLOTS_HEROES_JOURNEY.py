import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

# Cargar JSON
input_file = "secuencias_maximas_hero_journey.json"

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Fases del viaje del héroe
hero_journey_phases = [
    "ordinary world",
    "call to adventure",
    "refusal of the call",
    "meeting with the mentor",
    "crossing the first threshold",
    "tests, allies, enemies",
    "approach to the inmost cave",
    "ordeal",
    "reward",
    "the road back",
    "resurrection",
    "return with the elixir"
]

# Crear rangos equitativos
phase_length = 1.0 / len(hero_journey_phases)
phase_ranges = {
    phase: (i * phase_length, (i + 1) * phase_length)
    for i, phase in enumerate(hero_journey_phases)
}

# Colores asignados a cada fase
colors = {
    "ordinary world": "#a6cee3",
    "call to adventure": "#1f78b4",
    "refusal of the call": "#b2df8a",
    "meeting with the mentor": "#33a02c",
    "crossing the first threshold": "#fb9a99",
    "tests, allies, enemies": "#e31a1c",
    "approach to the inmost cave": "#fdbf6f",
    "ordeal": "#ff7f00",
    "reward": "#cab2d6",
    "the road back": "#6a3d9a",
    "resurrection": "#ffff99",
    "return with the elixir": "#b15928"
}

# Carpeta de salida
output_dir = Path("plots_hero_journey")
output_dir.mkdir(exist_ok=True)

# Iterar por cada película
for key, moments in data.items():
    plt.figure(figsize=(8, 6))
    ax = plt.gca()

    # Dibujar las fases como rectángulos de fondo
    for phase, (start, end) in phase_ranges.items():
        ax.add_patch(
            patches.Rectangle(
                (start, 0),
                end - start,
                1,
                color=colors.get(phase, "gray"),
                alpha=0.3,
                label=phase if phase not in ax.get_legend_handles_labels()[1] else None
            )
        )

    # Dibujar los puntos sin etiquetas, pero con borde
    for m in moments:
        pos = m["position"]
        phase = m["phase"].lower()
        color = colors.get(phase, "black")

        ax.plot(
            pos, 0.5, "o",
            color=color,
            markersize=12,
            markeredgecolor="black",
            markeredgewidth=0.5
        )

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xlabel("Posición relativa en el guion")
    ax.set_title(f"Estructura narrativa: {key}")

    # Leyenda debajo en dos columnas
    ax.legend(
        loc='upper center',
        bbox_to_anchor=(0.5, -0.25),
        ncol=2,
        fontsize=9
    )

    plt.tight_layout()
    plt.savefig(output_dir / f"{key}.png", bbox_inches='tight')
    plt.close()

print(f"✅ Gráficas generadas en: {output_dir.resolve()}")
