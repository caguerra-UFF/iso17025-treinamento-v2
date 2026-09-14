import os
import json
import urllib.request
import subprocess

API_KEY = "sk_dea857b7e1e6a546ce2b780720e8bc9173a74ce3ed9f7379"

# Voice IDs
VOICE_LAURA = "FGY2WhTYpPnrIDTdsKH5"   # Laura - Enthusiast, Quirky, Sassy
VOICE_JESSICA = "cgSgspJ2msm6clMCkdW9" # Jessica - Playful, Bright, Warm

dialogue = [
    ("Laura", VOICE_LAURA, 0.28, 0.45, "Gente, vamos começar falando de uma das maiores dores de cabeça nos laboratórios: o controle de calibração e manutenção! O instrutor do curso trouxe uma visão super prática sobre isso no item 2.1."),
    ("Jessica", VOICE_JESSICA, 0.30, 0.40, "Excelente ponto! E convenhamos, o pessoal adora complicar isso, né? Já vi laboratório mantendo três controles completamente separados pra mesma máquina! O que o instrutor defendeu aqui foi direto ao ponto: não precisa inventar moda! Calibração, verificação intermediária e manutenção preventiva podem sim estar integradas no mesmo plano geral!"),
    ("Laura", VOICE_LAURA, 0.28, 0.45, "Nossa, isso facilita demais a vida! Mas me diz uma coisa: e o avaliador da Cgcre, aceita isso numa boa? A norma não exige formulários separados?"),
    ("Jessica", VOICE_JESSICA, 0.30, 0.40, "Aceita sim, com ressalva! Os requisitos 6.4.3 e 6.4.13 da ISO 17025 exigem que o plano exista e esteja sob controle rastreável! A força da evidência tá na rastreabilidade e no cumprimento das datas, e não na quantidade de planilhas que você inventou!"),
    ("Laura", VOICE_LAURA, 0.28, 0.45, "Perfeito! Menos burocracia de gaveta e muito mais controle real do que realmente precisa ser feito no mês!")
]

temp_files = []
print("Iniciando sintese na ElevenLabs Super Animada...")

for i, (speaker, vid, stab, sty, text) in enumerate(dialogue):
    out_file = f"_temp_eleven_animada_{i}_{speaker}.mp3"
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
            "stability": stab,
            "similarity_boost": 0.75,
            "style": sty,
            "use_speaker_boost": True
        }
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    with urllib.request.urlopen(req) as resp:
        with open(out_file, "wb") as f:
            f.write(resp.read())

# Concat with 180ms pause using ffmpeg
silence_file = "_silence_180ms.mp3"
if not os.path.exists(silence_file):
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", "0.18", "-b:a", "192k", silence_file], check=True)

concat_list_file = "_concat_eleven_animada.txt"
with open(concat_list_file, "w", encoding="utf-8") as f:
    for i, tf in enumerate(temp_files):
        f.write(f"file '{tf}'\n")
        if i < len(temp_files) - 1:
            f.write(f"file '{silence_file}'\n")

output_mp3 = "Comparacao_Item_2_1_ElevenLabs_Super_Animada.mp3"
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_file, "-c:a", "libmp3lame", "-b:a", "192k", output_mp3], check=True)

for tf in temp_files:
    if os.path.exists(tf): os.remove(tf)
if os.path.exists(concat_list_file): os.remove(concat_list_file)

print(f"SUCESSO ElevenLabs Super Animada: {output_mp3} ({os.path.getsize(output_mp3)/1024:.1f} KB)")
