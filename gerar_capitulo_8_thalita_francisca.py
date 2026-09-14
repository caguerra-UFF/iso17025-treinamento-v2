"""
Gera os episódios da Seção 8 (Itens 8.1, 8.2, 8.3 e 8.4 da Parte 1)
no padrão oficial aprovado: Thalita & Francisca.
Requisito 6.6 da ISO/IEC 17025:2017 - Produtos e Serviços Providos Externamente.
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

import edge_tts

OUTPUT_DIR = Path(r"F:\Transcricoes_Consolidadas\Podcasts_Tematicos\Thalita_e_Francisca")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

VOZ_THALITA = "pt-BR-ThalitaMultilingualNeural"
VOZ_FRANCISCA = "pt-BR-FranciscaNeural"

EPISODIOS_SEC8 = [
    {
        "id": "8.1",
        "filename": "Podcast_Item_8_1_Especificacao_Vinculada_ao_Ensaio.mp3",
        "title": "Item 8.1 - Especificação Vinculada ao Ensaio",
        "dialogue": [
            ("Thalita", "Francisca, entramos agora no Capítulo 8 da nossa jornada pela ISO 17025, focado no Requisito 6.6: produtos e serviços providos externamente. O instrutor sugeriu que os laboratórios tenham uma lista de insumos e serviços vinculada a cada ensaio. A norma realmente obriga a ter uma lista separada por ensaio?"),
            ("Francisca", "Excelente ponto, Thalita! A classificação técnica dessa fala é Confirmado com Ressalva. O requisito 6.6.2, alínea a, exige que o laboratório defina, analise criticamente e aprove seus requisitos para produtos e serviços. Ter uma lista estruturada por ensaio é uma estratégia de gestão fantástica que facilita muito a rotina, mas a ISO 17025 não impõe esse formato como mandatório."),
            ("Thalita", "E na prática de bancada, como isso funciona pra um ensaio típico, como a medição de pH?"),
            ("Francisca", "Pense na ficha técnica do ensaio de pH: ali você já define o modelo e faixa do pHmetro, os requisitos do eletrodo, os padrões de tampão necessários, a incerteza máxima admitida e a validade mínima no momento da entrega. Quando o setor de compras vai contratar, usa essa ficha pronta. Isso elimina compras improvisadas de insumos que não atendem ao método!"),
            ("Thalita", "Perfeito! O setor de compras não fica no escuro e a qualidade técnica do ensaio fica blindada desde a raiz.")
        ]
    },
    {
        "id": "8.2",
        "filename": "Podcast_Item_8_2_Validacao_do_Metodo_para_Especificacoes.mp3",
        "title": "Item 8.2 - Usar a Validação ou Verificação para Definir Especificações",
        "dialogue": [
            ("Thalita", "No Item 8.2, Francisca, vem uma orientação técnica valiosa: usar o estudo de validação ou verificação do método como a base técnica para especificar as compras. Mas isso não corre o risco de amarrar o laboratório a uma marca ou modelo pra sempre?"),
            ("Francisca", "De forma alguma, Thalita! Essa é uma boa prática metrológica que não engessa a gestão. O estudo de verificação documenta exatamente em que condições o laboratório comprovou que atinge o desempenho requerido. A norma não obriga a casar para sempre com a marca comercial utilizada no estudo."),
            ("Thalita", "E como isso resolve a vida do laboratório, especialmente no setor público com a lei de licitações?"),
            ("Francisca", "Em compras públicas você não pode exigir marcas. Mas, usando os dados da validação, você especifica requisitos técnicos de desempenho: grau de pureza, limites de contaminantes e incertezas máximas admitidas. Qualquer fornecedor pode concorrer, desde que cumpra esses critérios. E se um novo insumo alterar uma contribuição relevante da incerteza, o laboratório apenas reavalia o impacto."),
            ("Thalita", "Brilhante! Você respeita as regras de contratação pública e ao mesmo tempo mantém o rigor metrológico intacto.")
        ]
    },
    {
        "id": "8.3",
        "filename": "Podcast_Item_8_3_Avaliacao_Selecao_Monitoramento_Reavaliacao.mp3",
        "title": "Item 8.3 - Ciclo Completo de Fornecedores: Avaliação, Monitoramento e Reavaliação",
        "dialogue": [
            ("Thalita", "Chegamos ao Item 8.3, tratando do ciclo completo de fornecedores exigido pelo item 6.6.2 da norma. Francisca, por que tanta gente erra achando que reavaliação de fornecedor é só preencher uma planilha com nota máxima no fim do ano, sem critério algum?"),
            ("Francisca", "Esse é o clássico cumprimento de tabela que não engana nenhum auditor sério, Thalita! A ISO 17025 exige quatro etapas vivas: avaliação prévia, seleção, monitoramento contínuo e reavaliação periódica. A chave de ouro de todo o processo está na terceira etapa: o monitoramento a cada entrega!"),
            ("Thalita", "Ou seja, cada calibração que chega ou cada lote de reagente recebido já gera uma evidência prática de desempenho?"),
            ("Francisca", "Exatamente! Quando um certificado de calibração chega, você confere: atendeu aos pontos pedidos? A incerteza foi a contratada? Houve atraso? Isso é monitoramento. Quando chega o momento da reavaliação anual, você não inventa notas: você simplesmente consolida o histórico real de entregas conformes e desvios ao longo do ano."),
            ("Thalita", "Isso sim é gestão pela evidência objetiva e não papelada inútil de gaveta!")
        ]
    },
    {
        "id": "8.4",
        "filename": "Podcast_Item_8_4_Comunicacao_Competencia_Criterios_Aceitacao.mp3",
        "title": "Item 8.4 - Comunicação com o Provedor: Competência e Critérios de Aceitação",
        "dialogue": [
            ("Thalita", "Pra encerrar a Seção 8, o Item 8.4 aborda o requisito 6.6.3: a comunicação com o provedor externo. O instrutor foi enfático: nunca faça pedidos vagos como simplesmente calibrar termômetro ou comprar tampão de pH. Qual é o risco real disso, Francisca?"),
            ("Francisca", "O risco é gastar orçamento e receber um documento inútil para o seu método, Thalita! A norma estabelece com clareza que o laboratório deve comunicar os critérios de aceitação, as especificações metrológicas, a qualificação requerida de quem presta o serviço e até atividades que pretende realizar nas instalações do prestador."),
            ("Thalita", "E se o laboratório mandar apenas calibrar manômetro sem especificar os pontos de faixa de trabalho nem a incerteza máxima?"),
            ("Francisca", "O calibrador vai escolher três pontos genéricos quaisquer, com a incerteza que for mais cômoda pra ele. Quando o certificado chegar, você não terá respaldo técnico nem contratual para recusar o serviço! O termo de referência de compra precisa ser tão preciso que, se vier fora do padrão, a rejeição seja imediata e incontestável."),
            ("Thalita", "Uma especificação precisa na entrada evita uma não conformidade grave na saída. Aula prática de metrologia e gestão!")
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
    print(f"\n[Seção 8 - Thalita & Francisca] Processando: {ep['title']}...")
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
    print(" GERANDO SEÇÃO 8 (ITENS 8.1 A 8.4) - THALITA & FRANCISCA")
    print("==========================================================")

    silence_file = OUTPUT_DIR / "_silence_180ms.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anullsrc=channel_layout=mono:sample_rate=24000",
        "-t", "0.18", "-q:a", "9", "-acodec", "libmp3lame",
        str(silence_file)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    gerados = []
    for ep in EPISODIOS_SEC8:
        caminho = await gerar_episodio(ep, silence_file)
        gerados.append(caminho)

    print("\n[Capítulo 8 Completo] Unindo os itens 8.1 a 8.4 em um único áudio...")
    ep_completo = OUTPUT_DIR / "Podcast_Capitulo_8_Itens_8_1_a_8_4_Completo_Thalita_e_Francisca.mp3"
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

    print(f"\n[Sucesso] Todos os episódios da Seção 8 foram salvos em: {OUTPUT_DIR}")

if __name__ == "__main__":
    asyncio.run(main())