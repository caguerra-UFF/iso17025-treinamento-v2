import subprocess
import json
import base64
from pathlib import Path

PYTHON_CHATTERBOX = r"C:\Users\NOVO OFFLINE\.openclaw\workspace\LocalDub-upstream\.venv-chatterbox\Scripts\python.exe"
WORKER = r"C:\Users\NOVO OFFLINE\.openclaw\workspace\LocalDub-upstream\backend\chatterbox_worker.py"
REF_AUDIO = r"C:\Users\NOVO OFFLINE\AppData\Local\LocalDub\voice_profiles\0fb717e8abb147c5\reference.ogg"
OUT_WAV = Path(r"F:\Transcricoes_Consolidadas\Podcasts_Tematicos\teste_voz_clonada_Eduardo.wav")
OUT_MP3 = Path(r"F:\Transcricoes_Consolidadas\Podcasts_Tematicos\teste_voz_clonada_Eduardo.mp3")

payload = {
    "text": "Olá, pessoal! Esta é a minha voz clonada, o Eduardo, testando a síntese local na minha placa de vídeo.",
    "ref_audio": REF_AUDIO,
    "exaggeration": 0.75,
    "cfg_weight": 0.35
}

print("Enviando requisição para o Chatterbox PT-BR na RTX 3060...")
p = subprocess.Popen(
    [PYTHON_CHATTERBOX, WORKER],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    encoding="utf-8"
)

stdout, stderr = p.communicate(input=json.dumps(payload) + "\n")
res = json.loads(stdout.strip())

if res.get("ok"):
    raw_audio = base64.b64decode(res["audio_data"])
    OUT_WAV.write_bytes(raw_audio)
    print(f"Sucesso! Gerado {len(raw_audio)} bytes em {res.get('latency_ms')} ms")
    # Converte para MP3
    subprocess.run(["ffmpeg", "-y", "-i", str(OUT_WAV), "-c:a", "libmp3lame", "-b:a", "192k", str(OUT_MP3)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print("Salvo em:", OUT_MP3)
else:
    print("Erro:", res.get("error"))
