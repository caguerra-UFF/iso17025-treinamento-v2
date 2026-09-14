"""
Gera os episódios da Seção 7 (Itens 7.1, 7.2, 7.3 e 7.4 da Parte 1)
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

EPISODIOS_SEC7 = [
    {
        "id": "7.1",
        "filename": "Podcast_Item_7_1_Conceito_Pratico_Rastreabilidade.mp3",
        "title": "Item 7.1 - Conceito Prático de Rastreabilidade Metrológica",
        "dialogue": [
            ("Thalita", "Francisca, chegamos ao Capítulo 7, um dos pilares da ISO 17025: a rastreabilidade metrológica. O instrutor resumiu isso de forma muito elegante: rastreabilidade é o que garante que um metro aqui seja exatamente um metro no Japão ou na Alemanha."),
            ("Francisca", "Essa definição é brilhante na sua simplicidade, Thalita! Tecnicamente, o requisito 6.5.1 define a rastreabilidade como uma cadeia ininterrupta e documentada de calibrações, onde cada elo contribui com a sua parcela de incerteza até chegar nos padrões do Sistema Internacional."),
            ("Thalita", "E por que isso é tão crucial pro cliente do laboratório?"),
            ("Francisca", "Porque sem rastreabilidade, os números não têm comparabilidade no tempo e no espaço! Um laudo emitido em São Paulo tem que ter o mesmo valor metrológico de um laudo emitido em Londres. É a rastreabilidade que dá validade jurídica e técnica ao comércio global e aos ensaios."),
            ("Thalita", "Perfeito. Uma ponte inquebrável entre a bancada do laboratório e a física internacional.")
        ]
    },
    {
        "id": "7.2",
        "filename": "Podcast_Item_7_2_Toda_Calibracao_em_Laboratorio_Acreditado.mp3",
        "title": "Item 7.2 - Toda Calibração Tem que Ser em Laboratório Acreditado?",
        "dialogue": [
            ("Thalita", "Agora, Francisca, no item 7.2 vem uma polêmica gigantesca: o instrutor cravou que 'toda calibração tem que ser obrigatoriamente feita por um laboratório acreditado'. Isso é verdade ao pé da letra da ISO 17025?"),
            ("Francisca", "Cuidado com essa afirmação, Thalita! A nossa equipe técnica marcou esse trecho com Atenção e Correção. A ISO 17025, no requisito 6.5.2, diz que a calibração deve ser provida por um 'laboratório competente', e não exige exclusivamente a palavra 'acreditado' no texto internacional."),
            ("Thalita", "Mas espera aí: e os institutos nacionais de metrologia, tipo o Inmetro no Brasil ou o NIST nos Estados Unidos?"),
            ("Francisca", "Exatamente! O Inmetro e o NIST não são acreditados por ninguém, porque eles são os próprios guardiões dos padrões primários nacionais! Além disso, se não houver laboratório acreditado para aquele serviço no país, existem caminhos documentados para demonstrar a competência do prestador. Dizer que toda calibração sem exceção precisa ser acreditada simplifica demais a regra."),
            ("Thalita", "Excelente esclarecimento! Acreditação é a rota preferencial e mais fácil, mas a norma internacional não fecha as portas para outras vias legítimas de competência.")
        ]
    },
    {
        "id": "7.3",
        "filename": "Podcast_Item_7_3_Sistema_Internacional_e_Excecoes.mp3",
        "title": "Item 7.3 - Sistema Internacional de Unidades e Exceções",
        "dialogue": [
            ("Thalita", "E quando chegamos no item 7.3, o que acontece quando tecnicamente não é possível rastrear o ensaio ao Sistema Internacional de Unidades, o famoso SI?"),
            ("Francisca", "A própria norma já previu isso, Thalita! O requisito 6.5.3 traz as exceções. Existem ensaios, principalmente nas áreas química, biológica ou de propriedades ópticas e dureza, onde você não consegue ligar o resultado diretamente ao metro, quilograma ou segundo."),
            ("Thalita", "E qual é o caminho aceito pela ISO 17025 nesses casos especiais?"),
            ("Francisca", "A norma permite demonstrar a rastreabilidade através de Materiais de Referência Certificados de produtores competentes, ou pelo uso de procedimentos de medição de consenso e métodos normalizados internacionalmente aceitos. O importante é que a referência seja reconhecida e que você comprove o controle por comparações."),
            ("Thalita", "Muito bom saber! A norma tem flexibilidade técnica para áreas onde o SI puro não se aplica.")
        ]
    },
    {
        "id": "7.4",
        "filename": "Podcast_Item_7_4_Reconhecimento_Internacional_e_NIT_DICLA_030.mp3",
        "title": "Item 7.4 - Reconhecimento Internacional, ILAC e NIT-DICLA-030",
        "dialogue": [
            ("Thalita", "E pra fechar o capítulo, no item 7.4, o treinamento citou a famosa NIT-DICLA-030 da Cgcre e os acordos da ILAC. Como o laboratório brasileiro deve se posicionar diante desse documento?"),
            ("Francisca", "Esse é um ponto fundamental de atenção, Thalita! Para os laboratórios acreditados pela Cgcre no Brasil, a NIT-DICLA-030 é a política mandatória de rastreabilidade. Ela estabelece a hierarquia: primeiro laboratórios da RBC ou institutos signatários do acordo ILAC. E detalha exatamente o que fazer quando não houver prestador disponível."),
            ("Thalita", "Então, antes de bater o martelo no procedimento interno de calibração, o gestor da qualidade precisa consultar essa NIT?"),
            ("Francisca", "Obrigatório! Baixe a versão vigente da NIT-DICLA-030 e monte uma matriz interna: para cada tipo de equipamento ou padrão, qual é a evidência de competência aceita e qual a justificativa se precisar usar uma exceção. Isso blinda a acreditação do laboratório."),
            ("Thalita", "Sensacional, Francisca! Uma verdadeira aula sobre como transformar política de acreditação em segurança prática.")
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
    print(f"\n[Seção 7 - Thalita & Francisca] Processando: {ep['title']}...")

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
    print(" GERANDO SEÇÃO 7 (ITENS 7.1 A 7.4) - THALITA & FRANCISCA")
    print("==========================================================")

    silence_file = OUTPUT_DIR / "_silence_180ms.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anullsrc=channel_layout=mono:sample_rate=24000",
        "-t", "0.18", "-q:a", "9", "-acodec", "libmp3lame",
        str(silence_file)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    gerados = []
    for ep in EPISODIOS_SEC7:
        caminho = await gerar_episodio(ep, silence_file)
        gerados.append(caminho)

    # Gera também o episódio completo com a Seção 7 unificada
    print("\n[Capítulo 7 Completo] Unindo os itens 7.1 a 7.4 em um único áudio...")
    ep_completo = OUTPUT_DIR / "Podcast_Capitulo_7_Itens_7_1_a_7_4_Completo_Thalita_e_Francisca.mp3"
    silence_1s = OUTPUT_DIR / "_silence_1s.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anullsrc=channel_layout=mono:sample_rate=24000",
        "-t", "1.0", "-q:a", "9", "-acodec", "libmp3lame",
        str(silence_1s)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        linhas_full = []
        for g in gerados:
            linhas_full.append(f"file '{g.as_posix()}'")
            linhas_full.append(f"file '{silence_1s.as_posix()}'")
        f.write("\n".join(linhas_full))
        concat_full = f.name

    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_full,
        "-c:a", "libmp3lame", "-b:a", "192k",
        str(ep_completo)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    try:
        silence_file.unlink(missing_ok=True)
        silence_1s.unlink(missing_ok=True)
        os.remove(concat_full)
    except Exception:
        pass

    print(f"\n[Sucesso] Todos os episódios da Seção 7 foram salvos em: {OUTPUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
