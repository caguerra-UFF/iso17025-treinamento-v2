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

EPISODIOS_SEC9 = [
    {
        "id": "9.1",
        "filename": "Podcast_Item_9_1_O_Que_Observar_no_Relatorio_de_Manutencao.mp3",
        "title": "Item 9.1 - Análise Crítica de Relatório de Manutenção: O Que Observar",
        "dialogue": [
            ("Thalita", "Francisca, chegamos ao Capítulo 9, analisando relatórios de manutenção preventiva. O instrutor usou o exemplo clássico de um espectrofotômetro e deu um puxão de orelha: muita gente só olha a assinatura da assistência técnica e arquiva a folha! O que a ISO realmente espera que o laboratório faça?"),
            ("Francisca", "Esse é um erro crônico, Thalita! A ISO 17025 exige nos requisitos 6.4.4 e 6.6.2 que o laboratório avalie criticamente o serviço prestado antes de recolocar o equipamento em rotina. Não basta o carimbo de manutenção realizada!"),
            ("Thalita", "E qual é o detalhe técnico essencial que o analista tem que conferir no relatório do espectrofotômetro?"),
            ("Francisca", "Você precisa checar se as verificações de comprimento de onda, ruído e linearidade feitas pelo técnico batem exatamente com as faixas que o seu laboratório utiliza! Se a sua rotina mede no ultravioleta a 254 nanômetros, mas o técnico só testou lâmpada no visível a 500 nanômetros, aquele relatório não garante nada pro seu ensaio."),
            ("Thalita", "Que visão cirúrgica! O serviço externo tem que ser confrontado com o uso real do laboratório antes de qualquer liberação.")
        ]
    },
    {
        "id": "9.2",
        "filename": "Podcast_Item_9_2_Frequencia_Anual_Manutencao_Espectrofotometro.mp3",
        "title": "Item 9.2 - Frequência Anual de Manutenção: Regra ou Gestão de Risco?",
        "dialogue": [
            ("Thalita", "No Item 9.2, Francisca, o curso comentou que a manutenção preventiva de espectrofotômetros é normalmente anual. Mas vem a dúvida de sempre: a ISO 17025 exige que todo equipamento passe por preventiva uma vez por ano?"),
            ("Francisca", "De jeito nenhum, Thalita! A classificação técnica dessa fala é Orientação Técnica e Boa Prática. A ISO não estabelece nenhum intervalo universal fixo. O prazo anual é um padrão consagrado de mercado recomendado por fabricantes, mas a periodicidade real tem que nascer da gestão de risco do próprio laboratório."),
            ("Thalita", "E quais fatores determinam se esse prazo anual deve ser mantido, encurtado ou até ampliado?"),
            ("Francisca", "O histórico de falhas, a intensidade de uso, as condições ambientais da sala e a estabilidade das checagens intermediárias! Se um espectrofotômetro trabalha em três turnos num ambiente agressivo e quebra com frequência, manutenção anual é insuficiente. Já para um aparelho com checagens diárias impecáveis e sem deriva, o histórico fundamenta a frequência adotada."),
            ("Thalita", "Sensacional! Nada de prazos cegos; a periodicidade deve ser respaldada por dados históricos e risco metrológico.")
        ]
    },
    {
        "id": "9.3",
        "filename": "Podcast_Item_9_3_Documentos_Orientativos_Cgcre_DOC_vs_NIT.mp3",
        "title": "Item 9.3 - Documentos da Cgcre: Diferença Prática entre DOC e NIT",
        "dialogue": [
            ("Thalita", "E pra fechar o Capítulo 9, o Item 9.3 trouxe uma distinção fundamental do sistema Cgcre: a diferença entre um DOC de orientação técnica e uma NIT. Qual é o peso normativo de cada um para o laboratório acreditado?"),
            ("Francisca", "Essa é uma dúvida clássica em auditoria, Thalita! A NIT, Norma Inmetro Técnica, é um documento mandatório. Descumprir uma diretriz de uma NIT gera não conformidade formal na auditoria da Cgcre. Já o DOC é um documento orientativo, que apresenta recomendações e boas práticas técnicas para checagens de balanças, espectrofotômetros e outros instrumentos."),
            ("Thalita", "Mas tem uma pegadinha aí, não tem Francisca? O laboratório pode ignorar o DOC completamente?"),
            ("Francisca", "Muito cuidado: se o laboratório copiar as orientações do DOC para dentro do seu Procedimento Operacional Padrão interno, aquilo passa a ser autocompromisso obrigatório! Além disso, a Cgcre atualiza seus documentos com frequência. O laboratório deve sempre verificar a versão em vigor no portal do Inmetro antes de desenhar seus protocolos de checagem."),
            ("Thalita", "Perfeito, Francisca! Conhecer a hierarquia dos documentos regulatórios evita surpresas desagradáveis nas avaliações.")
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
    print(f"\n[Seção 9 - Thalita & Francisca] Processando: {ep['title']}...")
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
    print(" GERANDO SEÇÃO 9 (ITENS 9.1 A 9.3) - THALITA & FRANCISCA")
    print("==========================================================")

    silence_file = OUTPUT_DIR / "_silence_180ms.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anullsrc=channel_layout=mono:sample_rate=24000",
        "-t", "0.18", "-q:a", "9", "-acodec", "libmp3lame",
        str(silence_file)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    gerados = []
    for ep in EPISODIOS_SEC9:
        caminho = await gerar_episodio(ep, silence_file)
        gerados.append(caminho)

    print("\n[Capítulo 9 Completo] Unindo os itens 9.1 a 9.3 em um único áudio...")
    ep_completo = OUTPUT_DIR / "Podcast_Capitulo_9_Itens_9_1_a_9_3_Completo_Thalita_e_Francisca.mp3"
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

    print(f"\n[Sucesso] Todos os episódios da Seção 9 foram salvos em: {OUTPUT_DIR}")

if __name__ == "__main__":
    asyncio.run(main())