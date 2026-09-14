import json

cat = json.load(open("catalogo_geral_podcasts.json", encoding="utf-8"))
all_tracks = []
for section, items in cat.items():
    part_num = "Parte 1" if "Parte 1" in section else ("Parte 2" if "Parte 2" in section else "Parte 3")
    part_folder = "" if part_num == "Parte 1" else ("Parte_2/" if part_num == "Parte 2" else "Parte_3/")
    base_rel = "Podcasts_Tematicos/Thalita_e_Francisca/" + part_folder
    for item in items:
        clean_title = item["filename"].replace("Podcast_", "").replace("Parte2_", "").replace("Parte3_", "").replace(".mp3", "").replace("_", " ")
        all_tracks.append({
            "part": part_num,
            "section": section,
            "filename": item["filename"],
            "title": clean_title,
            "size_mb": item["size_mb"],
            "is_full_chapter": item["is_full_chapter"],
            "url": base_rel + item["filename"]
        })

print(f"Total faixas catalogadas para o player: {len(all_tracks)}")
