import os
import sys
import json
import time
from faster_whisper import WhisperModel

def format_timestamp(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def transcribe_file(audio_path: str, output_dir: str, model: WhisperModel):
    print(f"\n=======================================================")
    print(f"Iniciando transcrição de: {audio_path}")
    print(f"Diretório de saída: {output_dir}")
    print(f"=======================================================")

    t0 = time.time()
    segments_generator, info = model.transcribe(
        audio_path,
        language="pt",
        beam_size=5,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=800)
    )

    print(f"Duração detectada do áudio: {info.duration:.1f}s ({format_timestamp(info.duration)})")
    print(f"Idioma detectado: {info.language} (probabilidade: {info.language_probability:.2f})")

    segments_data = []
    lines_with_ts = []
    paragraphs = []
    current_para = []

    count = 0
    for seg in segments_generator:
        count += 1
        text = seg.text.strip()
        if not text:
            continue
        
        start_str = format_timestamp(seg.start)
        end_str = format_timestamp(seg.end)

        seg_dict = {
            "id": count,
            "start": round(seg.start, 2),
            "end": round(seg.end, 2),
            "start_str": start_str,
            "end_str": end_str,
            "text": text
        }
        segments_data.append(seg_dict)
        lines_with_ts.append(f"[{start_str} -> {end_str}] {text}")

        current_para.append(text)
        if len(current_para) >= 6 or text.endswith(('.', '!', '?')):
            paragraphs.append(" ".join(current_para))
            current_para = []

        if count % 50 == 0:
            elapsed = time.time() - t0
            print(f"  Processados {count} segmentos... [{start_str}] ({elapsed:.1f}s decorridos)")

    if current_para:
        paragraphs.append(" ".join(current_para))

    total_time = time.time() - t0
    print(f"Transcrição concluída em {total_time:.1f}s ({total_time/60:.2f} min)!")
    print(f"Total de segmentos de fala extraídos: {len(segments_data)}")

    # 1. Salvar JSON completo
    json_path = os.path.join(output_dir, "transcricao_completa.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(segments_data, f, ensure_ascii=False, indent=2)
    print(f"Salvo: {json_path}")

    # 2. Salvar TXT com timestamps
    txt_ts_path = os.path.join(output_dir, "transcricao_com_timestamps.txt")
    with open(txt_ts_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines_with_ts))
    print(f"Salvo: {txt_ts_path}")

    # 3. Salvar TXT corrido
    txt_corrido_path = os.path.join(output_dir, "transcricao_texto_corrido.txt")
    with open(txt_corrido_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(paragraphs))
    print(f"Salvo: {txt_corrido_path}")

    return segments_data

def main():
    base_dir = r"F:\Transcricoes_Consolidadas\Aulas_10_09_2026"
    
    tasks = [
        {
            "audio": os.path.join(base_dir, "Parte_1_08-06-59", "audio_16k.wav"),
            "out": os.path.join(base_dir, "Parte_1_08-06-59")
        },
        {
            "audio": os.path.join(base_dir, "Parte_2_09-40-23", "audio_16k.wav"),
            "out": os.path.join(base_dir, "Parte_2_09-40-23")
        }
    ]

    print("Carregando modelo Whisper na GPU (CUDA)...")
    model = WhisperModel("small", device="cuda", compute_type="float16")
    print("Modelo carregado com sucesso!")

    for t in tasks:
        if os.path.exists(t["audio"]):
            transcribe_file(t["audio"], t["out"], model)
        else:
            print(f"ERRO: Arquivo não encontrado: {t['audio']}")

if __name__ == "__main__":
    main()
