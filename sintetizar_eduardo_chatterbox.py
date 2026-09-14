import subprocess
import json
import base64
from pathlib import Path

PYTHON_CHATTERBOX = r"C:\Users\NOVO OFFLINE\.openclaw\workspace\LocalDub-upstream\.venv-chatterbox\Scripts\python.exe"
WORKER = r"C:\Users\NOVO OFFLINE\.openclaw\workspace\LocalDub-upstream\backend\chatterbox_worker.py"
REF_AUDIO = r"C:\Users\NOVO OFFLINE\AppData\Local\LocalDub\voice_profiles\0fb717e8abb147c5\reference.ogg"
OUT_WAV = Path(r"F:\Transcricoes_Consolidadas\Podcasts_Tematicos\amostra_voz_clonada_Eduardo.wav")
OUT_MP3 = Path(r"F:\Transcricoes_Consolidadas\Podcasts_Tematicos\amostra_voz_clonada_Eduardo.mp3")

payload = {
    "text": "Olá! Esta é a minha voz clonada, o Eduardo, demonstrando que o meu perfil de voz local está ativo e funcionando na minha RTX 3060.",
    "ref_audio": REF_AUDIO,
    "exaggeration": 0.7,
    "cfg_weight": 0.35
}

print("Sintetizando voz clonada do Eduardo com Chatterbox PT-BR...")
p = subprocess.Popen(
    [PYTHON_CHATTERBOX, WORKER],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    encoding="utf-8"
)

stdout, stderr = p.communicate(input=json.dumps(payload) + "\n")

# Procura a linha com o JSON no stdout
data_line = None
for line in stdout.splitlines():
    line = line.strip()
    if line.startswith('{"ok":') or line.startswith('{"audio_data":'):
        data_line = line
        break

if not data_line and stdout.strip().startswith("{"):
    data_line = stdout.strip()

if data_line:
    res = json.loads(data_line)
    if res.get("ok"):
        raw_audio = base64.b64decode(res["audio_data"])
        OUT_WAV.write_bytes(raw_audio)
        print(f"Sucesso! Gerado {len(raw_audio)} bytes.")
        subprocess.run(["ffmpeg", "-y", "-i", str(OUT_WAV), "-c:a", "libmp3lame", "-b:a", "192k", str(OUT_MP3)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        OUT_WAV.unlink(missing_ok=True)
        print("Arquivo salvo com sucesso em:", OUT_MP3)
    else:
        print("Erro retornado pelo worker:", res.get("error"))
else:
    print("Nenhum JSON encontrado. Stdout:", stdout[:300])
    print("Stderr:", stderr[:300])
