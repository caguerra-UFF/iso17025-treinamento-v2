import os
import sys
import re
import cv2
import json
import time
import numpy as np
import easyocr

def format_timestamp(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def extract_iso_clause(text: str) -> str:
    # Procura padrões de cláusulas como "8.5", "5.1", "Cláusula 7", etc.
    m = re.search(r'\b([4-8]\.[0-9]+(?:\.[0-9]+)?)\b', text)
    if m:
        return f"Item {m.group(1)}"
    
    m2 = re.search(r'\b([4-8])\.\s*([A-Za-zÀ-ÿ]+(?:\s+[A-Za-zÀ-ÿ]+){1,3})', text)
    if m2:
        return f"Seção {m2.group(1)} - {m2.group(2)}"

    lower = text.lower()
    if "acredita" in lower:
        return "Conceito de Acreditação"
    elif "imparcialidade" in lower:
        return "Item 4.1 Imparcialidade"
    elif "confidencialidade" in lower:
        return "Item 4.2 Confidencialidade"
    elif "estrutura" in lower:
        return "Seção 5 Requisitos de Estrutura"
    elif "recursos" in lower:
        return "Seção 6 Requisitos de Recursos"
    elif "processo" in lower:
        return "Seção 7 Requisitos de Processo"
    elif "gestão" in lower or "gestao" in lower:
        return "Seção 8 Sistema de Gestão"
    elif "risco" in lower:
        return "Item 8.5 Riscos e Oportunidades"
    elif "auditoria" in lower:
        return "Item 8.8 Auditorias Internas"
    
    return "Geral / Treinamento"

def process_video_slides(video_path: str, output_dir: str, ocr_reader: easyocr.Reader):
    print(f"\n=======================================================", flush=True)
    print(f"Processando Slides de: {video_path}", flush=True)
    print(f"Diretório de saída: {output_dir}", flush=True)
    print(f"=======================================================", flush=True)

    slides_dir = os.path.join(output_dir, "slides")
    os.makedirs(slides_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"ERRO: Não foi possível abrir o vídeo {video_path}", flush=True)
        return

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_duration = total_frames / fps

    print(f"FPS: {fps:.2f} | Total Frames: {total_frames} | Duração: {format_timestamp(video_duration)}", flush=True)

    # Amostragem a cada 3 segundos
    sample_interval_sec = 3.0
    sample_step = int(fps * sample_interval_sec)

    detected_slides = []
    last_thumb = None
    last_slide_time = 0.0

    t0 = time.time()
    frame_idx = 0

    print("Iniciando detecção de transições de slides...", flush=True)
    while frame_idx < total_frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            break

        sec = frame_idx / fps
        h, m, s = int(sec // 3600), int((sec % 3600) // 60), int(sec % 60)
        ts_str = f"{h:02d}:{m:02d}:{s:02d}"

        # Região do slide dentro da janela do Teams (ajustada para 1280x720)
        # y: 180 a 645, x: 50 a 940
        slide_crop = frame[180:645, 50:940]
        gray = cv2.cvtColor(slide_crop, cv2.COLOR_BGR2GRAY)
        thumb = cv2.resize(gray, (160, 90))

        if last_thumb is None:
            last_thumb = thumb
            last_slide_time = sec
            detected_slides.append({
                "slide_idx": len(detected_slides) + 1,
                "start_sec": sec,
                "start_str": ts_str,
                "frame_crop": slide_crop.copy()
            })
            print(f"  Slide #1 detectado em {ts_str}", flush=True)
        else:
            diff = np.mean(np.abs(thumb.astype(float) - last_thumb.astype(float)))
            # Transição significativa e tempo mínimo de permanência (>= 6s)
            if diff > 11.0 and (sec - last_slide_time) >= 6.0:
                # Atualizar tempo final do slide anterior
                detected_slides[-1]["end_sec"] = sec
                detected_slides[-1]["end_str"] = ts_str
                detected_slides[-1]["duration"] = round(sec - detected_slides[-1]["start_sec"], 1)

                last_slide_time = sec
                detected_slides.append({
                    "slide_idx": len(detected_slides) + 1,
                    "start_sec": sec,
                    "start_str": ts_str,
                    "frame_crop": slide_crop.copy()
                })
                last_thumb = thumb
                print(f"  Slide #{len(detected_slides)} detectado em {ts_str} (diff={diff:.1f})", flush=True)

        frame_idx += sample_step

    cap.release()

    # Finalizar último slide
    if detected_slides:
        detected_slides[-1]["end_sec"] = video_duration
        detected_slides[-1]["end_str"] = format_timestamp(video_duration)
        detected_slides[-1]["duration"] = round(video_duration - detected_slides[-1]["start_sec"], 1)

    print(f"\nExtração de quadros concluída em {time.time()-t0:.1f}s! Total de slides detectados: {len(detected_slides)}", flush=True)

    # Carregar transcrição se existir para correlacionar
    transcription_file = os.path.join(output_dir, "transcricao_completa.json")
    transcripts = []
    if os.path.exists(transcription_file):
        with open(transcription_file, "r", encoding="utf-8") as f:
            transcripts = json.load(f)
        print(f"Carregados {len(transcripts)} segmentos de fala para correlação.", flush=True)

    # Executar OCR e Correlação
    print("\nExecutando OCR e correlação com a fala de cada slide...", flush=True)
    slides_metadata = []
    slides_txt_lines = [
        "=" * 100,
        f"METADADOS DE SLIDES E CORRELAÇÃO - {os.path.basename(video_path)}",
        f"Duração Total: {format_timestamp(video_duration)} | Total de Slides Únicos: {len(detected_slides)}",
        "=" * 100,
        f"{'SLIDE':<8} {'TEMPO':<12} {'DURAÇÃO':<10} {'CLÁUSULA/ITEM':<25} {'ASSUNTO / TÍTULO'}",
        "-" * 100
    ]

    correlation_doc = [
        "=" * 100,
        f"CORRELAÇÃO COMPLETA: SLIDES & TRANSCRIÇÃO DA FALA - {os.path.basename(video_path)}",
        "=" * 100,
        ""
    ]

    for item in detected_slides:
        s_idx = item["slide_idx"]
        s_start = item["start_sec"]
        s_end = item["end_sec"]
        s_start_str = item["start_str"]
        s_end_str = item["end_str"]
        s_dur = item["duration"]

        # Salvar imagem do slide
        time_slug = s_start_str.replace(":", "-")
        img_filename = f"slide_{s_idx:03d}_{time_slug}.jpg"
        img_full_path = os.path.join(slides_dir, img_filename)
        cv2.imwrite(img_full_path, item["frame_crop"], [cv2.IMWRITE_JPEG_QUALITY, 92])

        # OCR
        ocr_lines = ocr_reader.readtext(item["frame_crop"], detail=0)
        clean_lines = [l.strip() for l in ocr_lines if len(l.strip()) > 1 and "LCN" not in l.upper()]
        
        # Título provável (primeiras linhas com conteúdo)
        titulo_assunto = "Slide de Apresentação"
        if clean_lines:
            titulo_assunto = clean_lines[0]
            if len(clean_lines) > 1 and len(titulo_assunto) < 5:
                titulo_assunto = f"{titulo_assunto} - {clean_lines[1]}"

        full_ocr_text = " \n ".join(clean_lines)
        clausula_iso = extract_iso_clause(full_ocr_text)

        # Correlacionar com transcrição
        speech_in_slide = []
        for t in transcripts:
            # Segmento iniciou dentro da janela do slide ou cobre o slide
            if (t["start"] >= s_start and t["start"] < s_end) or (t["start"] <= s_start and t["end"] > s_start):
                speech_in_slide.append(t)

        speech_text = " ".join([seg["text"] for seg in speech_in_slide]).strip()

        meta = {
            "slide_id": f"SLIDE_{s_idx:03d}",
            "arquivo_imagem": f"slides/{img_filename}",
            "caminho_absoluto": img_full_path,
            "timestamp_inicio": s_start_str,
            "timestamp_inicio_segundos": s_start,
            "timestamp_fim": s_end_str,
            "timestamp_fim_segundos": s_end,
            "duracao_segundos": s_dur,
            "duracao_formatada": format_timestamp(s_dur),
            "titulo_assunto": titulo_assunto,
            "clausula_iso": clausula_iso,
            "linhas_ocr": clean_lines,
            "texto_ocr_completo": full_ocr_text,
            "quantidade_falas_correlacionadas": len(speech_in_slide),
            "transcricao_fala_slide": speech_text
        }
        slides_metadata.append(meta)

        # Linha para tabela resumo TXT
        dur_str = format_timestamp(s_dur)
        slides_txt_lines.append(
            f"#{s_idx:03d}     {s_start_str}     {dur_str}   {clausula_iso:<25} {titulo_assunto[:40]}"
        )

        # Bloco para documento de correlação profunda
        correlation_doc.append(f"────────────────────────────────────────────────────────────────────────────────")
        correlation_doc.append(f"SLIDE #{s_idx:03d} [{s_start_str} -> {s_end_str}] (Duração: {dur_str})")
        correlation_doc.append(f"Arquivo: slides/{img_filename}")
        correlation_doc.append(f"Cláusula/Assunto: {clausula_iso} | Título: {titulo_assunto}")
        correlation_doc.append(f"Conteúdo em Tela (OCR):")
        for cl in clean_lines[:6]:
            correlation_doc.append(f"   • {cl}")
        if len(clean_lines) > 6:
            correlation_doc.append(f"   • ... (+ {len(clean_lines)-6} linhas)")
        correlation_doc.append(f"\nFala da Instrutora / Participantes durante este slide:")
        if speech_text:
            correlation_doc.append(f"\"{speech_text}\"")
        else:
            correlation_doc.append("(Sem falas registradas neste intervalo ou período silencioso)")
        correlation_doc.append("")

        if s_idx % 5 == 0:
            print(f"  Processado Slide #{s_idx}/{len(detected_slides)}: [{s_start_str}] {titulo_assunto[:30]}", flush=True)

    # Salvar arquivos de saída
    meta_json_path = os.path.join(output_dir, "metadados_slides.json")
    with open(meta_json_path, "w", encoding="utf-8") as f:
        json.dump(slides_metadata, f, ensure_ascii=False, indent=2)
    print(f"\nSalvo: {meta_json_path}", flush=True)

    meta_txt_path = os.path.join(output_dir, "metadados_slides.txt")
    with open(meta_txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(slides_txt_lines))
    print(f"Salvo: {meta_txt_path}", flush=True)

    corr_json_path = os.path.join(output_dir, "correlacao_slides_transcricao.json")
    with open(corr_json_path, "w", encoding="utf-8") as f:
        json.dump([
            {
                "slide_id": m["slide_id"],
                "arquivo": m["arquivo_imagem"],
                "tempo": m["timestamp_inicio"],
                "titulo": m["titulo_assunto"],
                "clausula": m["clausula_iso"],
                "fala_correlacionada": m["transcricao_fala_slide"]
            } for m in slides_metadata
        ], f, ensure_ascii=False, indent=2)
    print(f"Salvo: {corr_json_path}", flush=True)

    corr_txt_path = os.path.join(output_dir, "correlacao_slides_transcricao.txt")
    with open(corr_txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(correlation_doc))
    print(f"Salvo: {corr_txt_path}", flush=True)

def main():
    base_dir = r"F:\Transcricoes_Consolidadas\Aulas_10_09_2026"
    
    videos = [
        {
            "path": r"F:\2026-09-10 08-06-59.mp4",
            "out": os.path.join(base_dir, "Parte_1_08-06-59")
        },
        {
            "path": r"F:\2026-09-10 09-40-23.mp4",
            "out": os.path.join(base_dir, "Parte_2_09-40-23")
        },
        {
            "path": r"F:\2026-09-10 13-35-40.mp4",
            "out": os.path.join(base_dir, "Parte_3_13-35-40")
        }
    ]

    print("Inicializando leitor OCR (EasyOCR) na GPU...", flush=True)
    reader = easyocr.Reader(['pt'], gpu=True)
    print("Leitor OCR pronto!", flush=True)

    for v in videos:
        if os.path.exists(v["path"]):
            process_video_slides(v["path"], v["out"], reader)
        else:
            print(f"AVISO: Vídeo não encontrado: {v['path']}", flush=True)

if __name__ == "__main__":
    main()
