"""
Gera os episódios da Seção 3 (Itens 3.1, 3.2 e 3.3 da Parte 1)
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

EPISODIOS_SEC3 = [
    {
        "id": "3.1",
        "filename": "Podcast_Item_3_1_Verificacao_Antes_do_Uso.mp3",
        "title": "Item 3.1 - Verificação Antes da Colocação em Serviço",
        "dialogue": [
            ("Thalita", "Francisca, entrando agora no Capítulo 3 do treinamento, tem uma frase que o instrutor repetiu várias vezes: ter um certificado de calibração na mão não significa que o equipamento está pronto pra ser usado. Como assim?"),
            ("Francisca", "Essa é uma das maiores pegadinhas em auditoria, Thalita! O requisito 6.4.4 da ISO 17025 exige que o laboratório verifique a conformidade antes de colocar o equipamento em serviço. Ou seja, você não pode só receber a balança calibrada e já sair pesando. Você precisa fazer a análise crítica daquele certificado!"),
            ("Thalita", "E o que exatamente a gente tem que checar nessa análise crítica antes de liberar a máquina pra bancada?"),
            ("Francisca", "Você precisa confrontar os dados com o seu método: conferir se os pontos calibrados cobrem a sua faixa real de trabalho, se o erro somado com a incerteza atende ao critério de tolerância interna e se não há nenhuma observação restritiva. Só depois disso você emite o registro formal: 'Apto para uso na faixa X'."),
            ("Thalita", "Sensacional. Se o auditor perguntar 'onde está a evidência de que esse equipamento foi aprovado pra essa rotina?', você mostra a análise crítica e não apenas o papel do laboratório externo.")
        ]
    },
    {
        "id": "3.2",
        "filename": "Podcast_Item_3_2_Exatidao_Precisao_e_Incerteza.mp3",
        "title": "Item 3.2 - Exatidão, Precisão e Incerteza na Decisão de Uso",
        "dialogue": [
            ("Thalita", "No item 3.2, o instrutor usou um exemplo bem prático: se a tolerância do meu método é de mais ou menos um, e a incerteza do meu equipamento já é de um, esse instrumento simplesmente não serve pro meu ensaio!"),
            ("Francisca", "Perfeito, Thalita! A decisão de adequação ao uso, segundo o requisito 6.4.5, depende diretamente da exatidão e da incerteza necessárias pro resultado ser válido. Não dá pra comprar equipamento olhando só a propaganda ou o catálogo do fabricante."),
            ("Thalita", "E por onde o laboratório deve começar essa avaliação técnica?"),
            ("Francisca", "Pelo processo! Você precisa se perguntar: qual é a tolerância máxima permitida pelo meu método? Qual a incerteza que esse instrumento pode contribuir sem estourar o orçamento global de incerteza? Qual a resolução necessária? É o método que dita a máquina, e nunca o contrário."),
            ("Thalita", "Faz total sentido. Olhar o alvo primeiro para depois escolher a ferramenta certa.")
        ]
    },
    {
        "id": "3.3",
        "filename": "Podcast_Item_3_3_Criterio_de_Aceitacao_Antes_da_Compra.mp3",
        "title": "Item 3.3 - Critério de Aceitação Deve Existir Antes da Compra ou Contratação",
        "dialogue": [
            ("Thalita", "E fechando esse capítulo, no item 3.3, vem a regra de ouro das aquisições: o critério de aceitação precisa nascer antes da compra ou da contratação do serviço externo."),
            ("Francisca", "Exatamente, Thalita! Os requisitos 6.6.2 e 6.6.3 da norma tratam de produtos e serviços providos externamente. Se você vai contratar a calibração de um termômetro, por exemplo, você precisa definir no pedido os pontos exatos que você quer calibrar e a incerteza máxima que você aceita receber."),
            ("Thalita", "Porque se você não especificar isso antes no termo de referência, o prestador calibra nos pontos padrão dele, te entrega um documento tecnicamente perfeito, mas que não serve pra nada no seu ensaio!"),
            ("Francisca", "Falou tudo! Você gasta dinheiro, recebe um certificado válido, mas o equipamento fica inutilizável porque não atende ao seu método. Definir o critério de aceitação antes da contratação protege o laboratório técnica e financeiramente."),
            ("Thalita", "Excelente lição. Planejamento na contratação evita não conformidade grave na auditoria.")
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
    print(f"\n[Seção 3 - Thalita & Francisca] Processando: {ep['title']}...")

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
    print(" GERANDO SEÇÃO 3 (ITENS 3.1, 3.2 E 3.3) - THALITA & FRANCISCA")
    print("==========================================================")

    silence_file = OUTPUT_DIR / "_silence_180ms.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anullsrc=channel_layout=mono:sample_rate=24000",
        "-t", "0.18", "-q:a", "9", "-acodec", "libmp3lame",
        str(silence_file)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    gerados = []
    for ep in EPISODIOS_SEC3:
        caminho = await gerar_episodio(ep, silence_file)
        gerados.append(caminho)

    # Gera também o episódio completo com a Seção 3 unificada
    print("\n[Capítulo 3 Completo] Unindo os itens 3.1 a 3.3 em um único áudio...")
    ep_completo = OUTPUT_DIR / "Podcast_Capitulo_3_Itens_3_1_a_3_3_Completo_Thalita_e_Francisca.mp3"
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

    print(f"\n[Sucesso] Todos os episódios da Seção 3 foram salvos em: {OUTPUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
