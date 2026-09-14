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
STATE_FILE = V2_ROOT / "status_aulas_jessica.json"
VOICE_JESSICA_ID = "cgSgspJ2msm6clMCkdW9"
VOICE_STUDENT = "pt-BR-AntonioNeural"

def get_api_key():
    env_file = V2_ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.strip().startswith("ELEVENLABS_API_KEY="):
                return line.split("=", 1)[1].strip()
    return ""

def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {"generated_trechos": {}, "total_chars_consumed": 0}
    return {"generated_trechos": {}, "total_chars_consumed": 0}

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")

def sintetizar_jessica(texto: str, out_file: Path, api_key: str):
    if not api_key:
        raise RuntimeError("API_KEY_VAZIA: Nenhuma chave da ElevenLabs foi configurada.")
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
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            out_file.write_bytes(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")
        if e.code in (401, 402, 429) and ("quota_exceeded" in body or "quota" in body.lower()):
            raise RuntimeError(f"QUOTA_ESGOTADA: HTTP {e.code} - {body}")
        else:
            raise RuntimeError(f"HTTP {e.code}: {body}")

async def sintetizar_aluno(texto: str, out_file: Path):
    communicate = edge_tts.Communicate(texto, VOICE_STUDENT)
    chunks = []
    async for ch in communicate.stream():
        if ch["type"] == "audio":
            chunks.append(ch["data"])
    out_file.write_bytes(b"".join(chunks))

def extrair_itens_aula():
    html_file = V2_ROOT / "index.html"
    if not html_file.exists():
        html_file = Path(r"F:\Transcricoes_Consolidadas\index.html")
    
    with open(html_file, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.strip().startswith("const itemsData = ["):
                raw = line.strip()[len("const itemsData = "):-1]
                data = json.loads(raw)
                return [d for d in data if d.get("trecho_audio")]
    return []

async def processar_trecho(item: dict, silence_path: Path, api_key: str) -> int:
    rel_audio = item["trecho_audio"]
    out_file = V2_ROOT / rel_audio
    out_file.parent.mkdir(parents=True, exist_ok=True)
    
    title = item.get("title", rel_audio)
    print(f"\n[*] Processando Trecho de Aula: {rel_audio} | {title[:60]}")
    
    dialogo = item.get("dialogo_integra", [])
    if not dialogo:
        quote = item.get("quote", "")
        if not quote:
            print(f"   [AVISO] Trecho sem texto transcrito! Pulando...")
            return 0
        dialogo = [{"speaker": "Instrutora", "role": "instructor", "text": quote}]

    chars_used = 0
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        concat_txt = tmp_path / "concat.txt"
        lines = []

        for idx, turn in enumerate(dialogo):
            spk = turn.get("speaker", "")
            role = turn.get("role", "")
            text = turn.get("text", "").strip()
            if not text:
                continue

            cfile = tmp_path / f"turn_{idx:03d}.mp3"
            disp = text[:50] if len(text) > 50 else text

            is_instructor = (role == "instructor" or "Instrutora" in spk or "Lina" in spk or "Luana" in spk)

            if is_instructor:
                chars_used += len(text)
                print(f"   [Jessica ({len(text)} chars)]: \"{disp}...\"")
                sintetizar_jessica(text, cfile, api_key)
            else:
                print(f"   [Aluno / Participante]: \"{disp}...\"")
                await sintetizar_aluno(text, cfile)

            lines.append(f"file '{cfile.as_posix()}'")
            if idx < len(dialogo) - 1:
                lines.append(f"file '{silence_path.as_posix()}'")

        if not lines:
            return 0

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
    print(" BATCH RUNNER V2: SUBSTITUIÇÃO DA VOZ DA AULA (JESSICA)")
    print(f" Chave em uso: {api_key[:8]}...{api_key[-4:] if len(api_key)>12 else ''}")
    print("=" * 65)

    if not api_key:
        print("[ERRO] Nenhuma chave ElevenLabs configurada em .env!")
        return

    state = load_state()
    generated = state.setdefault("generated_trechos", {})
    trechos = extrair_itens_aula()
    print(f"Total de trechos de aula mapeados: {len(trechos)}")
    print(f"Trechos já sintetizados com Jessica: {len(generated)}")

    silence_file = V2_ROOT / "_silence_250ms.mp3"
    if not silence_file.exists():
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi",
            "-i", "anullsrc=channel_layout=mono:sample_rate=24000",
            "-t", "0.25", "-q:a", "9", "-acodec", "libmp3lame",
            str(silence_file)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    total_novos = 0
    quota_esgotada = False

    for item in trechos:
        rel_audio = item.get("trecho_audio")
        if not rel_audio:
            continue
        fname = Path(rel_audio).name

        if fname in generated:
            continue

        try:
            chars = await processar_trecho(item, silence_file, api_key)
            generated[fname] = {
                "chars": chars,
                "title": item.get("title", fname),
                "item_id": item.get("item_id"),
                "file": rel_audio
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
                print(f"Último trecho de aula interrompido: {fname} ({item.get('title')})")
                print("!" * 65)
                quota_esgotada = True
                break
            else:
                print(f"[ERRO NO TRECHO {fname}]: {e}")
                raise

    print("\n" + "=" * 65)
    print(f" RESUMO DA EXECUÇÃO:")
    print(f" - Trechos de aula gerados nesta rodada: {total_novos}")
    print(f" - Total acumulado de trechos de aula com a Jessica: {len(generated)}/{len(trechos)}")
    print(f" - Total de caracteres Jessica consumidos: {state.get('total_chars_consumed', 0)}")
    if quota_esgotada:
        print(" [STATUS] PAUSADO POR ESGOTAMENTO DE COTA. AGUARDANDO NOVA CHAVE.")
    else:
        print(" [STATUS] CONCLUÍDO OU AGUARDANDO PRÓXIMAS AÇÕES.")
    print("=" * 65)

if __name__ == "__main__":
    asyncio.run(main())
