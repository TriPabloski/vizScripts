from transformers import pipeline
from pathlib import Path
import json
from tqdm import tqdm

# ----------------------
# 1. Función para leer un guion anotado por escenas
# ----------------------

def load_annotated_scenes(path):
    scenes = []
    current_scene = {"scene_heading": "", "blocks": []}

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("scene_heading:"):
                if current_scene["scene_heading"]:
                    scenes.append(current_scene)
                current_scene = {
                    "scene_heading": line.replace("scene_heading:", "").strip(),
                    "blocks": []
                }
            elif line.startswith(("text:", "dialog:")):
                content = line.split(":", 1)[-1].strip()
                if content:
                    current_scene["blocks"].append(content)

    if current_scene["scene_heading"]:
        scenes.append(current_scene)

    return scenes

# ----------------------
# 2. Inicializar el clasificador
# ----------------------

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Etiquetas para fases del Viaje del Héroe
hero_journey_labels = [
    "ordinary world", "call to adventure", "refusal of the call", "meeting with the mentor",
    "crossing the first threshold", "tests, allies, enemies", "approach to the inmost cave",
    "ordeal", "reward", "the road back", "resurrection", "return with the elixir"
]

# ----------------------
# 3. Procesar todos los guiones de la carpeta
# ----------------------

guiones_dir = Path("./guiones")
output_dir = Path("./hero_journey_jsons")
output_dir.mkdir(exist_ok=True)

script_paths = list(guiones_dir.glob("*.txt"))
print(f"📄 Guiones encontrados: {len(script_paths)}")

for script_path in script_paths:
    print(f"\n📘 Procesando: {script_path.name}")

    scenes = load_annotated_scenes(script_path)
    print(f"   Escenas cargadas: {len(scenes)}")

    hero_journey_results = []

    for idx, scene in enumerate(tqdm(scenes, desc=f"   Clasificando escenas")):
        scene_text = " ".join(scene["blocks"])

        if not scene_text.strip():
            continue  # Saltar escenas vacías

        # Clasificación Viaje del Héroe
        hj_result = classifier(scene_text, hero_journey_labels, hypothesis_template="This scene represents the phase '{}'.")
        hj_top_label = hj_result["labels"][0]
        hj_top_score = hj_result["scores"][0]

        if hj_top_score >= 0.3:
            hero_journey_results.append({
                "scene_index": idx,
                "scene_heading": scene["scene_heading"],
                "phase": hj_top_label,
                "score": hj_top_score,
                "position": idx / len(scenes),
            })

    print(f"   ✅ Fases del Viaje del Héroe detectadas: {len(hero_journey_results)}")

    # Guardar resultados Viaje del Héroe
    hj_output_filename = f"hero_journey_{script_path.stem}.json"
    hj_output_path = output_dir / hj_output_filename

    with open(hj_output_path, "w", encoding="utf-8") as f:
        json.dump(hero_journey_results, f, ensure_ascii=False, indent=2)

    print(f"   💾 Archivo guardado: {hj_output_path}")
