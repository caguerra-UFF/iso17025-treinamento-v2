"""
Gera o episódio do Capítulo 6 (Item 6.1 da Parte 1)
no padrão oficial aprovado: Thalita & Francisca.
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

OUTPUT_DIR = Path(r"F:\Transcricoes_Consolidadas\Podcasts_Tematicos\Thalita_e_Francisca")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

VOZ_THALITA = "pt-BR-ThalitaMultilingualNeural"
VOZ_FRANCISCA = "pt-BR-FranciscaNeural"

EPISODIOS_SEC6 = [
    {
        "id": "6.1",
        "filename": "Podcast_Item_6_1_Sondas_Consoles_e_Multiparametros.mp3",
        "title": "Item 6.1 - Sondas, Consoles e Combinações de Equipamentos Multiparâmetro",
        "dialogue": [
            ("Thalita", "Francisca, o Capítulo 6 traz uma dor de cabeça que quase todo laboratório com equipamentos multiparâmetro enfrenta: sondas e consoles. Sabe quando você tem aquele medidor de campo e três sondas diferentes? A instrutora sugeriu que toda vez que você for trocar a sonda ou o console, precisa ter essa combinação calibrada junta. Isso procede?"),
            ("Francisca", "Essa é uma discussão técnica de altíssimo nível, Thalita! E o nosso guia técnico marcou esse ponto com Atenção e Correção. A preocupação da instrutora é legítima: o sinal de uma sonda pode ter pequenas variações dependendo do console onde ela é conectada. Mas a ISO 17025 não diz que você é obrigado a calibrar todas as combinações possíveis externamente!"),
            ("Thalita", "Nossa, que alívio! Porque imagina o custo de mandar calibrar cada sonda com cada console disponível no laboratório, vira uma matriz infinita e caríssima!"),
            ("Francisca", "Exatamente! O que os requisitos 6.4.4 e 6.4.11 exigem é que a configuração usada esteja verificada e comprovada como capaz de atender ao desempenho do método. A pergunta que o avaliador da Cgcre vai fazer não é 'onde está o certificado desse par específico?', mas sim: 'como vocês demonstram que essa sonda funciona perfeitamente com esse console?'."),
            ("Thalita", "E qual é a melhor saída técnica pra responder a essa pergunta na auditoria sem gastar rios de dinheiro?"),
            ("Francisca", "O laboratório pode fazer um estudo interno documentado! Pega um material de referência e testa as combinações cruzadas. Se a variação entre os consoles for estatisticamente desprezível frente ao critério de aceitação do método, você documenta e autoriza o intercâmbio livre. Se houver diferença relevante, aí sim você fixa os pares: Sonda 1 só opera com Console 1."),
            ("Thalita", "Brilhante, Francisca! Decisão técnica baseada em dados e evidências internas, e não em regras engessadas que encarecem a operação.")
        ]
    }
]


async def sintetizar(texto: str, voz: str, rate: str = "+0%", pitch: str = "+0Hz") -> bytes:
    comm = edge_tts.Communicate(texto, voz, rate=rate, pitch=pitch)
    chunks = []
    async for ch in comm.stream():
        if ch["type"] == "audio":
            chunks.append(ch["data"])
    return b"".join(chunks)


async def gerar_episodio(ep: dict, silence_path: Path) -> Path:
    out_file = OUTPUT_DIR / ep["filename"]
    print(f"\n[Seção 6 - Thalita & Francisca] Processando: {ep['title']}...")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        concat_txt = tmp_path / "concat.txt"
        lines = []

        for idx, (speaker, text) in enumerate(ep["dialogue"]):
            voz = VOZ_THALITA if speaker == "Thalita" else VOZ_FRANCISCA
            print(f"   [{speaker}]: \"{text[:55]}...\"")
            rate = "+14%" if speaker == "Thalita" else "+10%"
            pitch = "+4Hz" if speaker == "Thalita" else "+2Hz"
            audio = await sintetizar(text, voz, rate=rate, pitch=pitch)
            cfile = tmp_path / f"turn_{idx:02d}.mp3"
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

    print(f"[OK] Gerado com sucesso: {out_file.name} ({out_file.stat().st_size // 1024} KB)")
    return out_file


async def main():
    print("==========================================================")
    print(" GERANDO SEÇÃO 6 (ITEM 6.1) - THALITA & FRANCISCA")
    print("==========================================================")

    silence_file = OUTPUT_DIR / "_silence_180ms.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anullsrc=channel_layout=mono:sample_rate=24000",
        "-t", "0.18", "-q:a", "9", "-acodec", "libmp3lame",
        str(silence_file)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    for ep in EPISODIOS_SEC6:
        await gerar_episodio(ep, silence_file)

    silence_file.unlink(missing_ok=True)
    print(f"\n[Sucesso] Episódio da Seção 6 salvo em: {OUTPUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
