import json
from pathlib import Path
import numpy as np

def analyze_scores(data, threshold):
    """
    data: lista de dicts con 'moment', 'score' y 'position'
    threshold: umbral para considerar asignación válida
    """
    if not data:
        return {
            "coverage": 0.0,
            "score_stats": None,
            "diversity": 0,
            "coherence": None
        }

    scores = [item["score"] for item in data]
    moments = [item["moment"] for item in data]

    coverage = sum(s >= threshold for s in scores) / len(scores)

    score_stats = {
        "min": float(np.min(scores)),
        "max": float(np.max(scores)),
        "mean": float(np.mean(scores)),
        "median": float(np.median(scores))
    }

    diversity = len(set(moments))

    return {
        "coverage": coverage,
        "score_stats": score_stats,
        "diversity": diversity,
        "coherence": None  # se calcula después
    }

def coherence_score(assigned_labels, expected_order):
    """
    assigned_labels: lista de etiquetas ('moment') en orden de aparición
    expected_order: lista ordenada de etiquetas esperadas

    Devuelve porcentaje de pares consecutivos que respetan el orden esperado.
    """
    index_map = {label: i for i, label in enumerate(expected_order)}

    valid_pairs = 0
    total_pairs = 0

    filtered_labels = [lbl for lbl in assigned_labels if lbl in index_map]

    for i in range(len(filtered_labels) - 1):
        total_pairs += 1
        current = filtered_labels[i]
        nxt = filtered_labels[i+1]

        if index_map[current] <= index_map[nxt]:
            valid_pairs += 1

    if total_pairs == 0:
        return None

    return valid_pairs / total_pairs

def analyze_file(path, thresholds=[0.5]):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    expected_order = ["oportunity", "change of plans", "point of no return", "major setback", "climax final"]

    result = {}
    for threshold in thresholds:
        filtered = [item for item in data if item["score"] >= threshold]

        metrics = analyze_scores(filtered, threshold)

        filtered_sorted = sorted(filtered, key=lambda x: x["position"])
        assigned_moments = [item["moment"] for item in filtered_sorted]
        coherence = coherence_score(assigned_moments, expected_order)
        metrics["coherence"] = coherence

        result[f"threshold_{threshold}"] = metrics

    return result

if __name__ == "__main__":
    input_dir = Path("./turning_points_jsons")
    output_dir = Path("./zero_shot_analysis")
    output_dir.mkdir(exist_ok=True)

    for file_path in input_dir.glob("turning_points_*.json"):
        print(f"Analizando {file_path.name} ...")
        analysis = analyze_file(file_path)
        output_path = output_dir / f"{file_path.stem}_metrics.json"
        with open(output_path, "w", encoding="utf-8") as f_out:
            json.dump(analysis, f_out, ensure_ascii=False, indent=2)
        print(f"  → Guardado análisis en {output_path}")
