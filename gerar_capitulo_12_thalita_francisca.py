# -*- coding: utf-8 -*-
import asyncio
import os
import sys
import subprocess
import tempfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

import edge_tts

OUTPUT_DIR = Path(r"F:\Transcricoes_Consolidadas\Podcasts_Tematicos\Thalita_e_Francisca")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

VOZ_THALITA = "pt-BR-ThalitaMultilingualNeural"
VOZ_FRANCISCA = "pt-BR-FranciscaNeural"

EPISODIO_SEC12 = {
    "filename": "Podcast_Capitulo_12_Mitos_Excessos_e_Fatos_ISO17025.mp3",
    "title": "Capítulo 12 Especial - Guia Anti-Pegadinhas: Mitos, Excessos e o que NÃO Está na ISO 17025",
    "dialogue": [
        ("Thalita", "Francisca, para fechar com chave de ouro as discussões conceituais do primeiro dia de treinamento, chegamos à seção mais aguardada de todas: a tabela de mitos, excessos e pegadinhas! Aquelas regras que todo mundo repete nos corredores dos laboratórios como se fossem a Bíblia da ISO 17025, mas que na verdade não estão escritas na norma!"),
        ("Francisca", "Essa seção é um verdadeiro divisor de águas entre quem apenas decora frases de efeito e quem realmente domina a metrologia e a gestão da ISO 17025, Thalita! O objetivo desse guia é impedir que o laboratório crie burocracias inúteis e autocompromissos perigosos que viram armadilhas nas auditorias."),
        ("Thalita", "Vamos começar pelo mito número um, o mais famoso de todos: Toda calibração tem que ser obrigatoriamente feita em laboratório acreditado pela RBC. Mito ou verdade?"),
        ("Francisca", "Mito na letra estrita da ISO, Thalita! O requisito 6.5.2 da ISO 17025 exige que a calibração seja provida por um laboratório competente. A acreditação pela Cgcre é a forma mais fácil e preferencial de evidenciar competência no Brasil, mas a norma internacional não proíbe institutos primários nacionais como Inmetro ou NIST, nem bloqueia outras comprovações legítimas quando não houver prestador acreditado disponível."),
        ("Thalita", "Mito número dois: A etiqueta física no equipamento precisa ter obrigatoriamente dia, mês e ano da próxima calibração. O que diz a norma?"),
        ("Francisca", "Outro excesso! O requisito 6.4.8 exige que o status do equipamento e o período de validade sejam facilmente identificáveis. Mas a norma aceita intervalo em meses, código de cores ou identificação no sistema informatizado do laboratório. Cravar data completa na etiqueta é uma opção de gestão interna, não uma imposição normativa internacional."),
        ("Thalita", "Mito número três: Se o frasco de material de referência certificado ou reagente venceu, o laboratório pode fazer um ensaio comparativo interno e estender a validade por conta própria."),
        ("Francisca", "Alerta gravíssimo de não conformidade! Nenhum laboratório tem autoridade metrológica para estender validade de MRC por conta própria. Venceu a validade do lote, o material perde o status de certificado para fins de rastreabilidade. Usar material vencido em calibrações e laudos de ensaio é passível de suspensão de escopo!"),
        ("Thalita", "E para fechar, mito número quatro: A manutenção preventiva tem que ser anual e a incerteza do equipamento deve ser sempre um terço da tolerância."),
        ("Francisca", "Duas orientações de mercado que foram tomadas como lei! A ISO não crava prazo de um ano para manutenção preventiva de nenhum instrumento; o intervalo deve nascer da gestão de risco, histórico de falhas e estabilidade do equipamento. E a relação de um terço é uma recomendação consagrada de orçamento de incerteza, mas que depende do risco e da tolerância de cada ensaio específico."),
        ("Thalita", "Que aula monumental, Francisca! Esse episódio vale ouro para qualquer gestor da qualidade e auditor de laboratório. Saber exatamente onde termina a exigência da ISO e onde começa a decisão técnica interna é a maior maturidade que um laboratório pode alcançar!")
    ]
}

async def sintetizar(texto: str, voz: str, rate: str = "+0%", pitch: str = "+0Hz") -> bytes:
    comm = edge_tts.Communicate(texto, voz, rate=rate, pitch=pitch)
    chunks = []
    async for ch in comm.stream():
        if ch["type"] == "audio":
            chunks.append(ch["data"])
    return b"".join(chunks)

async def main():
    print("==========================================================")
    print(" GERANDO CAPÍTULO 12 ESPECIAL (MITOS E VERDADES DA ISO)")
    print("==========================================================")

    out_file = OUTPUT_DIR / EPISODIO_SEC12["filename"]
    silence_file = OUTPUT_DIR / "_silence_180ms.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anullsrc=channel_layout=mono:sample_rate=24000",
        "-t", "0.18", "-q:a", "9", "-acodec", "libmp3lame",
        str(silence_file)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        concat_txt = tmp_path / "concat.txt"
        lines = []
        for idx, (speaker, text) in enumerate(EPISODIO_SEC12["dialogue"]):
            voz = VOZ_THALITA if speaker == "Thalita" else VOZ_FRANCISCA
            print(f"   [{speaker}]: \"{text[:55]}...\"")
            rate = "+14%" if speaker == "Thalita" else "+10%"
            pitch = "+4Hz" if speaker == "Thalita" else "+2Hz"
            audio = await sintetizar(text, voz, rate=rate, pitch=pitch)
            cfile = tmp_path / f"turn_{idx:02d}.mp3"
            cfile.write_bytes(audio)
            lines.append(f"file '{cfile.as_posix()}'")
            lines.append(f"file '{silence_file.as_posix()}'")

        concat_txt.write_text("\n".join(lines), encoding="utf-8")
        cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_txt),
            "-c:a", "libmp3lame", "-b:a", "192k",
            str(out_file)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    try:
        silence_file.unlink(missing_ok=True)
    except Exception:
        pass

    print(f"[OK] Gerado com sucesso: {out_file.name} ({out_file.stat().st_size // 1024} KB)")

if __name__ == "__main__":
    asyncio.run(main())