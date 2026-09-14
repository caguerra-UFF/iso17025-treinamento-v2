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

EPISODIOS_SEC10 = [
    {
        "id": "10.1",
        "filename": "Podcast_Item_10_1_Checklist_Tecnico_Certificados_Calibracao.mp3",
        "title": "Item 10.1 - Checklist Técnico Mínimo para Análise Crítica de Certificados",
        "dialogue": [
            ("Thalita", "Francisca, entramos no Capítulo 10: a oficina prática de análise crítica de certificados de calibração. Na rotina, a gente vê muito analista apenas conferir se o certificado tem o logotipo de acreditação e arquivar numa pasta. O que a ISO 17025 realmente exige do laboratório?"),
            ("Francisca", "Esse é um dos pontos onde mais chovem não conformidades em auditoria, Thalita! Arquivar certificado sem análise crítica é omissão grave. O laboratório tem que passar o documento por um checklist técnico rigoroso antes de autorizar o uso do equipamento."),
            ("Thalita", "E quais são as perguntas obrigatórias desse checklist técnico?"),
            ("Francisca", "São pelo menos seis pontos vitais: primeiro, o número de série e identificação batem exatamente com o nosso instrumento? Segundo, os pontos calibrados cobrem a faixa real de trabalho? Terceiro, o erro medido e a incerteza declarada atendem aos nossos critérios de aceitação? Quarto, os padrões usados têm rastreabilidade comprovada? E quinto, se houve ajuste, o calibrador informou os dados de antes e depois?"),
            ("Thalita", "Perfeito! Cada certificado tem que virar uma decisão documentada de conformidade e não apenas um papel guardado na gaveta.")
        ]
    },
    {
        "id": "10.2",
        "filename": "Podcast_Item_10_2_Capacidade_Medicao_Calibracao_CMC.mp3",
        "title": "Item 10.2 - Capacidade de Medição e Calibração (CMC) do Prestador",
        "dialogue": [
            ("Thalita", "No Item 10.2, o treinamento destacou a sigla CMC: Capacidade de Medição e Calibração do prestador de serviço. Francisca, por que o laboratório precisa consultar a CMC antes mesmo de mandar o equipamento para calibração?"),
            ("Francisca", "Porque a CMC representa a menor incerteza de medição que aquele laboratório de calibração consegue entregar na rotina para aquela faixa e grandeza, Thalita! Está tudo público na planilha de escopo acreditado da Cgcre."),
            ("Thalita", "E qual é o perigo de não checar a CMC antes de fechar o contrato?"),
            ("Francisca", "O perigo é contratar um laboratório acreditado cuja melhor incerteza é grosseira demais para a sua tolerância de ensaio! Se o seu método exige incerteza menor que um décimo de grau Celsius e a CMC do prestador é de meio grau, o certificado dele não servirá para aprovar o seu termômetro. Olhar a CMC garante que você só contrata quem tem capacidade metrológica compatível com o seu processo."),
            ("Thalita", "Excelente visão! Contratar competência técnica começa na consulta prévia do escopo de acreditação.")
        ]
    },
    {
        "id": "10.3",
        "filename": "Podcast_Item_10_3_Exemplo_pHmetro_Calibracao_Eletrica.mp3",
        "title": "Item 10.3 - O Caso do pHmetro: A Polêmica da Calibração da Parte Elétrica",
        "dialogue": [
            ("Thalita", "No Item 10.3 surge uma polêmica clássica de laboratório: o instrutor afirmou que o pHmetro precisa ter a chamada calibração da parte elétrica com simulador de milivolt, além do uso de materiais de referência. Francisca, a ISO 17025 exige ao pé da letra essa calibração elétrica separada?"),
            ("Francisca", "Atenção máxima a esse detalhe, Thalita! A nossa equipe técnica marcou esse trecho com Alerta e Fonte Complementar. A ISO 17025 exige calibração quando ela afeta o resultado, adequação ao uso e rastreabilidade metrológica. Mas a norma internacional não prescreve o roteiro interno para pHmetros nem crava a fórmula parte elétrica mais padrão tampão."),
            ("Thalita", "E de onde vem essa prática tão comum nos laboratórios brasileiros?"),
            ("Francisca", "Vem de guias orientativos específicos e práticas consolidadas da metrologia química. O importante na hora da contratação não é escrever calibração elétrica obrigatória pela ISO, mas sim descrever tecnicamente a faixa elétrica em milivolts, os pontos requeridos, erros máximos e padrões para demonstrar o desempenho global do sistema de medição."),
            ("Thalita", "Perfeito esclarecimento! Separar o que é texto estrito da ISO do que é prática técnica setorial evita discussões infundadas com auditores.")
        ]
    },
    {
        "id": "10.4",
        "filename": "Podcast_Item_10_4_Sensor_Temperatura_Associado_pHmetro.mp3",
        "title": "Item 10.4 - Sensor de Temperatura Associado: A Faixa Real de Medição",
        "dialogue": [
            ("Thalita", "Pra fechar a Seção 10, o Item 10.4 traz o exemplo de um certificado de sensor de temperatura associado a um pHmetro, calibrado nos pontos vinte, vinte e cinco e trinta graus Celsius. O instrutor questionou se essa faixa era suficiente. Qual foi o ponto central dessa reflexão, Francisca?"),
            ("Francisca", "O ponto central é a compatibilidade entre a calibração e a rotina real do laboratório, Thalita! A medição potenciométrica de pH depende criticamente da compensação automática de temperatura baseada na equação de Nernst. Se o sensor de temperatura errar, o valor de pH lido estará errado."),
            ("Thalita", "E se o laboratório mede água de rio no campo a dez graus no inverno, ou amostras industriais a quarenta graus?"),
            ("Francisca", "Aí está a armadilha! Se o certificado só cobriu de vinte a trinta graus, o instrumento estará operando em uma faixa não calibrada fora desses limites! A ISO 17025 não determina os pontos vinte, vinte e cinco ou trinta; é o laboratório que tem o dever de definir e exigir a faixa de temperatura em que suas amostras são efetivamente medidas."),
            ("Thalita", "Uma lição de ouro: calibrar não é cumprir protocolo engessado, é reproduzir com fidelidade a realidade operacional da bancada e do campo!")
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
    t_title = ep["title"]
    print(f"\n[Seção 10 - Thalita & Francisca] Processando: {t_title}...")
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
    print(" GERANDO SEÇÃO 10 (ITENS 10.1 A 10.4) - THALITA & FRANCISCA")
    print("==========================================================")

    silence_file = OUTPUT_DIR / "_silence_180ms.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anullsrc=channel_layout=mono:sample_rate=24000",
        "-t", "0.18", "-q:a", "9", "-acodec", "libmp3lame",
        str(silence_file)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    gerados = []
    for ep in EPISODIOS_SEC10:
        caminho = await gerar_episodio(ep, silence_file)
        gerados.append(caminho)

    print("\n[Capítulo 10 Completo] Unindo os itens 10.1 a 10.4 em um único áudio...")
    ep_completo = OUTPUT_DIR / "Podcast_Capitulo_10_Itens_10_1_a_10_4_Completo_Thalita_e_Francisca.mp3"
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

    print(f"\n[Sucesso] Todos os episódios da Seção 10 foram salvos em: {OUTPUT_DIR}")

if __name__ == "__main__":
    asyncio.run(main())