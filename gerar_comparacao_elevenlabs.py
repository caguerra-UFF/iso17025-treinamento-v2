import os
import json
import urllib.request
import subprocess

API_KEY = "sk_dea857b7e1e6a546ce2b780720e8bc9173a74ce3ed9f7379"

# Save key in .env for future use
with open(".env", "a", encoding="utf-8") as f:
    f.write(f"\nELEVENLABS_API_KEY={API_KEY}\n")

# Voice IDs
VOICE_SARAH = "EXAVITQu4vr4xnSDxMaL"  # Host / Curiosa (equivalente a Thalita)
VOICE_ALICE = "Xb7hH8MSUJpSbSDYk0k2"  # Especialista (equivalente a Francisca)

dialogue = [
    ("Sarah", VOICE_SARAH, "Francisca, vamos começar falando de uma das maiores dores de cabeça nos laboratórios: o controle de calibração e manutenção. O instrutor do curso trouxe uma visão bem pragmática sobre isso no item 2.1."),
    ("Alice", VOICE_ALICE, "Excelente ponto, Thalita! E convenhamos, o pessoal adora complicar isso, né? Já vi laboratório mantendo três controles completamente separados pra mesma máquina. O que o instrutor defendeu aqui foi direto ao ponto: não precisa inventar moda. Calibração, verificação intermediária e manutenção preventiva podem estar integradas no mesmo plano geral."),
    ("Sarah", VOICE_SARAH, "Nossa, isso facilita demais! Mas me diz uma coisa: e o avaliador da Cgcre, aceita isso numa boa? A norma não exige formulários separados?"),
    ("Alice", VOICE_ALICE, "Aceita sim, com ressalva! Os requisitos 6.4.3 e 6.4.13 da ISO 17025 exigem que o plano exista e esteja sob controle rastreável. A força da evidência tá na rastreabilidade e no cumprimento das datas, e não na quantidade ou na complexidade de planilhas que você inventou."),
    ("Sarah", VOICE_SARAH, "Perfeito! Menos burocracia de gaveta e mais controle real do que realmente precisa ser feito no mês.")
]

temp_files = []
total_chars = 0

print("Iniciando sintese na ElevenLabs (Multilingual v2)...")

for i, (speaker, vid, text) in enumerate(dialogue):
    total_chars += len(text)
    out_file = f"_temp_eleven_{i}_{speaker}.mp3"
    temp_files.append(out_file)
    print(f"[{i+1}/{len(dialogue)}] Sintetizando {speaker} ({len(text)} chars)...")
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{vid}"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    with urllib.request.urlopen(req) as resp:
        with open(out_file, "wb") as f:
            f.write(resp.read())

print(f"Total de caracteres consumidos: {total_chars}")

# Concat with 250ms pause using ffmpeg
silence_file = "_silence_250ms.mp3"
if not os.path.exists(silence_file):
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", "0.25", "-b:a", "192k", silence_file], check=True)

concat_list_file = "_concat_eleven_list.txt"
with open(concat_list_file, "w", encoding="utf-8") as f:
    for i, tf in enumerate(temp_files):
        f.write(f"file '{tf}'\n")
        if i < len(temp_files) - 1:
            f.write(f"file '{silence_file}'\n")

output_mp3 = "Comparacao_Item_2_1_ElevenLabs_Sarah_e_Alice.mp3"
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_file, "-c:a", "libmp3lame", "-b:a", "192k", output_mp3], check=True)

# Clean up temp files
for tf in temp_files:
    if os.path.exists(tf):
        os.remove(tf)
if os.path.exists(concat_list_file):
    os.remove(concat_list_file)

print(f"SUCESSO! Arquivo gerado: {output_mp3} ({os.path.getsize(output_mp3)/1024:.1f} KB)")
