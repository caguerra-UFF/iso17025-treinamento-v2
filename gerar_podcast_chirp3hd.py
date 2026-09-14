"""
Gerador de Podcast usando Google Cloud Text-to-Speech com o modelo Chirp 3: HD.
Gera o debate do Item 2.1 usando as vozes generativas Aoede e Charon (e Kore + Fenrir).
"""
import os
import sys
import subprocess
import tempfile
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.cloud import texttospeech

# UTF-8 encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

OUTPUT_DIR = Path(r"F:\Transcricoes_Consolidadas\Podcasts_Tematicos\Chirp3HD")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TOKEN_FILE = Path(r"F:\Transcricoes_Consolidadas\token_gcloud.json")

# Roteiro do Item 2.1
DIALOGO_2_1 = [
    ("H1", "Lucas, vamos começar falando de uma das maiores dores de cabeça nos laboratórios: o controle de calibração e manutenção. O instrutor do curso trouxe uma visão bem pragmática sobre isso no item 2.1."),
    ("H2", "Excelente, Mariana! E convenhamos, o pessoal adora complicar isso, né? Já vi laboratório mantendo três controles completamente separados pra mesma máquina. O que o instrutor defendeu aqui?"),
    ("H1", "Ele foi direto ao ponto: não precisa inventar moda. Calibração, verificação intermediária e manutenção preventiva podem estar integradas no mesmo plano geral. O procedimento define as regras e a periodicidade, mas o plano prático só precisa mostrar claramente quando a ação está prevista pra acontecer."),
    ("H2", "Faz muito sentido. Mas me diz uma coisa: e o avaliador da Cgcre, aceita isso numa boa? A norma não exige formulários separados?"),
    ("H1", "Aceita sim, com ressalva! Os requisitos 6.4.3 e 6.4.13 da ISO 17025 exigem que o plano exista e esteja sob controle rastreável. A força da evidência tá na rastreabilidade e no cumprimento das datas, e não na quantidade ou na complexidade de planilhas que você inventou."),
    ("H2", "Perfeito! Menos burocracia de gaveta e mais controle real do que realmente precisa ser feito no mês.")
]

CONFIGURACOES = [
    {
        "nome": "Debate_2_1_Chirp3HD_Aoede_e_Charon.mp3",
        "desc": "Dupla Chirp 3 HD: Aoede (Feminina) + Charon (Masculina)",
        "h1_voice": "pt-BR-Chirp3-HD-Aoede",
        "h2_voice": "pt-BR-Chirp3-HD-Charon"
    },
    {
        "nome": "Debate_2_1_Chirp3HD_Kore_e_Fenrir.mp3",
        "desc": "Dupla Chirp 3 HD: Kore (Feminina) + Fenrir (Masculina)",
        "h1_voice": "pt-BR-Chirp3-HD-Kore",
        "h2_voice": "pt-BR-Chirp3-HD-Fenrir"
    }
]


def sintetizar_chirp(client: texttospeech.TextToSpeechClient, text: str, voice_name: str) -> bytes:
    s_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code="pt-BR", name=voice_name)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=s_input, voice=voice, audio_config=audio_config)
    return response.audio_content


def gerar_debate(client: texttospeech.TextToSpeechClient, config: dict, silence_path: Path):
    out_file = OUTPUT_DIR / config["nome"]
    print(f"\n[Chirp 3 HD] Processando: {config['desc']}...")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        concat_txt = tmp_path / "concat.txt"
        lines = []

        for idx, (speaker, text) in enumerate(DIALOGO_2_1):
            voice_name = config["h1_voice"] if speaker == "H1" else config["h2_voice"]
            print(f"   [{speaker} -> {voice_name.split('-')[-1]}]: \"{text[:55]}...\"")
            audio_bytes = sintetizar_chirp(client, text, voice_name)
            chunk_file = tmp_path / f"turn_{idx:02d}.mp3"
            chunk_file.write_bytes(audio_bytes)

            lines.append(f"file '{chunk_file.as_posix()}'")
            lines.append(f"file '{silence_path.as_posix()}'")

        concat_txt.write_text("\n".join(lines), encoding="utf-8")

        cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_txt),
            "-c:a", "libmp3lame", "-b:a", "192k",
            str(out_file)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    print(f"[OK] Gerado com sucesso: {out_file.name} ({out_file.stat().st_size // 1024} KB)")
    return out_file


def main():
    print("==========================================================")
    print(" INICIANDO TESTE DO GOOGLE CHIRP 3: HD (PT-BR)")
    print("==========================================================")

    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE))
    client = texttospeech.TextToSpeechClient(credentials=creds)

    silence_file = OUTPUT_DIR / "_silence_250ms.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anullsrc=channel_layout=mono:sample_rate=24000",
        "-t", "0.25", "-q:a", "9", "-acodec", "libmp3lame",
        str(silence_file)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    for cfg in CONFIGURACOES:
        gerar_debate(client, cfg, silence_file)

    silence_file.unlink(missing_ok=True)
    print("\n[Sucesso] Todos os áudios do Chirp 3 HD foram gerados com sucesso!")
    print(f"Pasta de destino: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
