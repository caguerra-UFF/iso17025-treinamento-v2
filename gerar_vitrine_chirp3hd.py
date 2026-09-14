"""
Vitrine com outras vozes do Google Chirp 3 HD e novo debate com Puck (voz dinâmica do Gemini).
"""
import os
import sys
import subprocess
import tempfile
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.cloud import texttospeech

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

OUTPUT_DIR = Path(r"F:\Transcricoes_Consolidadas\Podcasts_Tematicos\Chirp3HD")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TOKEN_FILE = Path(r"F:\Transcricoes_Consolidadas\token_gcloud.json")

# Amostras individuais de vozes destacadas do Chirp 3 HD
AMOSTRAS = [
    ("pt-BR-Chirp3-HD-Puck", "Olá! Eu sou o Puck no modelo Chirp 3 HD. Minha entonação é mais animada, jovem e dinâmica, perfeita para um debate de podcast bem solto."),
    ("pt-BR-Chirp3-HD-Aoede", "Olá! Eu sou a Aoede. Minha voz tem um equilíbrio natural e suave, muito expressiva e agradável para explicações técnicas."),
    ("pt-BR-Chirp3-HD-Charon", "Olá! Eu sou o Charon. Tenho uma voz masculina mais firme e encorpada, transmitindo maturidade e confiança."),
    ("pt-BR-Chirp3-HD-Kore", "Oi! Eu sou a Kore. Minha fala é acolhedora, clara e fluida, ótima para condução didática."),
    ("pt-BR-Chirp3-HD-Fenrir", "Olá! Aqui é o Fenrir. Meu timbre é robusto e direto, ideal para trazer perguntas práticas e incisivas."),
    ("pt-BR-Chirp3-HD-Achernar", "Olá! Eu sou a Achernar. Minha voz é firme, assertiva e profissional, excelente para pareceres normativos."),
    ("pt-BR-Chirp3-HD-Enceladus", "E eu sou o Enceladus. Um tom masculino equilibrado de locução de rádio e jornalismo.")
]

# Debate Item 2.1 com Aoede e Puck
DIALOGO_2_1 = [
    ("Aoede", "Lucas, vamos começar falando de uma das maiores dores de cabeça nos laboratórios: o controle de calibração e manutenção. O instrutor do curso trouxe uma visão bem pragmática sobre isso no item 2.1."),
    ("Puck", "Excelente, Mariana! E convenhamos, o pessoal adora complicar isso, né? Já vi laboratório mantendo três controles completamente separados pra mesma máquina. O que o instrutor defendeu aqui?"),
    ("Aoede", "Ele foi direto ao ponto: não precisa inventar moda. Calibração, verificação intermediária e manutenção preventiva podem estar integradas no mesmo plano geral. O procedimento define as regras e a periodicidade, mas o plano prático só precisa mostrar claramente quando a ação está prevista pra acontecer."),
    ("Puck", "Faz muito sentido. Mas me diz uma coisa: e o avaliador da Cgcre, aceita isso numa boa? A norma não exige formulários separados?"),
    ("Aoede", "Aceita sim, com ressalva! Os requisitos 6.4.3 e 6.4.13 da ISO 17025 exigem que o plano exista e esteja sob controle rastreável. A força da evidência tá na rastreabilidade e no cumprimento das datas, e não na quantidade ou na complexidade de planilhas que você inventou."),
    ("Puck", "Perfeito! Menos burocracia de gaveta e mais controle real do que realmente precisa ser feito no mês.")
]


def sintetizar(client, text, voice_name):
    s_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code="pt-BR", name=voice_name)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    return client.synthesize_speech(input=s_input, voice=voice, audio_config=audio_config).audio_content


def main():
    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE))
    client = texttospeech.TextToSpeechClient(credentials=creds)

    silence_file = OUTPUT_DIR / "_silence_300ms.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anullsrc=channel_layout=mono:sample_rate=24000",
        "-t", "0.30", "-q:a", "9", "-acodec", "libmp3lame",
        str(silence_file)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # 1. Vitrine de Vozes
    print("\n[Vitrine Chirp 3 HD] Gerando amostras individuais...")
    vitrine_file = OUTPUT_DIR / "00_Vitrine_Todas_as_Vozes_Chirp3HD.mp3"
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        lines = []
        for idx, (vname, txt) in enumerate(AMOSTRAS):
            short = vname.split("-")[-1]
            print(f"   Voz: {short}")
            raw = sintetizar(client, txt, vname)
            cfile = tmp_path / f"amostra_{idx:02d}.mp3"
            cfile.write_bytes(raw)
            lines.append(f"file '{cfile.as_posix()}'")
            lines.append(f"file '{silence_file.as_posix()}'")

        concat = tmp_path / "concat.txt"
        concat.write_text("\n".join(lines), encoding="utf-8")
        subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c:a", "libmp3lame", "-b:a", "192k", str(vitrine_file)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"[OK] Vitrine Chirp 3 HD gerada: {vitrine_file.name}")

    # 2. Debate com Aoede e Puck
    print("\n[Debate] Gerando versão com Aoede e Puck (Voz mais descontraída)...")
    debate_puck = OUTPUT_DIR / "Debate_2_1_Chirp3HD_Aoede_e_Puck.mp3"
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        lines = []
        for idx, (spk, txt) in enumerate(DIALOGO_2_1):
            vname = "pt-BR-Chirp3-HD-Aoede" if spk == "Aoede" else "pt-BR-Chirp3-HD-Puck"
            raw = sintetizar(client, txt, vname)
            cfile = tmp_path / f"turn_{idx:02d}.mp3"
            cfile.write_bytes(raw)
            lines.append(f"file '{cfile.as_posix()}'")
            lines.append(f"file '{silence_file.as_posix()}'")

        concat = tmp_path / "concat.txt"
        concat.write_text("\n".join(lines), encoding="utf-8")
        subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c:a", "libmp3lame", "-b:a", "192k", str(debate_puck)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"[OK] Debate Aoede e Puck gerado: {debate_puck.name}")

    silence_file.unlink(missing_ok=True)
    print("\n[Sucesso] Tudo gerado com sucesso!")


if __name__ == "__main__":
    main()
