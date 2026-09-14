"""
Gera os episódios da Seção 4 (Itens 4.1, 4.2 e 4.3 da Parte 1)
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

EPISODIOS_SEC4 = [
    {
        "id": "4.1",
        "filename": "Podcast_Item_4_1_Identificacao_da_Situacao_do_Equipamento.mp3",
        "title": "Item 4.1 - Identificação da Situação do Equipamento",
        "dialogue": [
            ("Thalita", "Francisca, vamos entrar no Capítulo 4, que fala sobre como identificar a situação dos equipamentos. No dia a dia, todo mundo pensa logo em colar uma etiqueta física em cada item. Mas e quando o equipamento é minúsculo, tipo uma vidraria ou sensores pequenos de campo?"),
            ("Francisca", "Essa é uma dúvida clássica de bancada, Thalita! Os requisitos 6.4.8 e 6.4.9 da norma exigem que o usuário identifique prontamente se o equipamento está calibrado ou se está fora de serviço. Mas a norma é funcional: ela não obriga você a colar uma etiqueta numa micropipeta minúscula se isso for inviável."),
            ("Thalita", "E qual foi a saída prática apresentada no treinamento?"),
            ("Francisca", "O instrutor confirmou: a identificação pode estar na porta do armário, num mapa da bancada ou na tampa da maleta de campo! Desde que haja um vínculo inequívoco entre o item e a lista de controle, o requisito está cem por cento atendido. E o que estiver quebrado ou fora de serviço precisa estar segregado ou claramente sinalizado."),
            ("Thalita", "Muito prático. O fundamental é que ninguém pegue um equipamento duvidoso por engano.")
        ]
    },
    {
        "id": "4.2",
        "filename": "Podcast_Item_4_2_Data_da_Proxima_Calibracao_na_Etiqueta.mp3",
        "title": "Item 4.2 - Próxima Calibração e Data Exata na Etiqueta",
        "dialogue": [
            ("Thalita", "Agora, Francisca, no item 4.2 tem uma polêmica técnica bem interessante. O instrutor afirmou que a etiqueta precisa ter obrigatoriamente o dia exato da próxima calibração, e não apenas o mês e o ano. A norma é tão rigorosa assim?"),
            ("Francisca", "Olha que ponto excelente, Thalita! A nossa análise técnica marcou esse trecho com Atenção e Correção. A ISO 17025 exige que o laboratório mantenha registros com as datas de calibração e a data prevista ou intervalo. Mas ela não determina que a etiqueta física tenha o dia cravado!"),
            ("Thalita", "Quer dizer que se a minha etiqueta marcar apenas 'Validade: setembro de 2027', eu não tomo não conformidade?"),
            ("Francisca", "Não toma, desde que o seu procedimento interno e o seu sistema informatizado definam claramente a regra, por exemplo, que a validade vai até o último dia daquele mês. O auditor quer ver controle e clareza, mas não pode inventar exigência que não está escrita no texto da norma."),
            ("Thalita", "Que esclarecimento valioso! Saber a fronteira entre o que a norma pede e o que é rigor excessivo faz toda a diferença.")
        ]
    },
    {
        "id": "4.3",
        "filename": "Podcast_Item_4_3_Equipamento_Fora_do_Escopo.mp3",
        "title": "Item 4.3 - Equipamento Fora do Escopo de Acreditação",
        "dialogue": [
            ("Thalita", "E pra fechar o capítulo, no item 4.3, o que fazer com aqueles aparelhos que ficam no laboratório, mas que são usados só pra pesquisa ou ensaios fora do escopo acreditado da Cgcre?"),
            ("Francisca", "A recomendação do instrutor foi cirúrgica: identifique claramente esses aparelhos com uma etiqueta de 'Fora do Escopo'. Tecnicamente, a ISO 17025 não tem uma cláusula exigindo essa etiqueta específica, mas na prática é uma das melhores orientações preventivas que existem."),
            ("Thalita", "Porque se o avaliador entrar no laboratório e vir duas balanças iguais lado a lado, ele vai pedir o certificado das duas, certo?"),
            ("Francisca", "Exatamente! Se não tiver placa ou identificação, gera dúvida na auditoria e risco real de um operador desavisado usar a máquina errada num ensaio acreditado. Identificar o que está fora do escopo protege a rotina e evita questionamentos desnecessários."),
            ("Thalita", "Perfeito, Francisca! Boa prática que economiza dor de cabeça na hora H.")
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
    print(f"\n[Seção 4 - Thalita & Francisca] Processando: {ep['title']}...")

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
    print(" GERANDO SEÇÃO 4 (ITENS 4.1, 4.2 E 4.3) - THALITA & FRANCISCA")
    print("==========================================================")

    silence_file = OUTPUT_DIR / "_silence_180ms.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anullsrc=channel_layout=mono:sample_rate=24000",
        "-t", "0.18", "-q:a", "9", "-acodec", "libmp3lame",
        str(silence_file)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    gerados = []
    for ep in EPISODIOS_SEC4:
        caminho = await gerar_episodio(ep, silence_file)
        gerados.append(caminho)

    # Gera também o episódio completo com a Seção 4 unificada
    print("\n[Capítulo 4 Completo] Unindo os itens 4.1 a 4.3 em um único áudio...")
    ep_completo = OUTPUT_DIR / "Podcast_Capitulo_4_Itens_4_1_a_4_3_Completo_Thalita_e_Francisca.mp3"
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

    print(f"\n[Sucesso] Todos os episódios da Seção 4 foram salvos em: {OUTPUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
