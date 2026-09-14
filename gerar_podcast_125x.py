"""
Piloto de Podcast Estilo NotebookLM usando o backend do LocalDub (Edge-TTS).
Versão acelerada em 1.25x (rate="+25%").
"""
import asyncio
import os
import sys
import subprocess
import tempfile
from pathlib import Path

# Ajusta encoding para UTF-8 no console Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Conecta ao backend do LocalDub
LOCALDUB_BACKEND = Path(r"C:\Users\NOVO OFFLINE\.openclaw\workspace\LocalDub-upstream\backend")
if str(LOCALDUB_BACKEND) not in sys.path:
    sys.path.append(str(LOCALDUB_BACKEND))

from tts import EdgeTTSProvider

OUTPUT_DIR = Path(r"F:\Transcricoes_Consolidadas\Podcasts_Tematicos")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Definição das Personas do Podcast
VOICES = {
    "Mariana": "pt-BR-FranciscaNeural",
    "Lucas": "pt-BR-AntonioNeural"
}

SPEED_RATE = "+25%"  # 1.25x

EPISODIOS = [
    {
        "id": "2.1",
        "filename": "Podcast_Item_2_1_Plano_de_Manutencao_e_Calibracao_1.25x.mp3",
        "title": "Item 2.1 - Plano de Manutenção e Programa de Calibração (1.25x)",
        "dialogue": [
            {
                "speaker": "Mariana",
                "text": "Lucas, vamos começar falando de uma das maiores dores de cabeça nos laboratórios: o controle de calibração e manutenção. O instrutor do curso trouxe uma visão bem pragmática sobre isso no item 2.1."
            },
            {
                "speaker": "Lucas",
                "text": "Excelente, Mariana! E convenhamos, o pessoal adora complicar isso, né? Já vi laboratório mantendo três controles completamente separados pra mesma máquina. O que o instrutor defendeu aqui?"
            },
            {
                "speaker": "Mariana",
                "text": "Ele foi direto ao ponto: não precisa inventar moda. Calibração, verificação intermediária e manutenção preventiva podem estar integradas no mesmo plano geral. O procedimento define as regras e a periodicidade, mas o plano prático só precisa mostrar claramente quando a ação está prevista pra acontecer."
            },
            {
                "speaker": "Lucas",
                "text": "Faz muito sentido. Mas me diz uma coisa: e o avaliador da Cgcre, aceita isso numa boa? A norma não exige formulários separados?"
            },
            {
                "speaker": "Mariana",
                "text": "Aceita sim, com ressalva! Os requisitos 6.4.3 e 6.4.13 da ISO 17025 exigem que o plano exista e esteja sob controle rastreável. A força da evidência tá na rastreabilidade e no cumprimento das datas, e não na quantidade ou na complexidade de planilhas que você inventou."
            },
            {
                "speaker": "Lucas",
                "text": "Perfeito! Menos burocracia de gaveta e mais controle real do que realmente precisa ser feito no mês."
            }
        ]
    },
    {
        "id": "2.2",
        "filename": "Podcast_Item_2_2_Sistema_Informatizado_vs_Planilha_1.25x.mp3",
        "title": "Item 2.2 - Sistema Informatizado pode Substituir Planilha Paralela (1.25x)",
        "dialogue": [
            {
                "speaker": "Lucas",
                "text": "Agora, Mariana, pegando o gancho do item anterior: o que acontece quando o laboratório já tem um sistema informatizado, tipo um LIMS ou um ERP de gestão? Ainda precisa manter aquela planilha paralela no Excel?"
            },
            {
                "speaker": "Mariana",
                "text": "Essa dúvida é clássica! Por receio de auditoria, muita gente alimenta o sistema e ainda gasta horas atualizando uma planilha por fora só por segurança. Mas o parecer técnico no item 2.2 foi taxativo: confirmado. Não há necessidade de controle paralelo."
            },
            {
                "speaker": "Lucas",
                "text": "Que alívio pra rotina da equipe, né? Se o software já cadastra os equipamentos, dispara alertas automáticos de vencimento e bloqueia o uso, qual seria o sentido de retrabalho?"
            },
            {
                "speaker": "Mariana",
                "text": "Exatamente. O requisito 7.11 da norma chancela totalmente o uso de sistemas eletrônicos. O único ponto inegociável é garantir que o sistema seja confiável, tenha controle de acesso, backup e integridade dos dados."
            },
            {
                "speaker": "Lucas",
                "text": "Sensacional. Se a ferramenta já resolve com rastreabilidade, duplicar em planilha só gera risco de divergência."
            }
        ]
    },
    {
        "id": "2.3",
        "filename": "Podcast_Item_2_3_Manutencao_ao_Uso_Real_1.25x.mp3",
        "title": "Item 2.3 - Manutenção Voltada ao Uso Real do Equipamento (1.25x)",
        "dialogue": [
            {
                "speaker": "Lucas",
                "text": "E pra fechar esse bloco, o item 2.3 traz um alerta que muita gente deixa passar batido durante a rotina: a manutenção voltada ao uso real."
            },
            {
                "speaker": "Mariana",
                "text": "Pois é, Lucas! O fornecedor externo vem, executa a manutenção preventiva, entrega aquele relatório bonito cheio de carimbos, e o laboratório apenas arquiva na pasta sem ler. Isso é um perigo enorme!"
            },
            {
                "speaker": "Lucas",
                "text": "Explica melhor pra gente: qual é a pegadinha técnica aí?"
            },
            {
                "speaker": "Mariana",
                "text": "O instrutor usou o exemplo claro de um espectrofotômetro. Se o seu laboratório faz análises em quatrocentos e vinte e oitocentos e oitenta nanômetros, a manutenção precisa testar o equipamento nessa faixa exata de trabalho! Não adianta o técnico testar só no comprimento de onda padrão dele se isso não reflete o seu método de ensaio."
            },
            {
                "speaker": "Lucas",
                "text": "Entendi perfeitamente. A análise crítica do relatório de manutenção é indispensável. Não basta comprovar que a manutenção foi feita; é obrigatório provar que ela cobriu o desempenho requerido pro seu uso pretendido."
            },
            {
                "speaker": "Mariana",
                "text": "Falou tudo! É essa postura crítica que a 17025 exige e que garante a validade técnica dos seus resultados."
            }
        ]
    }
]


async def gerar_audio_episodio(provider: EdgeTTSProvider, episodio: dict, silence_path: Path) -> Path:
    out_path = OUTPUT_DIR / episodio["filename"]
    print(f"\n[Podcast 1.25x] Processando: {episodio['title']}...")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        concat_list_path = tmp_path / "concat.txt"
        file_lines = []

        for idx, turn in enumerate(episodio["dialogue"]):
            speaker = turn["speaker"]
            voice = VOICES[speaker]
            text = turn["text"]
            chunk_file = tmp_path / f"turn_{idx:02d}_{speaker}.mp3"

            print(f"   [{speaker}]: \"{text[:60]}...\"")
            synth_res = await provider.synthesize(text, voice=voice, rate=SPEED_RATE)
            chunk_file.write_bytes(synth_res.audio)

            file_lines.append(f"file '{chunk_file.as_posix()}'")
            # Micropausa de 200ms para 1.25x
            file_lines.append(f"file '{silence_path.as_posix()}'")

        concat_list_path.write_text("\n".join(file_lines), encoding="utf-8")

        cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_list_path),
            "-c:a", "libmp3lame", "-b:a", "192k",
            str(out_path)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    print(f"[OK] Audio 1.25x gerado: {out_path.name} ({out_path.stat().st_size // 1024} KB)")
    return out_path


async def main():
    print("==========================================================")
    print(" GERANDO PODCAST EM VELOCIDADE 1.25X (RATE = +25%)")
    print("==========================================================")

    # 1. Micropausa de 200ms (ajustada para ritmo 1.25x)
    silence_file = OUTPUT_DIR / "_silence_200ms.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anullsrc=channel_layout=mono:sample_rate=24000",
        "-t", "0.20", "-q:a", "9", "-acodec", "libmp3lame",
        str(silence_file)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    provider = EdgeTTSProvider()
    gerados = []

    for ep in EPISODIOS:
        caminho = await gerar_audio_episodio(provider, ep, silence_file)
        gerados.append(caminho)

    # Versão unificada em 1.25x
    episodio_completo = OUTPUT_DIR / "Podcast_Capitulo_2_Itens_2_1_a_2_3_Completo_1.25x.mp3"
    silence_800ms = OUTPUT_DIR / "_silence_800ms.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anullsrc=channel_layout=mono:sample_rate=24000",
        "-t", "0.8", "-q:a", "9", "-acodec", "libmp3lame",
        str(silence_800ms)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        linhas_full = []
        for g in gerados:
            linhas_full.append(f"file '{g.as_posix()}'")
            linhas_full.append(f"file '{silence_800ms.as_posix()}'")
        f.write("\n".join(linhas_full))
        concat_full = f.name

    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_full,
        "-c:a", "libmp3lame", "-b:a", "192k",
        str(episodio_completo)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    try:
        silence_file.unlink(missing_ok=True)
        silence_800ms.unlink(missing_ok=True)
        os.remove(concat_full)
    except Exception:
        pass

    print("\n[Sucesso] Todos os audios em 1.25x foram gerados com sucesso!")
    print(f"Pasta de destino: {OUTPUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
