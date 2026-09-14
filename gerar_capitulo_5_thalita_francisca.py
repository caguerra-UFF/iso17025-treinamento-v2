"""
Gera os episódios da Seção 5 (Itens 5.1, 5.2, 5.3 e 5.4 da Parte 1)
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

EPISODIOS_SEC5 = [
    {
        "id": "5.1",
        "filename": "Podcast_Item_5_1_Quando_a_ISO_Exige_Checagem.mp3",
        "title": "Item 5.1 - Quando a ISO Exige Checagem Intermediária",
        "dialogue": [
            ("Thalita", "Francisca, o Capítulo 5 aborda um tema que gera muita sobrecarga de trabalho desnecessária nos laboratórios: checagens intermediárias. Já vi gente fazendo checagem diária em tudo quanto é máquina por medo de auditor. A ISO 17025 realmente exige isso?"),
            ("Francisca", "Definitivamente não, Thalita! O requisito 6.4.10 da norma é muito claro: as checagens intermediárias são exigidas 'quando forem necessárias' para manter a confiança no desempenho. Essa frase é a chave de tudo!"),
            ("Thalita", "Ou seja, o laboratório não precisa checar tudo todo dia?"),
            ("Francisca", "Exatamente. O laboratório precisa avaliar o risco e justificar tecnicamente: qual equipamento tem risco de deriva? Qual a frequência necessária? Qual o material de controle e o que fazer se a checagem falhar? Criar checagem diária pra equipamento estável só consome reagente, tempo da equipe e gera burocracia inútil."),
            ("Thalita", "Excelente! Checagem baseada em risco real, e não em paranoia de auditoria.")
        ]
    },
    {
        "id": "5.2",
        "filename": "Podcast_Item_5_2_Exemplo_pHmetro_e_Controle.mp3",
        "title": "Item 5.2 - Exemplo de pHmetro: Calibração e Material de Controle",
        "dialogue": [
            ("Thalita", "E no item 5.2, o instrutor deu o exemplo clássico do pHmetro, falando de calibrar em pH quatro, sete e dez, e depois passar uma solução de controle de outro lote pra conferir a curva. Essa regra vale pra todo mundo?"),
            ("Francisca", "Essa é uma excelente estratégia metrológica, Thalita! Usar uma solução de controle independente pra checar se a curva é válida é uma prática consagrada. Mas é importante lembrar: a quantidade de pontos, os valores quatro, sete e dez e a frequência vêm do procedimento do seu método analítico, e não como um mandato universal engessado da ISO."),
            ("Thalita", "Entendi perfeitamente. Se o método do laboratório trabalha só em faixa ácida, ele ajusta a faixa dele conforme a rotina técnica, certo?"),
            ("Francisca", "Com certeza! A norma exige que a calibração e a verificação cubram o seu uso real. Se o controle falhar, aí sim: para tudo, investiga e recalibra antes de soltar laudo."),
            ("Thalita", "Muito claro. Rigor técnico onde precisa, flexibilidade onde a norma permite.")
        ]
    },
    {
        "id": "5.3",
        "filename": "Podcast_Item_5_3_Transporte_ao_Campo_e_Verificacao.mp3",
        "title": "Item 5.3 - Transporte ao Campo e Verificação Após Deslocamento",
        "dialogue": [
            ("Thalita", "Agora, Francisca, no item 5.3 vem uma situação bem delicada: quando o equipamento sai da bancada e vai pro campo. O instrutor recomendou fazer uma checagem antes de sair e outra logo após chegar no local de amostragem. Isso é exigência da norma?"),
            ("Francisca", "Os requisitos 6.4.2 e 6.4.4 cobrem o manuseio e transporte fora das dependências permanentes. Embora a norma não dite a regra exata de checagem a cada quilômetro rodado, o raciocínio de risco do instrutor é perfeito! A viagem de carro introduz trepidação, calor e impacto que podem desajustar um sensor sensível."),
            ("Thalita", "E se você não checa na chegada e mede a amostra com o aparelho descalibrado, você perde o dia inteiro de trabalho em campo!"),
            ("Francisca", "Exato! Você não tem como voltar no tempo pra refazer aquela coleta. Checar com um padrão no destino antes de iniciar a medição garante que o transporte não afetou a resposta do equipamento e blinda os resultados da campanha."),
            ("Thalita", "Sensacional. Prevenção pura pra não invalidar coleta de campo.")
        ]
    },
    {
        "id": "5.4",
        "filename": "Podcast_Item_5_4_Prazo_15_Minutos_pH_e_Temperatura.mp3",
        "title": "Item 5.4 - Prazo de 15 Minutos para pH e Temperatura",
        "dialogue": [
            ("Thalita", "E fechando esse capítulo, no item 5.4, o instrutor citou que o pH e a temperatura precisam ser medidos em até quinze minutos após a coleta, não podendo levar pro laboratório. De onde vem esse prazo de quinze minutos?"),
            ("Francisca", "Essa é uma distinção essencial, Thalita! A ISO 17025 em si não estabelece esse prazo de quinze minutos. Esse limite vem de normas específicas de ensaio, como o consagrado Standard Methods para águas e efluentes."),
            ("Thalita", "Quer dizer que é o método analítico oficial que exige a medição imediata in loco, e não uma cláusula geral da 17025?"),
            ("Francisca", "Exatamente! A 17025 exige que você siga métodos apropriados e válidos. Como o pH e a temperatura de uma amostra de água sofrem trocas gasosas rápidas com a atmosfera, o método manda medir em até quinze minutos. É isso que justifica levar o pHmetro pro campo em vez de engarrafar a água e levar pra bancada."),
            ("Thalita", "Que clareza, Francisca! Conhecer a origem de cada requisito evita misturar regra da norma com regra do método.")
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
    print(f"\n[Seção 5 - Thalita & Francisca] Processando: {ep['title']}...")

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
    print(" GERANDO SEÇÃO 5 (ITENS 5.1 A 5.4) - THALITA & FRANCISCA")
    print("==========================================================")

    silence_file = OUTPUT_DIR / "_silence_180ms.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anullsrc=channel_layout=mono:sample_rate=24000",
        "-t", "0.18", "-q:a", "9", "-acodec", "libmp3lame",
        str(silence_file)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    gerados = []
    for ep in EPISODIOS_SEC5:
        caminho = await gerar_episodio(ep, silence_file)
        gerados.append(caminho)

    # Gera também o episódio completo com a Seção 5 unificada
    print("\n[Capítulo 5 Completo] Unindo os itens 5.1 a 5.4 em um único áudio...")
    ep_completo = OUTPUT_DIR / "Podcast_Capitulo_5_Itens_5_1_a_5_4_Completo_Thalita_e_Francisca.mp3"
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

    print(f"\n[Sucesso] Todos os episódios da Seção 5 foram salvos em: {OUTPUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
