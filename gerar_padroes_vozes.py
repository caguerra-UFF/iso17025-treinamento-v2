"""
Gera comparativo de diferentes padrões e combinações de vozes para o debate do Item 2.1,
além de uma vitrine de apresentação individual de cada voz.
"""
import asyncio
import os
import sys
import subprocess
import tempfile
from pathlib import Path

# UTF-8 encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

LOCALDUB_BACKEND = Path(r"C:\Users\NOVO OFFLINE\.openclaw\workspace\LocalDub-upstream\backend")
if str(LOCALDUB_BACKEND) not in sys.path:
    sys.path.append(str(LOCALDUB_BACKEND))

import edge_tts

OUTPUT_DIR = Path(r"F:\Transcricoes_Consolidadas\Podcasts_Tematicos\Comparativo_Vozes")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Texto padrão do Item 2.1 para comparação justa
DIALOGO_2_1 = [
    ("H1", "Vamos começar falando de uma das maiores dores de cabeça nos laboratórios: o controle de calibração e manutenção. O instrutor do curso trouxe uma visão bem pragmática sobre isso no item 2.1."),
    ("H2", "Excelente! E convenhamos, o pessoal adora complicar isso, né? Já vi laboratório mantendo três controles completamente separados pra mesma máquina. O que o instrutor defendeu aqui?"),
    ("H1", "Ele foi direto ao ponto: não precisa inventar moda. Calibração, verificação intermediária e manutenção preventiva podem estar integradas no mesmo plano geral. O procedimento define as regras e a periodicidade, mas o plano prático só precisa mostrar claramente quando a ação está prevista pra acontecer."),
    ("H2", "Faz muito sentido. Mas me diz uma coisa: e o avaliador da Cgcre, aceita isso numa boa? A norma não exige formulários separados?"),
    ("H1", "Aceita sim, com ressalva! Os requisitos 6.4.3 e 6.4.13 da ISO 17025 exigem que o plano exista e esteja sob controle rastreável. A força da evidência tá na rastreabilidade e no cumprimento das datas, e não na quantidade ou na complexidade de planilhas que você inventou."),
    ("H2", "Perfeito! Menos burocracia de gaveta e mais controle real do que realmente precisa ser feito no mês.")
]

# Vitrine de apresentação individual
APRESENTACOES = [
    ("pt-BR-FranciscaNeural", "+0Hz", "+0%", "Olá! Eu sou a Francisca. Minha voz tem um estilo mais clássico, claro e institucional, ideal para condução técnica e leitura formal."),
    ("pt-BR-AntonioNeural", "+0Hz", "+0%", "Olá! Eu sou o Antonio. Minha voz tem uma presença masculina firme e profissional, muito usada para narração e debates técnicos."),
    ("pt-BR-ThalitaMultilingualNeural", "+0Hz", "+0%", "Oi pessoal, eu sou a Thalita! Minha voz é mais jovem, moderna e conversacional, perfeita para dar uma energia leve e dinâmica ao podcast."),
    ("pt-BR-AntonioNeural", "-15Hz", "+0%", "E eu sou o Antonio configurado com um tom mais grave e encorpado, criando um estilo de locutor experiente de estúdio de rádio."),
    ("pt-BR-FranciscaNeural", "-8Hz", "+0%", "Aqui é a Francisca com um tom ligeiramente mais quente e intimista, soando menos formal e mais próxima do ouvinte.")
]

# Combinações de duplas para o debate
COMBINACOES = [
    {
        "nome": "1_Padrao_Moderno_Thalita_e_AntonioGrave",
        "desc": "Thalita (jovem/dinâmica) + Antonio (tom grave/estúdio)",
        "h1": {"voice": "pt-BR-ThalitaMultilingualNeural", "pitch": "+0Hz"},
        "h2": {"voice": "pt-BR-AntonioNeural", "pitch": "-12Hz"}
    },
    {
        "nome": "2_Dupla_Feminina_Thalita_e_Francisca",
        "desc": "Dupla Feminina: Thalita (curiosa/enérgica) + Francisca (especialista técnica)",
        "h1": {"voice": "pt-BR-ThalitaMultilingualNeural", "pitch": "+0Hz"},
        "h2": {"voice": "pt-BR-FranciscaNeural", "pitch": "+0Hz"}
    },
    {
        "nome": "3_Dupla_Masculina_Dois_Timbres",
        "desc": "Dupla Masculina: Antonio tom leve/ágil + Antonio tom grave/experiente",
        "h1": {"voice": "pt-BR-AntonioNeural", "pitch": "+8Hz"},
        "h2": {"voice": "pt-BR-AntonioNeural", "pitch": "-18Hz"}
    },
    {
        "nome": "4_Classico_Ajustado_FranciscaIntimista_e_Antonio",
        "desc": "Francisca (tom intimista/quente) + Antonio (padrão)",
        "h1": {"voice": "pt-BR-FranciscaNeural", "pitch": "-8Hz"},
        "h2": {"voice": "pt-BR-AntonioNeural", "pitch": "+0Hz"}
    }
]


async def sintetizar_trecho(texto: str, voz: str, pitch: str = "+0Hz", rate: str = "+0%") -> bytes:
    comm = edge_tts.Communicate(texto, voz, pitch=pitch, rate=rate)
    chunks = []
    async for ch in comm.stream():
        if ch["type"] == "audio":
            chunks.append(ch["data"])
    return b"".join(chunks)


async def gerar_vitrine(silence_path: Path):
    print("\n[Vitrine] Gerando áudio de apresentação de cada voz...")
    out_file = OUTPUT_DIR / "00_Vitrine_Apresentacao_de_Cada_Voz.mp3"
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        concat_txt = tmp_path / "concat.txt"
        lines = []

        for idx, (voz, pitch, rate, texto) in enumerate(APRESENTACOES):
            audio = await sintetizar_trecho(texto, voz, pitch=pitch, rate=rate)
            cfile = tmp_path / f"amostra_{idx:02d}.mp3"
            cfile.write_bytes(audio)
            lines.append(f"file '{cfile.as_posix()}'")
            lines.append(f"file '{silence_path.as_posix()}'")

        concat_txt.write_text("\n".join(lines), encoding="utf-8")
        cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_txt),
            "-c:a", "libmp3lame", "-b:a", "192k",
            str(out_file)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"[OK] Vitrine gerada: {out_file.name}")


async def gerar_combinao(combo: dict, silence_path: Path):
    out_file = OUTPUT_DIR / f"Debate_2_1_{combo['nome']}.mp3"
    print(f"\n[Debate] Gerando: {combo['desc']}...")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        concat_txt = tmp_path / "concat.txt"
        lines = []

        for idx, (speaker, texto) in enumerate(DIALOGO_2_1):
            cfg = combo["h1"] if speaker == "H1" else combo["h2"]
            audio = await sintetizar_trecho(texto, cfg["voice"], pitch=cfg["pitch"])
            cfile = tmp_path / f"turn_{idx:02d}_{speaker}.mp3"
            cfile.write_bytes(audio)
            lines.append(f"file '{cfile.as_posix()}'")
            lines.append(f"file '{silence_path.as_posix()}'")

        concat_txt.write_text("\n".join(lines), encoding="utf-8")
        cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_txt),
            "-c:a", "libmp3lame", "-b:a", "192k",
            str(out_file)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"[OK] Gerado: {out_file.name}")


async def main():
    print("==========================================================")
    print(" GERANDO COMPARATIVO DE PADRÕES DE VOZES")
    print("==========================================================")

    silence_file = OUTPUT_DIR / "_silence_300ms.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anullsrc=channel_layout=mono:sample_rate=24000",
        "-t", "0.30", "-q:a", "9", "-acodec", "libmp3lame",
        str(silence_file)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # 1. Vitrine com cada voz se apresentando individualmente
    await gerar_vitrine(silence_file)

    # 2. O mesmo debate do item 2.1 em 4 estilos diferentes
    for combo in COMBINACOES:
        await gerar_combinao(combo, silence_file)

    silence_file.unlink(missing_ok=True)
    print("\n[Sucesso] Todos os comparativos de vozes foram gerados!")
    print(f"Pasta: {OUTPUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
