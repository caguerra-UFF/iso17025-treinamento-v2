"""
Gera os episódios 2.1, 2.2 e 2.3 no padrão vencedor escolhido pelo usuário:
Dupla Feminina Especialista: Thalita (dinâmica/curiosa) + Francisca (especialista técnica).
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

VOZ_THALITA = "pt-BR-ThalitaMultilingualNeural"  # Curiosa, apresentadora dinâmica
VOZ_FRANCISCA = "pt-BR-FranciscaNeural"          # Especialista técnica, autoridade normativa

EPISODIOS = [
    {
        "id": "2.1",
        "filename": "Podcast_Item_2_1_Plano_de_Manutencao_e_Calibracao.mp3",
        "title": "Item 2.1 - Plano de Manutenção e Programa de Calibração",
        "dialogue": [
            ("Thalita", "Francisca, vamos começar falando de uma das maiores dores de cabeça nos laboratórios: o controle de calibração e manutenção. O instrutor do curso trouxe uma visão bem pragmática sobre isso no item 2.1."),
            ("Francisca", "Excelente ponto, Thalita! E convenhamos, o pessoal adora complicar isso, né? Já vi laboratório mantendo três controles completamente separados pra mesma máquina. O que o instrutor defendeu aqui foi direto ao ponto: não precisa inventar moda. Calibração, verificação intermediária e manutenção preventiva podem estar integradas no mesmo plano geral."),
            ("Thalita", "Nossa, isso facilita demais! Mas me diz uma coisa: e o avaliador da Cgcre, aceita isso numa boa? A norma não exige formulários separados?"),
            ("Francisca", "Aceita sim, com ressalva! Os requisitos 6.4.3 e 6.4.13 da ISO 17025 exigem que o plano exista e esteja sob controle rastreável. A força da evidência tá na rastreabilidade e no cumprimento das datas, e não na quantidade ou na complexidade de planilhas que você inventou."),
            ("Thalita", "Perfeito! Menos burocracia de gaveta e mais controle real do que realmente precisa ser feito no mês.")
        ]
    },
    {
        "id": "2.2",
        "filename": "Podcast_Item_2_2_Sistema_Informatizado_vs_Planilha.mp3",
        "title": "Item 2.2 - Sistema Informatizado pode Substituir Planilha Paralela",
        "dialogue": [
            ("Thalita", "Agora, Francisca, pegando o gancho do item anterior: o que acontece quando o laboratório já tem um sistema informatizado, tipo um LIMS ou um ERP de gestão? Ainda precisa manter aquela planilha paralela no Excel?"),
            ("Francisca", "Essa dúvida é clássica, Thalita! Por receio de auditoria, muita gente alimenta o sistema e ainda gasta horas atualizando uma planilha por fora só por segurança. Mas o parecer técnico no item 2.2 foi taxativo: confirmado. Não há necessidade de controle paralelo."),
            ("Thalita", "Que alívio pra rotina da equipe, né? Se o software já cadastra os equipamentos, dispara alertas automáticos de vencimento e bloqueia o uso, qual seria o sentido de retrabalho?"),
            ("Francisca", "Exatamente. O requisito 7.11 da norma chancela totalmente o uso de sistemas eletrônicos. O único ponto inegociável é garantir que o sistema seja confiável, tenha controle de acesso, backup e integridade dos dados."),
            ("Thalita", "Sensacional. Se a ferramenta já resolve com rastreabilidade, duplicar em planilha só gera risco de divergência.")
        ]
    },
    {
        "id": "2.3",
        "filename": "Podcast_Item_2_3_Manutencao_ao_Uso_Real.mp3",
        "title": "Item 2.3 - Manutenção Voltada ao Uso Real do Equipamento",
        "dialogue": [
            ("Thalita", "E pra fechar esse bloco, Francisca, o item 2.3 traz um alerta que muita gente deixa passar batido durante a rotina: a manutenção voltada ao uso real."),
            ("Francisca", "Pois é, Thalita! O fornecedor externo vem, executa a manutenção preventiva, entrega aquele relatório bonito cheio de carimbos, e o laboratório apenas arquiva na pasta sem ler. Isso é um perigo enorme!"),
            ("Thalita", "Explica melhor pra gente: qual é a pegadinha técnica aí?"),
            ("Francisca", "O instrutor usou o exemplo claro de um espectrofotômetro. Se o seu laboratório faz análises em quatrocentos e vinte e oitocentos e oitenta nanômetros, a manutenção precisa testar o equipamento nessa faixa exata de trabalho! Não adianta o técnico testar só no comprimento de onda padrão dele se isso não reflete o seu método de ensaio."),
            ("Thalita", "Entendi perfeitamente. A análise crítica do relatório de manutenção é indispensável. Não basta comprovar que a manutenção foi feita; é obrigatório provar que ela cobriu o desempenho requerido pro seu uso pretendido."),
            ("Francisca", "Falou tudo! É essa postura crítica que a 17025 exige e que garante a validade técnica dos seus resultados.")
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
    print(f"\n[Podcast Thalita & Francisca] Processando: {ep['title']}...")

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
    print(" GERANDO ITENS 2.1, 2.2 E 2.3 (PADRÃO THALITA & FRANCISCA)")
    print("==========================================================")

    silence_file = OUTPUT_DIR / "_silence_180ms.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anullsrc=channel_layout=mono:sample_rate=24000",
        "-t", "0.18", "-q:a", "9", "-acodec", "libmp3lame",
        str(silence_file)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    gerados = []
    for ep in EPISODIOS:
        caminho = await gerar_episodio(ep, silence_file)
        gerados.append(caminho)

    # Gera também o episódio completo com os 3 itens juntos
    print("\n[Podcast Completo] Unindo os 3 itens em um único áudio contínuo...")
    ep_completo = OUTPUT_DIR / "Podcast_Capitulo_2_Itens_2_1_a_2_3_Completo_Thalita_e_Francisca.mp3"
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

    print(f"\n[Sucesso] Todos os episódios foram salvos em: {OUTPUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
