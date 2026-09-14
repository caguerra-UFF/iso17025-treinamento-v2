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

EPISODIO_SEC13 = {
    "filename": "Podcast_Capitulo_13_Plano_de_Implantacao_e_Checklist_Final_Dia_1.mp3",
    "title": "Capítulo 13 - Plano de Implantação Prático e Checklist de Autoavaliação para Auditoria",
    "dialogue": [
        ("Thalita", "Francisca, chegamos ao grande fechamento de todo o Módulo 1 da ISO 17025! Depois de dissecar cada artigo sobre equipamentos, calibrações, manutenções e materiais de referência, o que o laboratório precisa colocar em prática amanhã de manhã na bancada?"),
        ("Francisca", "Essa é a síntese gerencial definitiva, Thalita! O guia técnico estruturou um plano de implantação de alta prioridade em cinco entregáveis fundamentais para blindar a acreditação perante qualquer avaliador da Cgcre."),
        ("Thalita", "Quais são essas cinco entregas obrigatórias de alta prioridade?"),
        ("Francisca", "Primeiro: consolidar o cadastro mestre no sistema ou planilha geral, integrando manutenção, calibração e checagens sem duplicidade. Segundo: implantar a rotina de análise crítica formal de cada certificado de calibração recebido, confrontando erro e incerteza com a tolerância do método."),
        ("Thalita", "E as outras três frentes vitais de metrologia?"),
        ("Francisca", "Terceiro: definir critérios técnicos de aceitação antes de emitir qualquer pedido de compras de insumo ou serviço. Quarto: formalizar em procedimento as checagens intermediárias necessárias, especialmente para aparelhos que vão a campo. E quinto: criar a regra inegociável de controle de frascos de MRC abertos e a segregação física de qualquer reagente vencido!"),
        ("Thalita", "E para o gestor que quer saber se o seu laboratório passaria numa auditoria surpresa amanhã?"),
        ("Francisca", "Basta aplicar o checklist de dez perguntas de autoavaliação do guia: se os equipamentos fora de uso estão fisicamente isolados, se as sondas intercambiáveis têm compatibilidade registrada, e se cada número emitido em laudo está ancorado em uma cadeia ininterrupta de rastreabilidade!"),
        ("Thalita", "Com isso, concluímos com maestria todas as seções do Dia 1! Uma verdadeira formação prática para elevar o nível metrológico de qualquer laboratório. Parabéns pela parceria técnica, Francisca!"),
        ("Francisca", "Obrigada, Thalita! Metrologia com rigor técnico e linguagem clara transforma a rotina do laboratório. Nos encontramos no Dia 2 com a validação de métodos, amostragem e garantia da qualidade!")
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
    print(" GERANDO CAPÍTULO 13 (PLANO DE IMPLANTAÇÃO E CHECKLIST)")
    print("==========================================================")

    out_file = OUTPUT_DIR / EPISODIO_SEC13["filename"]
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
        for idx, (speaker, text) in enumerate(EPISODIO_SEC13["dialogue"]):
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