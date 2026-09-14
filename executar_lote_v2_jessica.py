# -*- coding: utf-8 -*-
import asyncio
import json
import os
import sys
import subprocess
import tempfile
import urllib.request
import urllib.error
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

import edge_tts

V2_ROOT = Path(r"F:\Transcricoes_Consolidadas_V2")
STATE_FILE = V2_ROOT / "status_geracao_jessica.json"
VOICE_JESSICA_ID = "cgSgspJ2msm6clMCkdW9"
VOICE_FRANCISCA = "pt-BR-FranciscaNeural"

def get_api_key():
    env_file = V2_ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.strip().startswith("ELEVENLABS_API_KEY="):
                return line.split("=", 1)[1].strip()
    return "sk_dea857b7e1e6a546ce2b780720e8bc9173a74ce3ed9f7379"

def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {"generated_episodes": {}, "total_chars_consumed": 0}
    return {"generated_episodes": {}, "total_chars_consumed": 0}

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")

def sintetizar_jessica(texto: str, out_file: Path, api_key: str):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_JESSICA_ID}"
    payload = json.dumps({
        "text": texto,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.2,
            "use_speaker_boost": True
        }
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg"
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            out_file.write_bytes(resp.read())
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8", errors="ignore")
        if e.code in (401, 402, 429) or "quota" in err_msg.lower() or "character_limit" in err_msg.lower():
            raise RuntimeError(f"QUOTA_ESGOTADA: HTTP {e.code} - {err_msg}")
        raise RuntimeError(f"HTTP {e.code} da ElevenLabs: {err_msg}")

async def sintetizar_francisca(texto: str, out_file: Path, rate: str = "+10%", pitch: str = "+2Hz"):
    comm = edge_tts.Communicate(texto, VOICE_FRANCISCA, rate=rate, pitch=pitch)
    chunks = []
    async for ch in comm.stream():
        if ch["type"] == "audio":
            chunks.append(ch["data"])
    out_file.write_bytes(b"".join(chunks))

async def processar_episodio(ep: dict, out_dir: Path, silence_path: Path, api_key: str) -> int:
    out_file = out_dir / ep["filename"]
    title = ep.get("title", ep["filename"])
    print(f"\n[*] Sintetizando Jessica: {title}")
    
    chars_used = 0
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        concat_txt = tmp_path / "concat.txt"
        lines = []

        for idx, turn in enumerate(ep["dialogue"]):
            speaker = turn[0]
            text = turn[1]
            cfile = tmp_path / f"turn_{idx:02d}.mp3"
            disp = text[:50] if len(text) > 50 else text

            if speaker in ("Thalita", "Jessica"):
                chars_used += len(text)
                print(f"   [Jessica ({len(text)} chars)]: \"{disp}...\"")
                sintetizar_jessica(text, cfile, api_key)
            else:
                print(f"   [Francisca]: \"{disp}...\"")
                await sintetizar_francisca(text, cfile)

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
    print(f"[OK] Gerado com sucesso: {out_file.name} ({kb} KB, {chars_used} chars Jessica)")
    return chars_used

async def main():
    api_key = get_api_key()
    print("=" * 65)
    print(" BATCH RUNNER V2: SUBSTITUIÇÃO DA APRESENTADORA (JESSICA)")
    print(f" Chave em uso: {api_key[:8]}...{api_key[-4:]}")
    print("=" * 65)

    state = load_state()
    generated = state.setdefault("generated_episodes", {})

    dialogue_files = [
        "dialogos_parte2_cap2.json",
        "dialogos_parte2_cap3.json",
        "dialogos_parte2_cap4.json",
        "dialogos_parte2_cap5.json",
        "dialogos_parte2_cap6.json",
        "dialogos_parte2_cap7.json",
        "dialogos_parte2_cap8.json",
        "dialogos_parte2_cap9.json",
        "dialogos_parte2_cap10_especial.json",
        "dialogos_parte2_cap11_especial.json",
        "dialogos_parte3_cap2.json",
        "dialogos_parte3_cap3.json",
        "dialogos_parte3_cap4.json",
        "dialogos_parte3_cap5_6_7.json",
        "dialogos_parte3_cap8_9_10.json",
        "dialogos_parte3_cap11_especial.json",
        "dialogos_parte3_cap12_especial.json"
    ]

    silence_file = V2_ROOT / "_silence_180ms.mp3"
    if not silence_file.exists():
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi",
            "-i", "anullsrc=channel_layout=mono:sample_rate=24000",
            "-t", "0.18", "-q:a", "9", "-acodec", "libmp3lame",
            str(silence_file)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    total_novos = 0
    quota_esgotada = False

    for df in dialogue_files:
        dpath = V2_ROOT / df
        if not dpath.exists():
            continue

        with open(dpath, "r", encoding="utf-8") as jf:
            config = json.load(jf)

        raw_out = config["output_dir"]
        v2_out = raw_out.replace("Transcricoes_Consolidadas", "Transcricoes_Consolidadas_V2")
        out_dir = Path(v2_out)
        out_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n>>> Processando Arquivo: {df} ({config.get('title')})")

        for ep in config["episodes"]:
            fname = ep["filename"]
            if fname in generated:
                print(f"   [PULADO - Já Gerado] {fname}")
                continue

            try:
                chars = await processar_episodio(ep, out_dir, silence_file, api_key)
                generated[fname] = {
                    "chars": chars,
                    "title": ep.get("title", fname),
                    "file": str((out_dir / fname).relative_to(V2_ROOT))
                }
                state["total_chars_consumed"] = state.get("total_chars_consumed", 0) + chars
                save_state(state)
                total_novos += 1
            except RuntimeError as e:
                err_str = str(e)
                if "QUOTA_ESGOTADA" in err_str:
                    print(f"\n" + "!" * 65)
                    print(f"[ALERTA DE COTA] A cota da API ElevenLabs foi esgotada!")
                    print(f"Detalhes: {err_str}")
                    print(f"Último arquivo interrompido: {fname}")
                    print("!" * 65)
                    quota_esgotada = True
                    break
                else:
                    print(f"[ERRO NO EPISÓDIO {fname}]: {e}")
                    raise

        if quota_esgotada:
            break

    print("\n" + "=" * 65)
    print(f" RESUMO DA EXECUÇÃO:")
    print(f" - Episódios gerados nesta rodada: {total_novos}")
    print(f" - Total acumulado com a voz Jessica: {len(generated)} episódios")
    print(f" - Total de caracteres Jessica consumidos: {state.get('total_chars_consumed', 0)}")
    if quota_esgotada:
        print(" [STATUS] PAUSADO POR ESGOTAMENTO DE COTA. AGUARDANDO NOVA CHAVE.")
    else:
        print(" [STATUS] CONCLUÍDO COM SUCESSO!")
    print("=" * 65)

if __name__ == "__main__":
    asyncio.run(main())
