# -*- coding: utf-8 -*-
import asyncio
import json
import os
import sys
import subprocess
import tempfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

import edge_tts

VOZ_THALITA = "pt-BR-ThalitaMultilingualNeural"
VOZ_FRANCISCA = "pt-BR-FranciscaNeural"

async def sintetizar(texto: str, voz: str, rate: str = "+0%", pitch: str = "+0Hz") -> bytes:
    comm = edge_tts.Communicate(texto, voz, rate=rate, pitch=pitch)
    chunks = []
    async for ch in comm.stream():
        if ch["type"] == "audio":
            chunks.append(ch["data"])
    return b"".join(chunks)

async def gerar_episodio(ep: dict, out_dir: Path, silence_path: Path) -> Path:
    out_file = out_dir / ep["filename"]
    title = ep.get("title", ep["filename"])
    print(f"\n[*] Processando: {title}...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        concat_txt = tmp_path / "concat.txt"
        lines = []
        for idx, turn in enumerate(ep["dialogue"]):
            speaker = turn[0]
            text = turn[1]
            voz = VOZ_THALITA if speaker == "Thalita" else VOZ_FRANCISCA
            rate = "+14%" if speaker == "Thalita" else "+10%"
            pitch = "+4Hz" if speaker == "Thalita" else "+2Hz"
            disp = text[:55] if len(text) > 55 else text
            print(f"   [{speaker} ({rate},{pitch})]: \"{disp}...\"")
            audio = await sintetizar(text, voz, rate=rate, pitch=pitch)
            cfile = tmp_path / f"turn_{idx:02d}.mp3"
            cfile.write_bytes(audio)
            lines.append(f"file '{cfile.as_posix()}'")
            if idx < len(ep["dialogue"]) - 1:
                lines.append(f"file '{silence_path.as_posix()}'")

        concat_txt.write_text("\n".join(lines), encoding="utf-8")
        cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_txt),
            "-c:a", "libmp3lame", "-b:a", "192k",
            str(out_file)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    kb = out_file.stat().st_size // 1024
    print(f"[OK] Gerado: {out_file.name} ({kb} KB)")
    return out_file

async def main():
    if len(sys.argv) < 2:
        print("Uso: python gerar_podcast_por_json.py <arquivo_config.json>")
        sys.exit(1)

    json_path = Path(sys.argv[1])
    with open(json_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    out_dir = Path(config["output_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print(f" GERANDO (SUPER ANIMADA): {config.get('title', json_path.stem)}")
    print("=" * 60)

    silence_file = out_dir / "_silence_180ms.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anullsrc=channel_layout=mono:sample_rate=24000",
        "-t", "0.18", "-q:a", "9", "-acodec", "libmp3lame",
        str(silence_file)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    gerados = []
    for ep in config["episodes"]:
        caminho = await gerar_episodio(ep, out_dir, silence_file)
        gerados.append(caminho)

    if "chapter_filename" in config and config["chapter_filename"]:
        chap_file = out_dir / config["chapter_filename"]
        print(f"\n[Unificação] Gerando capítulo completo: {chap_file.name}...")
        silence_1s = out_dir / "_silence_1s.mp3"
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi",
            "-i", "anullsrc=channel_layout=mono:sample_rate=24000",
            "-t", "1.0", "-q:a", "9", "-acodec", "libmp3lame",
            str(silence_1s)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
            linhas_full = []
            for g in gerados:
                linhas_full.append(f"file '{g.as_posix()}'")
                linhas_full.append(f"file '{silence_1s.as_posix()}'")
            f.write("\n".join(linhas_full))
            concat_full = f.name

        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", concat_full,
            "-c:a", "libmp3lame", "-b:a", "192k",
            str(chap_file)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        try:
            silence_file.unlink(missing_ok=True)
            silence_1s.unlink(missing_ok=True)
            os.remove(concat_full)
        except Exception:
            pass
        kb_chap = chap_file.stat().st_size // 1024
        print(f"[OK Capítulo Completo] {chap_file.name} ({kb_chap} KB)")

    print(f"\n[Finalizado com Sucesso] Arquivos em: {out_dir}")

if __name__ == "__main__":
    asyncio.run(main())